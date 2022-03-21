from flask import Blueprint, current_app, jsonify, request

from services.DbService import DbService

blueprint = Blueprint('api', __name__)

@blueprint.route('/api/v1/users',methods=['POST'])
def post_users():
    return "users"

@blueprint.route('/api/v1/detections')
def get_detections():
    skip_param = request.args.get("skip")  
    limit_param = request.args.get("limit")
        
    detections = (
        DbService.get_db().detections.find()
        .skip (int(skip_param) if skip_param is not None else 0)
        .limit(int(limit_param) if limit_param is not None else 0)
    )
    
    detections = list(detections)
    [detection.pop("_id") for detection in detections]
    
    current_app.logger.debug ("Fetched Detections: %s", detections)
    return jsonify(detections)
    
@blueprint.route('/api/v1/stats')
def get_stats():
    return "stats"

@blueprint.route('/api/v1/alerts')
def get_alerts():
    return "alerts"