import os
from flask import Flask
from controllers.ping_controller import blueprint as ping_controller
from controllers.swagger_controller import blueprint as swagger_controller
from controllers.api_controller import blueprint as api_controller
    
def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(ping_controller)
    app.register_blueprint(swagger_controller)
    app.register_blueprint(api_controller)
    
    return app