# Logic inference functions

def modus_ponens(exp1, exp2):
    if not('→' in exp1) and not('→' in exp2):
        return [False, None]
    if len(exp1) < 3 or not('→' in exp1):
        exp1, exp2 = exp2, exp1
    exp1 = exp1.replace('(', '').replace(')', '')
    splited = exp1.split('→')
    #print(exp2[::-1])
    if exp2 == splited[0] or exp2[::-1] == splited[0] or (exp2 in splited[0] and 'V' in splited[0]):
        return [splited[1], None]
    if exp2 in splited[0] and '∧' in splited[0]:
        return [-1, splited[0].replace(exp2, '').replace('∧', '')]
    return [False, None]

# Modus Tollens -> Return -1 if a -> ~bVc garantir que ~c existe na kb
def modus_tollens(exp1, exp2):
    if not('→' in exp1) and not('→' in exp2):
        return [False, None]
    if len(exp1) < 3 or not('→' in exp1):
        exp1, exp2 = exp2, exp1
    exp1 = exp1.replace('(', '').replace(')', '')
    splited = exp1.split('→')
    if '¬' in exp2 or '¬' in splited[1]:
        if exp2 == splited[1].replace('¬', '', 1) or (exp2 in splited[1] and '∧' in splited[1]):
            return ['¬'+splited[0], None]
        if exp2 == splited[1].replace('¬', '', 1) or exp2.replace('¬', '', 1) == splited[1]:
            return ['¬'+splited[0], None]
    return [False, None]

def syllogism(exp1, exp2):
    if not('∨' in exp1) and not('∨' in exp2):
        return [False, None]
    if len(exp1) < 3 or not('∨' in exp1):
        exp1, exp2 = exp2, exp1
    exp1 = exp1.replace('(', '').replace(')', '')
    splited = exp1.split('∨')
    if '¬' in exp2 or '¬' in splited[1] or '¬' in splited[0]:
        if exp2 == splited[1].replace('¬', '', 1) or exp2.replace('¬', '', 1) == splited[1]:
            return [splited[0], None]
        if exp2 == splited[0].replace('¬', '', 1) or exp2.replace('¬', '', 1) == splited[0]:
            return [splited[1], None]
    return [False, None]

# hypotetic syllogism
def hypotetic_syllogism(exp1, exp2):
    if not('→' in exp1) and not('→' in exp2):
        return [False, None]
    if not('→' in exp1) and '→' in exp2:
        return [False, None]
    if not('→' in exp2) and '→' in exp1:
        return [False, None]
    splited1 = exp1.split('→')
    splited2 = exp2.split('→')
    if splited1[1] == splited2[0]:
        return [splited1[0]+'→'+splited2[1]]
    if splited2[1] == splited1[0]:
        return [splited2[0]+'→'+splited1[1]]
    return [False, None]

# resolution
def resolution(exp1, exp2):
    if not('∨' in exp1) and not('∨' in exp2):
        return [False, None]
    if not('∨' in exp1) and '∨' in exp2:
        return [False, None]
    if not('∨' in exp2) and '∨' in exp1:
        return [False, None]
    splited1 = exp1.split('∨')
    splited2 = exp2.split('∨')
    if ('¬' in splited2[0] or '¬' in splited1[0]):
        if splited1[0] == splited2[0].replace('¬', '', 1):
            return [splited1[1]+'∨'+splited2[1]]
        if splited2[0] == splited1[0].replace('¬', '', 1):
            return [splited2[1]+'∨'+splited1[1]]
    return [False, None]
    

def addition(exp1, exp2):
    return [exp1 + '∨' + exp2, None]

def conjuction(exp1, exp2):
    return [exp2 + '∧' + exp1, None]


#print(modus_tollens('a→¬c', 'c'))
#print(l.replace('(', ''))
#print(eval('(1 or 2)'))
#print(modus_tollens('a→(bvc)', '¬(bvc)'))