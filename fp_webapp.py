"""
  website_demo shows how to use templates to generate HTML
  from data selected/generated from user-supplied information
"""

from flask import Flask, render_template, request
import hangman_methods
app = Flask(__name__)

import csv
csv_recipes = list(csv.DictReader(open('RAW_recipes.csv','r'),delimiter=','))


global state
state = {'ingred_list':[]}

@app.route('/')
@app.route('/main')
def main():
	return render_template('quarantineeats.html')


@app.route('/start')
def play():
    global state
    print(state)
    return render_template("start.html",state=state)


@app.route('/submit',methods=['GET','POST'])
def split():
    global state
    ingred_list=request.form['ingred_list']
    sorting=request.form['sorting']
    print(ingred_list)
    state['ingred_list']=ingred_list
    split_ingred = ingred_list.split(",")
    print(split_ingred)
    print(len(split_ingred))

    matching_recipes = []

    if sorting == 'a':
        sorting='time'
    elif sorting == 'b':
        sorting = 'number_steps'
    elif sorting == 'c':
        sorting = 'num_ingredients'
    for i in csv_recipes:
        matches = True
        for x in split_ingred:
            if x not in i['ingredients']:
                matches = False
        if matches:
            matching_recipes.append({'name': [i['name']],'descrip':[i['description']], 'number_steps':[i['n_steps']], 'time':[i['minutes']],'steps':[i['steps']],
                                    'ingred': [i['ingredients']],
                                    'num_ingredients': [i['n_ingredients']]})
            matching_recipes.sort(key=lambda x: x[sorting])
    print("These are the top recipes:\n")
    state['recipe_names']=[]
    state['recipes']=[]
    for y in matching_recipes[0:5]:
        state['recipes'].append(y)
        for key in y['name']:
            print("»" + key)
            state['recipe_names'].append(key)
    print("\n")
    return render_template("submit.html",state=state)


@app.route('/information',methods=['GET','POST'])
def information():
    global state
    state['information']=[]
    state['descrip'] = []
    state['number_steps'] = []
    state['time']=[]
    state['steps'] = []
    state['in'] = []
    state['name'] = []
    print(state['ingred_list'])
    narrow=request.form['gender']
    state['narrow'] = narrow
    state['all'] = 'all'
    state['description'] = 'description'
    state['numsteps'] = 'number of steps'
    state['t'] = 'time'
    state['s'] = 'step'
    r=request.form['r']

    if narrow == 'all':
        print("\n")
        for y in state['recipes']:
            for key in y['name']:
                if r == key:
                    state['information'].append(y)
                    state['name'].append(y['name'])
                    state['in'].append(y['ingred'])
                    state['descrip'].append(y['descrip'])
                    state['number_steps'].append(y['number_steps'])
                    state['time'].append(y['time'])
                    state['steps'].append(y['steps'])
                    print("Description:", y['descrip'])
                    print("This recipe has", y['number_steps'], "steps.")
                    print("This recipe takes", y['time'], "minutes.")
                    if "/" in y['steps']:
                        state['information'].append(y['steps'])
                        print("These are the steps: \n\n ", str(y['steps']).replace('/' , '\n'))
                    else:
                        print("These are the steps: \n\n ", str(y['steps']).replace(',' , '\n'))

    if narrow == 'description':
        print("\n")
        for y in state['recipes']:
            for key in y['name']:
                if r == key:
                    state['information'].append(y['descrip'])
                    state['descrip'].append(y['descrip'])
                    state['name'].append(y['name'])
                    print("Description:", y['descrip'])

    if narrow == 'number of steps':
        print("\n")
        for y in state['recipes']:
            for key in y['name']:
                if r == key:
                    state['information'].append(y['number_steps'])
                    state['number_steps'].append(y['number_steps'])
                    state['name'].append(y['name'])
                    print("This recipe has", y['number_steps'], "steps.")

    if narrow == 'time':
        print("\n")
        for y in state['recipes']:
            for key in y['name']:
                if r == key:
                    state['information'].append(y['time'])
                    state['time'].append(y['time'])
                    state['name'].append(y['name'])
                    print("This recipe takes", y['time'], "minutes.")

    if narrow == "step":
        print("\n")
        for y in state['recipes']:
            for key in y['name']:
                if r == key:
                    state['steps'].append(y['steps'])
                    state['name'].append(y['name'])
                    if "/" in y['steps']:
                        print("These are the steps: \n\n ", str(y['steps']).replace('/' , '\n'))
                    else:
                        print("These are the steps: \n\n ", str(y['steps']).replace(',' , '\n'))
    return render_template("information.html",state=state)

@app.route('/again',methods=['GET','POST'])
def again():
    global state
    print(state['ingred_list'])
    if again == "yes":
        print("\n")
        information()
    else:
        print("\n\nGood luck with your recipe! ツ")
    return render_template("again.html",state=state)




@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run('0.0.0.0',port=4000)
