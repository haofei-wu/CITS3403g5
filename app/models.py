from app import db
from flask_login import UserMixin
#rom sqlalchemy import DDL, event
# The first argument defines the type of the column, then the rest you can defineoptional columns in any order after.
#foreign key references table name, not class name -> table name is tolower in the database automatically. 

def default_nickname(context):
    email = context.get_current_parameters().get("email", "")
    return email.split("@", 1)[0] if "@" in email else "User"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), nullable=False, default=default_nickname)
    email = db.Column(db.String(120), unique=True, nullable=False)

    #wait to hash
    password = db.Column(db.String(200), nullable=False)
    study_seconds = db.Column(db.Integer, default=0)

    #connection to Task table and lazyloading
    task = db.relationship('Task', backref='user', lazy=True)
    avatar = db.Column(db.String(200), nullable=False, default="image/default.png")


class TimerSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    taskforsession = db.Column(db.ForeignKey('task.content'), nullable=False)
    sessiondate = db.Column(db.String(10), nullable=False)
    timeCost = db.Column(db.Integer, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    taskdate = db.Column(db.String(10), nullable=False)
    
# # trigger to automatically insert timecost into timer_session table after insert
# trigger = DDL("""
#     CREATE TRIGGER timeCostTrigger AFTER INSERT ON timer_session
#     FOR EACH ROW
#     BEGIN
#         UPDATE timer_session SET timeCost = (end_time - start_time)
#     WHERE id = NEW.id;
#     END;
# """)

# # 2. Attach it to the table using 'event'
# # This ensures it runs automatically during metadata.create_all()
# event.listen(TimerSession.__table__, 'after_create', trigger)
# dont need trigger, can do it server side in route. 

class Settings(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    flow_restratio = db.Column(db.Integer, nullable=False, default=5)
    pom_worklength = db.Column(db.Integer, nullable=False, default= 25)
    pom_short_break = db.Column(db.Integer, nullable=False, default= 5)
    pom_long_break = db.Column(db.Integer, nullable=False, default= 15)
    show_leaderboard = db.Column(db.Boolean, nullable=False, default=True)

# Initialise: python3 -m venv application-env
# .
# Activate: source application-env/bin/activate
# .











