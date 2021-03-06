# Developed by Jan Füsting and Tim Heimann

from flask import Flask
from flask_restplus import Resource, Api, fields
from bs4 import BeautifulSoup
import urllib.request


app = Flask(__name__)
api = Api(app)

ns = api.namespace('mensa', title='Mensa Microservice', description='This microservice returns the current menu')

# Models for export
menu_model = ns.model('MenuModel', {
        'Gericht': fields.String,
        'Student': fields.String,
        'Mitarbeiter': fields.String,
        'Gast': fields.String
        })

model = ns.model('Model', {
        'Tellergericht': fields.List(fields.Nested(menu_model)),
        'Komponente 1': fields.Nested(menu_model),
        'Komponente 2': fields.Nested(menu_model),
        'Nudeltheke': fields.Nested(menu_model),
        'Beilagen': fields.List(fields.Nested(menu_model)),
        'Gemüse': fields.List(fields.Nested(menu_model)),
        'Salate und Deserts': fields.Nested(menu_model)
        })


# Path and class to get Speiseplan JSON
@ns.route('/getter')
class Data(Resource):
    @ns.marshal_with(model)
    def get(self):
        # debug sites
        # ---------------------------
        # added notice
        # url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/?datum=2018-05-12'

        # normal day
        # url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/?datum=2018-05-18'

        # no data
        # url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/?datum=2018-05-21'
        # ---------------------------

        # Download current page
        url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/'
        text = urllib.request.urlopen(url).read().decode('utf-8')

        parsed_html = BeautifulSoup(text, "html.parser")
        result = parsed_html.body.findAll('table', attrs={'class': 'table module-food-table'})

        mensa_obj = {}

        # Parsing site
        for i in result:
            component = i.find_all('th')

            # Get name of stations and create empty array of objects
            mensa_obj[component[0].text.rstrip()] = []

            rows = i.find_all('tr')
            for row in rows:
                menu = row.find('td', attrs={'style': 'width:70%'})

                # Checks if station has food
                if not menu:
                    continue

                # Create object for meal
                menu_obj = {}
                menu_name = menu.text.split('(', 1)[0].split(' \n', 1)[0]
                menu_obj["Gericht"] = menu_name.replace("\r\n  ", "").rstrip()

                # Get prices for meal
                price = row.find_all('td', attrs={'class': 'hidden-xs', 'style': 'text-align:center'})
                pricelist = []
                for j in price:
                    pricelist.append(j.text.replace("\xa0€", ""))

                menu_obj["Student"] = pricelist[0]
                menu_obj["Mitarbeiter"] = pricelist[1]
                menu_obj["Gast"] = pricelist[2]

                mensa_obj[component[0].text.rstrip()].append(menu_obj)

        if not mensa_obj:
            # Couldn't parse information
            return None, 204
        else:
            # return parsed information
            return mensa_obj


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
