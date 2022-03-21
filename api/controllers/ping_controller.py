from flask import Blueprint

blueprint = Blueprint('ping', __name__)

@blueprint.route('/ping')
def get_ping():
    return {'message': 'pong'}