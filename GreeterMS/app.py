from flask import Flask
from flask_restplus import Resource, Api, marshal, fields
import json

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)                         #  Create a Flask-RESTPlus API

ns = api.namespace('greeter', title='Greeter Microservice',
                    description='This microservice handles the greeting message.')

file = 'greeterMessage.txt'

model = ns.model('Model', {
        'message': fields.String
        })


# Handling messages
class Message(object):
    def get(self):
        file_content = open(file, 'r')

        message = file_content.read()

        file_content.close()
        return message

    def set(self, data):
        file_content = open(file, 'w')

        message = data

        file_content.write(message)
        file_content.close()
        return None, 204


# return message
@ns.route('/getter')
class Getter(Resource):
    @ns.marshal_with(model)
    def get(self):
        msg = Message()
        result = {}
        result['message'] = msg.get()
        return result


# set message
@ns.route('/setter/<string:payload>',
          methods=['POST'])
@ns.param('payload', 'Greeter message')
class Setter(Resource):
    def post(self, payload):
        msg = Message()
        return msg.set(payload)


if __name__ == '__main__':
    app.run()

