# Duas listas: expressões iniciais e stack de operações
# pegar a menor expressão
# Adicionar o score de cada expressão com base na menor
# operação entre a menor e a com maior score
# add novo valor nas duas listas e volta ao passo 3 com esse novo valor
# se valor == resultado, fim do algoritmo 

import re
from logic_rules import modus_ponens, modus_tollens, syllogism, hypotetic_syllogism, resolution, conjuction
import collections
# Fazer esse loop ate nao ter mais elementos em dict_exp
# caso nao tenha achado a resposta, então:
# fazer as operações de conjunção entre os elementos na memoria
# caso nao encontre a resposta, retorne falso

# VER ALGORITMO A* PARA TENTAR MELHORAR ESSA HEURISTICA
# DEPENDE DO OBJETIVO E DO PROXIMO PASSO (SOMA)

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
            # Pegando o dicionario com os scores universais
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

    def _try_find(self, exp):
        if not self.exp_dict:
            return False
        if exp in self.exp_dict or exp in self.cache_list:
            return True
        return False

    def _clear_score(self):
        self.exp_dict = {x : 0 for x in self.exp_dict.keys()}

    def get_scores(self, key, obj):
        if(self.exp_dict == None): return True
        score = dict()
        for x in self.exp_dict.keys():
            # para cada char no valor
            if(x != key): score[x] = 0
            for j in x:
                # se o atomo está la ou o objetivo esta la, add +1
                if (j in self._get_atoms(key)) and x != key: score[x] += 1
            if obj in x and x != key: score[x] += 1
        return score
    
    def _clear_all(self):
        self.print_list.clear()
        self.atoms = set()
        self.cache_list.clear()
        self.achou = False
        self.exp_dict.clear()

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

    def bfs(self, exp, obj, i):
        # Dict to find next
        print(f'exp atual: {exp} e obj: {obj}')
        if(exp == obj) or self._find_conjuctions(obj):
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
                # quando falta algum valor pra funfar
                if ret[0] == -1:
                    # Para modus ponens
                    if name == "Modus Ponens":
                        finded = self._try_find(ret[1])
                        # Se encontrou:
                        if finded:
                            print("Complementar encontrado!")
                            ret[0] = conjuction(ret[1], min(exp, txt, key=len))[0]
                            name = "Conjunção"
                        else:
                            ret[0] = 0
                if ret[0] == 0:
                    if not self.achou:
                        if self.print_list:
                            # Outra solução: No final, retirar as premissas repetidas
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
    
    def _check_printed(self, exp):
        inside = [i[0] for i in self.print_list]
        if exp in inside:
            return True
        return False

    # modus ponens retorna falso e o valor que falta pra funcionar, se existir
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
    
    def _find_conjuctions(self, obj):
        if '∧' in obj:
            splited = obj.replace(' ', '').split('∧')
            for i in splited:
                if i not in self.exp_dict.keys(): return False
            self.cache_list.append(obj)
            self.print_list.append([obj, 'Conjunction'])
            return True
        return False
    
    def _find_additions(self):
        pass

