from functools import wraps
from flask import Blueprint, Response, abort, current_app, jsonify, request
from flask_restx import Api, Resource , fields
from services.UserAuthService import UserAuthService
from services.AlertsService import AlertsService
from services.DetectionsService import DetectionsService

blueprint = Blueprint('api', __name__)
api = Api(blueprint, version='1.0', title='Detections API',
    description='Api that returns vehicle detections and alarms',
)

parser = api.parser()
parser.add_argument('X-Access-Token', help='Access token',location='headers')

resource_fields = api.model('Resource', {
    'user_id': fields.String,
    'password': fields.String
})

def token_required(f):
    @wraps(f)
    def decorator(self):
        if 'X-Access-Token' not in request.headers:
            abort(401)      
        
        token = request.headers['X-Access-Token']
        
        if not UserAuthService().is_token_valid(token):
            abort(401) 
        
        return f(self)
    return decorator


@api.route('/users')
@api.doc(description='Returns a new token for a valid combination of user_id/password')
class UsersEndpoint (Resource):
    @api.expect(resource_fields)
    @api.doc(responses={
        201: 'Created',
        400: 'Invalid request',
        401: 'Unauthorized Error'
    })
    def post(self):
        request_body = request.get_json()    
        
        if (request_body is None 
            or request_body.get('user_id') is None
            or request_body.get('password') is None):
            abort(400)
        
        token = UserAuthService().get_token(
            request_body.get('user_id'),
            request_body.get('password')
        )
        
        if token is None:
            abort(401)
        
        return Response(token, status=201, mimetype='application/text')

@api.route('/detections')
@api.header('X-Access-Token', 'Valid access token')
@api.expect(parser)
@api.doc(params={'skip': 'The number of registers that will be skiped in the response'})
@api.doc(params={'limit': 'The max number of registers that will be returned'})
@api.doc(description='Returns a list with vehicle detections according to skip and limit params')
class DetectionsEndpoint (Resource):
    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized Error'
    })
    @token_required
    def get(self):
        skip_param = request.args.get("skip", 0, int)  
        limit_param = request.args.get("limit", 0, int)
            
        detections = DetectionsService().get_detections(
            skip_param,
            limit_param
        )
        
        current_app.logger.debug ("Fetched Detections: %s", detections)
        return jsonify(detections)
    
@api.route('/stats')
@api.header('X-Access-Token', 'Valid access token')
@api.expect(parser)
@api.doc(description='Returns a list of vehicle detections quantity grouped by maker')
class StatsEndpoint (Resource):
    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized Error'
    })
    @token_required
    def get(self):
        detections_by_maker = DetectionsService().get_detections_by_maker()
        return jsonify(detections_by_maker)

@api.route('/alerts')
@api.header('X-Access-Token', 'Valid access token')
@api.doc(description='Returns SUV vehicles alerts in real time')
@api.expect(parser)
class AlertsEndpoint(Resource):
    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized Error'
    })
    @token_required
    def get(self):
        return Response(
            AlertsService().listen(), 
            mimetype="text/event-stream"
        )