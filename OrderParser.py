import re
from drinks import drink_list

def CheckTextVaildity(order):
    drinks = []
    drink_aliases = {}

    for name in drink_list:
        drinks.append(name['name'])
        # If you have aliases for drinks, add them here
        if name['name'].lower() == 'psl':
            drink_aliases['psl'] = 'PSL'
            drink_aliases['pumpkin spice latte'] = 'PSL'
            drink_aliases['pumpkin latte'] = 'PSL'

    print(drinks)
    
    # Regex to capture drink type and optional sweetener
    drink_pattern = r'\b(' + '|'.join(re.escape(drink.lower()) for drink in drinks) + r')\b'
    sweetener_pattern = r'\b(sweetener|sweet|with sweetener|with sweet)\b'  # Expand as needed

    order = order.lower()
    coffeetype = re.findall(drink_pattern, order, re.I)
    has_sweetener = re.search(sweetener_pattern, order, re.I)

    if len(coffeetype) > 1:
        print("Too many inputs")
        return None, False  # Or handle as needed

    matches = False
    drink = None
    if coffeetype:
        drink_key = coffeetype[0]
        # Check if the drink is an alias
        if drink_key in drink_aliases:
            drink = drink_aliases[drink_key]
        elif drink_key.capitalize() in drinks:
            drink = drink_key.capitalize()
        else:
            for value in drinks:
                if value.lower() == drink_key:
                    drink = value
                    break
        matches = drink is not None

    if matches:
        # For PSL, sweetener is always included
        if drink == "PSL":
            return drink, False  # No need to add extra sweetener
        else:
            return drink, has_sweetener is not None
    else:
        return None, False
