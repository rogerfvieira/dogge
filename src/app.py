from flask import Flask, render_template, request
from .upcsearch import upcfunc, toxic_ingredients


def create_app():
    """Displays web application for user to input upc and recieve results

    :returns:user webpage
    :rtype: HTML , CSS , PYTHON
    """

    APP = Flask(__name__)
    APP.static_folder = 'static'

    @APP.route('/')
    def form():
        """Displays homepage without user input

        :returns: HTML CSS page with empty input field
        :rtype: HTML , CSS , PYTHON
        """
        return render_template('index.html')

    @APP.route('/input', methods=['POST', 'GET'])
    def root():
        """Displays results of ingredient search and dog toxic ingredients
           comparison

        :returns: webpage with search results
        :rtype: HTML , CSS , PYHON , string
        """

        if request.method == 'GET':
            return render_template('index.html')

        if request.method == 'POST':

            user_upc = request.form.get('fname')
            ingredients_from_upc = upcfunc(user_upc)

            toxic_ingredients_list = toxic_ingredients(ingredients_from_upc)
            toxic = toxic_ingredients_list

            return render_template('index.html',
                                   ingredients=ingredients_from_upc,
                                   toxic=toxic)

    return APP
