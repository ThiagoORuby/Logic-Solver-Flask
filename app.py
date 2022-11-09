from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from brain import Brain
from truth_table import create_table
import pandas as pd
from random import randint


def create_app():
    app = Flask(__name__)

    # Generate example list
    text = ''
    with open('examples.txt', 'r', encoding='utf-8') as file:
        text += file.read()
    lista = text.split('\n\\e\n')
    example_list = [lista[i].split('\n\\s\n') for i in range(len(lista))]
    ##################################

    def get_answer(kb, obj):
        brain = Brain(kb)
        brain.print_list.clear()
        try:
            ret = brain.new_ask(obj)
        except:
            return [False, -1]
        print(brain.print_list)
        if ret:
            return [brain.print_list, True]
        else:
            return [brain.print_list, False]

    @app.route('/', methods=['POST', 'GET'])
    def home():
        info = False
        obj = None
        finded = False
        columns = []
        color = False
        buttons = [x for x in "→¬∧∨()"]
        if request.method == 'POST':
            kb = request.form['kb']
            kb = kb.split('\r\n')
            print("kb: ", kb)
            obj = request.form['obj']
            tipo = request.form['method']
            if tipo == 'logic_inference':
                print("tipo" , tipo)
                print(obj)
                info, finded = get_answer(kb, obj)
                columns = ['Proposition', 'Origin']
            elif tipo == 'truth_table':
                try:
                    info, columns, color = create_table(obj, kb)
                    if color:
                        finded = True
                    else:
                        finded = False
                except:
                    finded = -1
        print("columns: ", columns)
        return render_template('index.html', buttons=buttons, table_info = info, obj=obj, columns=columns, finded=finded, color = color)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/example')
    def example():
        choice = randint(0, len(example_list))
        response = {"kb" : example_list[choice][0], "obj" : example_list[choice][1]}
        return jsonify(response)

    return app