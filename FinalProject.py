import csv
csv_recipes = list(csv.DictReader(open('RAW_recipes.csv','r'),delimiter=','))

# print the first five lines
#print("This list has",len(csv_recipes),"items in it")
#csv_recipes[351]


print("Hi! Welcome to Quaratine Eats! Here, we will be helping you find recipes you can make with the limited ingredients you may have in the house.\n")
print("It may seem like certain things don't go together, but try inputting the ingredients you have and we'll see what recipes we can come up with!\n")
print("When inputting your ingredients, remember to please seperate them by commas with no spaces in between!\n\n")


ingred_list = str(input("Your ingredients?"))

split_ingred = ingred_list.split(",")
print(split_ingred)
len(split_ingred)




matching_recipes = []

for i in csv_recipes:
    matches = True
    for x in split_ingred:
        if x not in i['ingredients']:
            matches = False
    if matches:
        matching_recipes.append({'Name': [i['name']],'Description':[i['description']]})


print(matching_recipes)
