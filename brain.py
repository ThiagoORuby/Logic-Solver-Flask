# THE LOGIC INFERENCE BRAIN

from logic_rules import modus_ponens, modus_tollens, syllogism, hypotetic_syllogism, resolution, conjuction


class Brain:

    atoms = set()
    exp_dict = dict() 
    cache_list = list()
    print_list = list()
    achou = False

    # Init the brain and generate atoms list and exp_dict
    def __init__(self, kb):
        self._clear_all()
        for ex in kb:
            exp = ex.replace(' ', '')
            for i in exp:
                # pegando os atomos 
                if i not in '→¬∧∨()':
                    self.atoms.add(i)
            score = 0
            #atoms_list = sorted(self.atoms)
            self.exp_dict[exp] = score
        self.atoms = list(self.atoms)
            #list_exp.append(exp)
    
    def _get_atoms(self, exp):
        ret = ''
        for i in exp:
            if(i not in '¬()∧∨→'): ret+=i
        return ret

    # add some new exp in the exp_dict
    def _add_to_dict(self, exp):
        if(self.exp_dict == None): return True
        score = 0
        for i in exp:
            self.exp_dict[i] = score

    # try find some exp in exp_dict
    def _try_find(self, exp):
        if not self.exp_dict:
            return False
        if exp in self.exp_dict or exp in self.cache_list:
            return True
        return False

    # clear the score of exp_dict
    def _clear_score(self):
        self.exp_dict = {x : 0 for x in self.exp_dict.keys()}

    # get the new scores of exp_dict
    def get_scores(self, key, obj):
        if(self.exp_dict == None): return True
        score = dict()
        # for each expression in exp_dict
        for x in self.exp_dict.keys():
            # create a new dict without the current key
            if(x != key): score[x] = 0
            # for each char in each expression
            for j in x:
                # if this char has in the key, add +1 to score
                if (j in self._get_atoms(key)) and x != key: score[x] += 1
            # if the objective is in the expression, add +1 to score
            if obj in x and x != key: score[x] += 1
        return score
    
    # Restart all the atributes
    def _clear_all(self):
        self.print_list.clear()
        self.atoms = set()
        self.cache_list.clear()
        self.achou = False
        self.exp_dict.clear()

    # Do a new ask to the Knowledge base 
    def new_ask(self, obj):
        self.exp_dict = dict(sorted(list(self.exp_dict.items()), key=lambda l: len(l[0])))
        print(self.exp_dict)
        obj = obj.replace(' ', '')
        for value in list(self.exp_dict.keys()):
            if not self.achou:
                self._clear_score()
                ret = self.bfs(value, obj, 0)
        print("ret final: ", ret)
        if not self.achou:
            return self._find_conjuctions(obj)
        return self.achou
    
    # Compare two expressions without parentesis
    def _compare_results(self, exp1, exp2):
        exp1 = exp1.replace('(', '').replace(')', '')
        exp2 = exp2.replace("(", '').replace(")", '')
        if exp1 == exp2: return True
        return False

    # doing the heuristic BFS
    def bfs(self, exp, obj, i):
        # Dict to find next
        print(f'exp atual: {exp} e obj: {obj}')

        # Stop conditions
        if(self._compare_results(exp, obj)) or self._find_conjuctions(obj) or self._find_additions(obj):
            print("Achei!")
            self.exp_dict = None
            self.achou = True
            return True
        
        scores = self.get_scores(exp, obj)
        if(scores == True): return True
        scores = dict(sorted(scores.items(), key=lambda x:x[1], reverse=True))

        if (sum(scores.values()) == 0):
            if(self.exp_dict):
                del self.exp_dict[exp]
                if(self.exp_dict):
                    exp = min(self.exp_dict.keys(), key=len)
                    self.bfs(exp, obj, i+1)
            return False
        
        print(scores)
        for txt in scores.keys():
            if scores[txt] != 0:
                print("next: ", txt)
                ret, name = self._apply_rules(txt, exp)
                print("ret: ", ret[0])
                # If need some value to apply rule
                if ret[0] == -1:
                    # For modus ponens
                    if name == "Modus Ponens":
                        finded = self._try_find(ret[1])
                        # if find:
                        if finded:
                            print("Complementar encontrado!")
                            ret[0] = conjuction(ret[1], min(exp, txt, key=len))[0]
                            name = "Conjunção"
                        else:
                            ret[0] = 0
                if ret[0] == 0:
                    if not self.achou:
                        if self.print_list:
                            # Another solution: At the end, remove the repeated premises
                            #self.print_list.pop()
                            #if self.print_list: self.print_list.pop()
                            print()
                    continue
                # execute the changes
                if(len(ret[0]) >= 3 and ret[0][0:2] == '¬¬'): ret[0] = ret[0][2:]
                self.cache_list.append(exp)
                self.cache_list.append(txt)
                if self.achou == False:
                    if not self._check_printed(exp):
                        self.print_list.append([exp, "Premise " + str(list(self.exp_dict.keys()).index(exp)+1)])
                    self.print_list.append([txt, "Premise " + str(list(self.exp_dict.keys()).index(txt)+1)])
                    self.print_list.append([ret[0], name])
                self._add_to_dict([ret[0]])
                self.bfs(ret[0], obj, i+1)
    
    # Check if has in the printed_list to avoid repetitions
    def _check_printed(self, exp):
        inside = [i[0] for i in self.print_list]
        if exp in inside:
            return True
        return False

    # Apply Inference rules
    def _apply_rules(self, exp1, exp2):
        if(modus_ponens(exp1, exp2)[0]): 
            return [modus_ponens(exp1, exp2), 'Modus Ponens']
        if(modus_tollens(exp1, exp2)[0]):
            return [modus_tollens(exp1, exp2), 'Modus Tollens']
        if(syllogism(exp1, exp2)[0]):
            return [syllogism(exp1, exp2), 'Disjunctive Syllogism']
        if(hypotetic_syllogism(exp1, exp2)[0]):
            return [hypotetic_syllogism(exp1, exp2), 'Hypothetical Syllogism']
        if(resolution(exp1, exp2)[0]):
            return [resolution(exp1, exp2), "Resolution"]
        print("to aqui")
        return [[0, None], 'erro']
    
    # Find possible conjunctions that solve the problem
    def _find_conjuctions(self, obj):
        if '∧' in obj:
            splited = obj.replace(' ', '').replace('(', '').replace(')', '').split('∧')
            for i in splited:
                if i not in self.exp_dict.keys(): return False
            self.cache_list.append(obj)
            self.print_list.append([obj, 'Conjunction'])
            return True
        return False
    
    # Find possible additions that solve the problem
    def _find_additions(self, obj):
        qnt = 0
        if '∨' in obj:
            splited = obj.replace(' ', '').replace('(', '').replace(')', '').split('∨')
            for i in splited:
                if i in self.exp_dict.keys(): qnt+=1
            if qnt == 0: return False
            else:
                self.cache_list.append(obj)
                self.print_list.append([obj, 'Addition'])
                return True

