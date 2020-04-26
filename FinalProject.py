import csv
csv_recipes = list(csv.DictReader(open('RAW_recipes.csv','r'),delimiter=','))


print("Hi! Welcome to Quaratine Eats! Here, we will be helping you find recipes you can make with the limited ingredients you may have in the house.\n")
print("It may seem like certain things don't go together, but try inputting the ingredients you have and we'll see what recipes we can come up with!\n")
print("When inputting your ingredients, remember to please seperate them by commas with no spaces in between!\n\n")


ingred_list = str(input("Input your ingredients: "))

split_ingred = ingred_list.split(",")
print(split_ingred)
len(split_ingred)


matching_recipes = []
sorting = input("What is your priorities when finding a recipe? Would you like to sort this list by shortest amount of time to cook (a), smallest number of steps (b), or smallest number of ingredients (c)? ")

if sorting == 'a':
    sorting='time'
elif sorting == 'b':
    sorting = 'number_steps'
elif sorting == 'c':
    sorting = 'num_ingredients'

def iterate():
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
iterate()

def information():
    print("These are the top 5 recipes:\n")
    for y in matching_recipes[0:5]:
        for key in y['name']:
            print("»" + key)
    print("\n")

    narrow = input("Would you like to see the 'description', 'number of steps', 'time to prepare' or 'steps' for one of these recipes? ")
    print("\n")

    def selection():
        if narrow == 'description':
            r = input("Which recipe would you like to see the description of? Copy & paste the recipe here: ")
            print("\n")
            for y in matching_recipes:
                for key in y['name']:
                    if r == key:
                        print("Description:", y['descrip'])

        if narrow == 'number of steps':
            r = input("Which recipe would you like to see the amount of steps for? Copy & paste the recipe here:  ")
            print("\n")
            for y in matching_recipes:
                for key in y['name']:
                    if r == key:
                        print("This recipe has", y['number_steps'], "steps.")

        if narrow == 'time to prepare':
            r = input("Which recipe would you like to see the amount of time it takes in minutes? Copy & paste the recipe here: ")
            print("\n")
            for y in matching_recipes:
                for key in y['name']:
                    if r == key:
                        print("This recipe takes", y['time'], "minutes.")

        if narrow == 'steps':
            r = input("Which recipe would you like to see the steps for? Copy & paste the recipe here: ")
            print("\n")
            for y in matching_recipes:
                for key in y['name']:
                    if r == key:
                        if "/" in y['steps']:
                            print("These are the steps: \n\n ", str(y['steps']).replace('/' , '\n'))
                        else:
                            print("These are the steps: \n\n ", str(y['steps']).replace(',' , '\n'))
    selection()
    print("\n")

    again= input("Do you want to see any information on other recipes? yes or no? ").lower()
    if again == "yes":
        print("\n")
        information()
    else:
        print("\n\nGood luck with your recipe! ツ")
        quit()
information()
