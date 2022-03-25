from flask import Blueprint
from flask_restx import Api, Resource

blueprint = Blueprint('ping', __name__)
api = Api(blueprint, version='1.0', title='Detections api')

@api.route('/ping')
class ping (Resource) :
    def get(self):
        return {'message': 'pong'}