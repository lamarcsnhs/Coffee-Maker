import re
from drinks import drink_list 
import json 


def CheckTextVaildity(order):
    drinks = []
    for name in drink_list:
        drinks.append(name['name'])

    print(drinks)
    
    # Regex to capture drink type and optional sweetener
    drink_string = r'\b(' + '|'.join(drinks) + r')\b'
    sweetener_string = r'\b(sweetener|sweet|with sweetener|with sweet)\b'  # Expand as needed

    coffeetype = re.findall(drink_string, order, re.I)
    has_sweetener = re.search(sweetener_string, order, re.I)

    if len(coffeetype) > 1:
        print("Too many inputs")

    matches = False
    for value in drinks:
        if coffeetype:
            if value == coffeetype[0]:
                matches = True
                break

    if matches:
        drink = value
        return drink, has_sweetener is not None
    else:
        return None, False

