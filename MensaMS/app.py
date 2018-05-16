from flask import Flask
from flask_restplus import Resource, Api
from bs4 import BeautifulSoup
import urllib.request
import json

from pip.utils import encoding

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)                         #  Create a Flask-RESTPlus API

ns = api.namespace('mensa', description='Mensa Speiseplan Microservice')

@ns.route('/data')
class Data(Resource):
    def get(self):
        url = 'http://studwerk.fh-stralsund.de/essen/speiseplaene/mensa-stralsund/'
        text = urllib.request.urlopen(url).read().decode('utf-8')

        parsed_html = BeautifulSoup(text, "html.parser")
        result = parsed_html.body.findAll('table', attrs={'class': 'table module-food-table'})

        string = []
        for i in result:
            element_result = []
            menu = i.find('td', attrs={'style':'width:70%'}).text

            price = i.find_all('td', attrs={'class':'hidden-xs'})
            pricelist = []
            for j in price:
                pricelist.append(j.text.replace("\xa0€", ""))
                element_result.append(menu.replace("\r\n  ", "").replace("\xa0€", ""))
                element_result.append(pricelist)
            string.append(element_result)

        for i in string:
            print(i)
        return json.dumps(string, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    app.run()

