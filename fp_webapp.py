"""
  website_demo shows how to use templates to generate HTML
  from data selected/generated from user-supplied information
"""

from flask import Flask, render_template, request
app = Flask(__name__)

import csv
csv_recipes = list(csv.DictReader(open('RAW_recipes.csv','r'),delimiter=','))

import json

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
    state['none'] = []
    ingred_list=request.form['ingred_list']
    sorting=request.form['sorting']
    print(ingred_list)
    state['ingred_list']=ingred_list
    split_ingred = ingred_list.split(",")
    print(split_ingred)
    print(len(split_ingred))

    matching_recipes = []

    if sorting == 'amount_time':
        sorting='time'
    elif sorting == 'stepnumbers':
        sorting = 'number_steps'
    elif sorting == 'ingredientnumbers':
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
    n=0
    for y in matching_recipes[0:5]:
        state['recipes'].append(y)
        n+=1
        for key in y['name']:
            print("»" + key)
            state['recipe_names'].append(str(n)+". "+key)

    if len(matching_recipes) == 0:
        state['none'] = "There are no matching recipes. Sorry try again :(("
    elif len(matching_recipes) > 0:
        state['none'] = "Ta da!"
    print("\n")
    return render_template("submit.html",state=state)


@app.route('/information',methods=['GET','POST'])
def information():
    global state
    state['information']= []
    state['descrip'] = []
    state['number_steps'] = []
    state['time']= []
    state['steps'] = []
    state['in'] = []
    state['name'] = []
    state['hour'] = []
    print(state['ingred_list'])
    narrow=request.form['gender']
    state['narrow'] = narrow
    state['all'] = 'all'
    state['description'] = 'description'
    state['numsteps'] = 'number of steps'
    state['t'] = 'time'
    state['s'] = 'step'
    r=request.form['r']
    print(state['recipes'][int(r)-1])
    y=state['recipes'][int(r)-1]
    if narrow == 'all':
        print("\n")

        state['information'] = y
        a = y['name']
        b = y['ingred']
        b = b[0].strip('][').split(', ')
        b = [a.strip('\'') for a in b]
        b = [a.strip('\"') for a in b]
        print("after:",b)
        b=[a+","for a in b]
        c = y['descrip']
        d = y['number_steps']
        e = y['time']
        f = y['steps']
        f = f[0].strip('][').split(', ')
        f = [a.strip('\'') for a in f]
        f = [a.strip('\"') for a in f]
        f=[a+","for a in f]
        print("Description:", y['descrip'])
        print("This recipe has", y['number_steps'], "steps.")
        print("This recipe takes", y['time'], "minutes.")
        state['name'] = ' '.join(a)
        state['in'] = ' '.join(b)
        state['descrip'] = ' '.join(c)
        state['number_steps'] = ' '.join(d)
        state['time'] = ' '.join(e)
        state['steps'] = ' '.join(f)
        state['hour'] = int(state['time'])/60
        state['hour'] = str(round(state['hour'], 3))

    if narrow == 'description':
        print("\n")

        state['information'] = y['descrip']
        a = y['descrip']
        b = y['name']
        print("Description:", y['descrip'])

        state['descrip'] = ' '.join(a)
        state['name'] = ' '.join(b)

    if narrow == 'number of steps':
        print("\n")

        state['information'] = y['number_steps']
        a = y['number_steps']
        b = y['name']
        print("This recipe has", y['number_steps'], "steps.")
        state['number_steps'] = ' '.join(a)
        state['name'] = ' '.join(b)

    if narrow == 'time':
        print("\n")

        state['information'] = y['time']
        a = y['time']
        b = y['name']
        print("This recipe takes", y['time'], "minutes.")
        state['time'] = ' '.join(a)
        state['name'] = ' '.join(b)
        state['hour'] = int(state['time'])/60
        state['hour'] = str(round(state['hour'], 3))

    if narrow == "step":
        print("\n")
        a = y['steps']
        b = y['name']
        a = a[0].strip('][').split(', ')
        a = [a.strip('\'') for a in a]
        a = [a.strip('\"') for a in a]
        a=[a+","for a in a]
        if "/" in y['steps']:
            print("These are the steps: \n\n ", str(y['steps']).replace('/' , '\n'))
        else:
            print("These are the steps: \n\n ", str(y['steps']).replace(',' , '\n'))
        state['steps'] = ' '.join(a)
        state['name'] = ' '.join(b)
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
