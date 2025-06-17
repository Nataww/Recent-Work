from flask import Flask
from app.config import Config
from flask_login import LoginManager
import os
from flask_session import Session

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = os.urandom(24)
    
    # Session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')
    app.config['SESSION_USE_SIGNER'] = True
    

    Session(app)
    

    login_manager.init_app(app)
    
    # Blueprints
    from app.routes import main, auth, files
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(files)
    
    return app
