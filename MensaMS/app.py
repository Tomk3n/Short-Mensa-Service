from flask import Flask
from flask_restplus import Resource, Api, fields, marshal
from bs4 import BeautifulSoup
import urllib.request
import json

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)                         #  Create a Flask-RESTPlus API

ns = api.namespace('mensa', title='Mensa Microservice', description='This microservice returns the current menu')

menu_model = ns.model('menu_model', {
                'Gericht': fields.String,
                'Preise': fields.List(fields.String)
            })


@ns.route('/getter')
class Data(Resource):
    def get(self):
        # debug sites
        # ---------------------------
        # added notice
        # url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/?datum=2018-05-12'

        # normal day
        url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/?datum=2018-05-18'

        # no data
        # url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/?datum=2018-05-21'
        # ---------------------------

        # url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/'
        text = urllib.request.urlopen(url).read().decode('utf-8')

        parsed_html = BeautifulSoup(text, "html.parser")
        result = parsed_html.body.findAll('table', attrs={'class': 'table module-food-table'})

        string = []
        for i in result:
            element_result = []

            component = i.find_all('th')
            element_result.append(component[0].text)

            menu_list = []

            rows = i.find_all('tr')
            for row in rows:
                menu = row.find('td', attrs={'style':'width:70%'})

                if not menu:
                    continue

                menu_name = menu.text.split('(', 1)[0]
                # print(menu_name)

                menu_list.append(menu_name.replace("\r\n  ", "").replace("\xa0€", ""))

                price = row.find_all('td', attrs={'class':'hidden-xs', 'style':'text-align:center'})
                pricelist = []
                for j in price:
                    pricelist.append(j.text.replace("\xa0€", ""))

                    menu_list.append(pricelist)
            element_result.append(menu_list)
            string.append(element_result)

        for i in string:
            print(i)
            # print(json.dumps(string, indent=4))

        if not string:
            return None, 204
        else:
            return string
            #return json.dumps(marshal(string), indent=4)


    def serializer(self, data):

        return ""


if __name__ == '__main__':
    app.run()

