from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# initiate login manager, and define to flask how to get current user id based on our models. 
login_manager = LoginManager(app)
#Redirect unauthenticated users to loginpage
login_manager.login_view = 'login'

#import models after db is initiated
from app.models import Task, User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#populates current_user object based on user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import routes