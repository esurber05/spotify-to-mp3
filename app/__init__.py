from flask import Flask
from flask_socketio import SocketIO
from .config import Config

socketio = SocketIO()
from .routes.socketio_events import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from .routes.main_routes import main as main_blueprint
    from .routes.auth_routes import auth as auth_blueprint
    from .routes.download_routes import download as download_blueprint
    
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(download_blueprint)
    
    socketio.init_app(app, cors_allowed_origins="*")
    
    return app
