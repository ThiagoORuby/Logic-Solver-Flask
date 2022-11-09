"""
→ ¬ ∧ ∨
4
a → ¬b
c ∨ d
c → b
a
d ?

6
(c ∧ m) → b
f
t
t → c
i → c
(c ∧ f) → g
g

2
j → (l ∧ ¬c)
c
¬j

2
¬r → ¬l
l
r

4
j ∨ b
c ∨ ¬j
¬b ∨ d
¬d
c ∧ j

3
g → ¬d
¬d → ¬i
i
¬g

3
¬a → s
a → ¬p
p
s

4
n → (¬j ∧ ¬r)
¬r → l
l → s
¬s
¬n ∧ ¬l

4
t → s
u → ¬s
¬w
u ∨ w
¬t

P → (Q ∧ R)
(Q ∧ R) → S
S → (T ∨ ( ¬T → U))
P
¬T
U

p
q → (r ∧ s)
t → ¬¬q
t ∨ ¬p
r ∧ s

¬p → (r ∧ ¬s)
t → s
u → ¬p
¬w
u ∨ w
¬t ∨ w

7
p
q ∨ r
s → t
q → u
¬s → ¬r
r → v
¬t
u

7
p → q
r ∨ s
¬s → ¬t
¬q ∨ s
¬s
¬p ∧ r → u
w ∨ t
u ∧ w

10
(a ∧ b ∧ c) → d
(d ∧ f) → G
e → f
f → b
b → c
g → h
i → j
(a ∧ f) → h
a
f
h
e → b
"""
from brain import Brain
from truth_table import create_table, get_atoms

# Teste de entrada inicial
no_of_exp = int(input())
list_exp = list()

for i in range(no_of_exp):
    exp = input()
    list_exp.append(exp)
obj = input()

#brain = Brain(list_exp)
#ret = brain.new_ask(obj)

print()
"""if ret:
    for i in brain.print_list:
        print(i[0] + ' | ' + i[1])
else:
    print("Não foi possivel encontrar")
"""

import itertools

dic = get_atoms(list_exp)

print(dic)
print([dic[x] for x in dic.keys()])
comb = list(itertools.product(*[dic[x] for x in dic.keys()]))

dic2 = list()
keys = list(dic.keys())
for c in comb:
    dic2.append({keys[i] : c[i] for i in range(len(c))})

#print(dic2)

create_table(obj, list_exp)
#print(list_exp)
#print(eval('a + b + c', {'a':[1,2], 'b':[3,1], 'c':[1,2]}))