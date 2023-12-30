
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import os
import pytz
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"

# Create a socketio instance without initializing it
socketio = SocketIO()

# Factory function to create the Flask app
def create_app():
    app = Flask(__name__, static_folder='static')

    # Configure the app
    app.config['SECRET_KEY'] = '#$&^&^WYYDUHS&YWE'
    db_path = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_path, DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Define paths for file uploads
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/img/profile')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    EXCEL_FOLDER = os.path.join(app.root_path, 'static/excel')
    app.config['EXCEL_FOLDER'] = EXCEL_FOLDER

    # Initialize SQLAlchemy with the app
    db.init_app(app)
    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import Emp_login
    # User loader callback for LoginManager
    @login_manager.user_loader
    def load_user(id):
        return Emp_login.query.get(int(id))

    # Import and register blueprints
    from .auth import auth
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True

    # Import and initialize Flask-SocketIO with the app
    socketio.init_app(app)

    # Create the database if it doesn't exist
    create_database(app)

    return app


# Function to create the database if it doesn't exist
def create_database(app):
    if not os.path.exists(os.path.join(app.instance_path, DB_NAME)):
        with app.app_context():
            db.create_all()
        print('Created Database!')
