from flask import Flask
from flask_restplus import Resource, Api, reqparse

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)                         #  Create a Flask-RESTPlus API

ns = api.namespace('greeter', title='Greeter Microservice',
                    description='This microservice handles the greeting message.')

file = 'greeterMessage.txt'


# Handling messages
class Message(object):
    def get(self):
        fileContent = open(file, 'r')

        message = fileContent.read()

        fileContent.close()
        return message

    def set(self, data):
        fileContent = open(file, 'w')

        message = data

        fileContent.write(message)
        fileContent.close()
        return None, 204


# return message
@ns.route('/getter')
class Getter(Resource):
    def get(self):
        msg = Message()
        return {"message": msg.get()}


# set message
@ns.route('/setter')
@ns.param('payload', "Greeter message")
class Setter(Resource):
    def post(self, payload):
        msg = Message()
        return msg.set(payload)


if __name__ == '__main__':
    app.run()

