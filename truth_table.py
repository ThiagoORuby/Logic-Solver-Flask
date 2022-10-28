import itertools
import pandas as pd
# Truth table solve method
# → ¬ ∧ ∨
def replace_exp(exp):
    exp = exp.replace("→", "<=")
    exp = exp.replace("¬", "0**")
    exp = exp.replace("∧", "and")
    exp = exp.replace("∨", "or")
    return exp

def get_list(exp):
    new_exp = []
    for ex in exp:
        new_exp.append(replace_exp(ex))
    return new_exp

def get_atoms(exp):
    atoms = set()
    dict_atoms = {}
    for ex in exp:
        for i in ex:
            # pegando os atomos 
            if i not in '→¬∧∨() ':
                atoms.add(i)
    for i in atoms:
        dict_atoms[i] = [0,1]
    return dict_atoms

def create_table(obj, exp):
    table = []
    row = []
    atoms = get_atoms(exp)
    answer = ' and '.join(exp)  + ' <= ' + obj
    exp.append(answer)
    exp_rep = get_list(exp)
    comb = list(itertools.product(*[atoms[x] for x in atoms.keys()]))
    # For loop
    dic2 = list()
    keys = list(atoms.keys())
    for c in comb:
        dic2.append({keys[i] : c[i] for i in range(len(c))})
    
    #print(dic2[0:1])
    #print(exp_rep[0:1])
    i = 0
    for c in dic2:
        row = []
        for ex in exp_rep:
            res = int(eval(ex, c))
            row.append(res)
        table.append(list(comb[i]) + row)
        i+=1
    exp.pop(len(exp)-1)
    exp.append(f"→ {obj}")
    dt = pd.DataFrame(table, columns= keys+exp)
    #print(dt)
    #print()
    color = list(dt.index[dt.iloc[:, len(keys):].product(axis=1) == 1])
    #print(dt.to_dict())
    return [table, keys+exp, color]

