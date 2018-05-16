from flask import Flask, Request
from flask_restplus import Resource, Api

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)                         #  Create a Flask-RESTPlus API

ns = api.namespace('greeter', description='Greeter Microservice')

@ns.route('/data')
class Data(Resource):
    def get(self):
        file = 'greeterMessage.txt'
        fileContent = open(file, 'r')
        message = fileContent.read()
        fileContent.close()

        return {"message": message}


@ns.route('/set')
class Setter(Resource):
    def post(self):
        file = 'greeterMessage.txt'
        fileContent = open(file, 'w')

        args = Request.args

        fileContent.write()
        fileContent.close()

        return None, 204


if __name__ == '__main__':
    app.run()

