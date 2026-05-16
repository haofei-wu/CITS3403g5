from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()

# Redirect to login page if user is not authenticated
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    # Load a user from the database for Flask-Login
    from app.models import User

    return User.query.get(int(user_id))

def create_app(config):

    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)

    db.init_app(flaskApp)
    migrate.init_app(flaskApp, db)
    csrf.init_app(flaskApp)
    login_manager.init_app(flaskApp)

    from app import routes
    from app.blueprints import main
    
    flaskApp.register_blueprint(main)

    return flaskApp
