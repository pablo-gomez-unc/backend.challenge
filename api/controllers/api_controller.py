import json
from flask import Blueprint, Response, current_app, jsonify, request
from services.AlertsService import AlertsService
from services.DetectionsService import DetectionsService

blueprint = Blueprint('api', __name__)

@blueprint.route('/api/v1/users',methods=['POST'])
def post_users():
    return "users"

@blueprint.route('/api/v1/detections')
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
def get_stats():
    detections_by_maker = DetectionsService().get_detections_by_maker()
    return jsonify(detections_by_maker)

@blueprint.route('/api/v1/alerts')
def get_alerts():
    return Response(
        AlertsService().listen(), 
        mimetype="text/event-stream"
    )