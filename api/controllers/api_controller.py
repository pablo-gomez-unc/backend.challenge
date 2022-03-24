from functools import wraps
from flask import Blueprint, Response, abort, current_app, jsonify, request
from services.UserAuthService import UserAuthService
from services.AlertsService import AlertsService
from services.DetectionsService import DetectionsService

blueprint = Blueprint('api', __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'X-Access-Token' not in request.headers:
            abort(401)      
        
        token = request.headers['X-Access-Token']
        
        if not UserAuthService().is_token_valid(token):
            abort(401) 
        
        return f()
    return decorator

@blueprint.route('/api/v1/users',methods=['POST'])
def post_users():
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
    
    return jsonify(token)

@blueprint.route('/api/v1/detections')
@token_required
def get_detections():
    skip_param = request.args.get("skip", 0, int)  
    limit_param = request.args.get("limit", 0, int)
        
    detections = DetectionsService().get_detections(
        skip_param,
        limit_param
    )
    
    current_app.logger.debug ("Fetched Detections: %s", detections)
    return jsonify(detections)
    
@blueprint.route('/api/v1/stats')
@token_required
def get_stats():
    detections_by_maker = DetectionsService().get_detections_by_maker()
    return jsonify(detections_by_maker)

@blueprint.route('/api/v1/alerts')
@token_required
def get_alerts():
    return Response(
        AlertsService().listen(), 
        mimetype="text/event-stream"
    )