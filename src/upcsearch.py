import urllib.request
import json
import requests
from dotenv import load_dotenv
import os


def upcfunc(user_input):
    """Takes the barcode provided by the user and performs an api query

    :param user_input: takes barcode input from user
    :type user_input: str
    :returns: ingrdient list
    :rtype: str
    :raises ExceptionType: deals with HTTP 400,
     client side malformed request syntax
    """

    try:

        url = 'https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(user_input)

        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())

        item_ing = data.get('items')[0].get('description')
        item_ing = item_ing.lower()

        return item_ing

    except Exception:

        item_ing = "could not find provided barcode"

        return item_ing


def toxic_ingredients(ingredients):
    """Compares input to a database of known dog toxic ingredients

    :param ingredients: api output of ingredients as input
    :type ingredients: str
    :returns: returns innerjoin of ingredients input and a dictionary
    :rtype: str
    """

    load_dotenv()

    if not ingredients:

        display = "could not find provided barcode"

        return display

    else:
        url = "https://data.mongodb-api.com/app/data-gjrnb/endpoint/data/v1/action/find"
        payload = json.dumps({
        "collection": "toxic_items",
        "database": "doggesaver",
        "dataSource": "Cluster0",
        "projection": {
            "_id":0,
        }
    })
        headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': os.getenv("API_KEY"), 
        }

        response = requests.request("POST", url, headers=headers, data=payload,)
        response = response.json().get('documents')
        data = [rows.get('item') for rows in response]

        list_toxic = [x for x in data if x in ingredients]

        if not list_toxic:
            display = "does not contain dog toxic ingredients"
        else:
            display = "Dog toxic ingredients: "
            display += ','.join([str(item) for item in list_toxic])

    return display
