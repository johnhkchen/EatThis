# Nutrition API 
# yK3Xwo3sLb4dDpntkqK1yyfYq6usk8kMaMrQBnxA
# Take string
# Make nutrition request

import requests
import json

def search(food):
    r = requests.get('https://api.nal.usda.gov/ndb/search/?format=json&q={}&sort=r&max=15&offset=0&ds=Standard%20Reference&api_key=yK3Xwo3sLb4dDpntkqK1yyfYq6usk8kMaMrQBnxA'.format(item))
    searchData = r.json()
    for food in searchData['list']['food']:
       print("{}: {}".format(food['ndbno'], food['name']))

def getTrackedVitamins():
    return ['Vitamin C', 'Vitamin E']

def getTrackedNutrients():
    return ['Energy', 'Carbohydrate', 'Protein', 'Fat']+getTrackedVitamins()

def getNutrientID(nutrientName):
    # Todo: fill out dict
    return {
        'Protein':'203',
        'Fat':'204',
        'Carbohydrate':'205',
        'Carbohydrates':'205',
        'Energy':'208',
        'Calories':'208',
        'Calcium':'301',
        'Iron':'303',
        'Potassium':'306',
        'Sodium':'307',
        'Vitamin E':'323',
        'Vitamin C':'401'
    }[nutrientName]

def isNumber(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def getNutritionData(food, nutrient_id):
    if not isNumber(nutrient_id):
        target = getNutrientID(nutrient_id)
    for nutrient in food['nutrients']:
        if nutrient['nutrient_id'] == target:
            return float(nutrient['value'])

def amountOf(nutrient, food, weight):
    # TODO: Manage weight when food is not in grams
    nutritionDensity = getNutritionData(food, nutrient)
    return nutritionDensity/100*weight

def foodInfo(ndbno):
    # Request food report using database ID
    r = requests.get('https://api.nal.usda.gov/ndb/reports/?ndbno={}&type=b&format=json&api_key=yK3Xwo3sLb4dDpntkqK1yyfYq6usk8kMaMrQBnxA'.format(ndbno))
    return r.json()['report']['food']

def nutritionalInfo(food, weight):
    if not isNumber(weight):
        weight = float(weight)

    nutritionInfo = dict()
    for nutrient in getTrackedNutrients():
        nutritionInfo[nutrient] = amountOf(nutrient, food, weight)
    return nutritionInfo

def initNutritionInfo():
    nutritionInfo = dict()
    for nutrient in getTrackedNutrients():
        nutritionInfo[nutrient] = 0
    return nutritionInfo

def addToInfo(subtotal, item):
    food = foodInfo(item['id'])
    weight = item['wt']
    nutrients = nutritionalInfo(food, weight)

    for nutrient in getTrackedNutrients():
        subtotal[nutrient] += nutrients[nutrient]
    return subtotal

def printVitamins(nutrients):
    print('\t', end='')
    for vitamin in getTrackedVitamins():
        print("{}: {} | ".format(vitamin, nutrients[vitamin]), end='')
    print()

def printMacros(nutrients):
    print("{:.0f} kcal ({:.1f}g carb/{:.1f}g protein/{:.1f}g fat)".format(nutrients['Energy'], nutrients['Carbohydrate'], nutrients['Protein'], nutrients['Fat']))

def printInfo(item):
    #  Todo: Define menu item details
    food = foodInfo(item['id'])
    weight = item['wt']
    nutrients = nutritionalInfo(food, weight)

    # Pull specific data: Energy, Protein, Carbohydrate, Fat, Vitamin C
    print("{}, {}g: ".format(food['name'], weight))
    print("\t", end='')
    printMacros(nutrients)

# Print menu nutrition
myFoods = ['Eggs', 'Bacon', 'Grits', 'Sausage']

myMenu = [{'id':'01128', 'wt':200}, {'id':'10860', 'wt':150}, {'id':'08165', 'wt':350}, {'id':'07074','wt':250}]

myNutrition = initNutritionInfo()
for food in myMenu:
    myNutrition = addToInfo(myNutrition, food)
    printInfo(food)

printMacros(myNutrition)
printVitamins(myNutrition)