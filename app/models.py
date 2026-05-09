from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    #wait to hash
    password = db.Column(db.String(200), nullable=False)

    study_hours = db.Column(db.Float, default=0.0)

    #connection to Task table and lazyloading
    task = db.relationship('Task', backref='user', lazy=True)


class TimerSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    taskforsession_id = db.Column(db.ForeignKey('task.content'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Settings(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    flow_restratio = db.Column(db.Integer, nullable=False, default=5)
    pom_worklength = db.Column(db.Integer, nullable=False, default= 25)
    pom_short_break = db.Column(db.Integer, nullable=False, default= 5)
    pom_long_break = db.Column(db.Integer, nullable=False, default= 15)

# Initialise: python3 -m venv application-env
# .
# Activate: source application-env/bin/activate
# .











