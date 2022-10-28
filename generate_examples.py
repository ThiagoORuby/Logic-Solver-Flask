import json
text = ''
with open('examples.txt', 'r', encoding='utf-8') as file:
    text += file.read()

lista = text.split('\n\\e\n')
#print(lista[0].split('\n\\s\n'))

split_list = [lista[i].split('\n\\s\n') for i in range(len(lista))]
print(split_list)


