import os
from flask import Flask
from services.LoggingService import LoggingService
from controllers.ping_controller import blueprint as ping_controller
from controllers.api_controller import blueprint as api_controller
    
def create_app():
    app = Flask(__name__)
    
    LoggingService().set_logger(app.logger)
    
    app.register_blueprint(ping_controller)
    app.register_blueprint(api_controller)
    
    return app