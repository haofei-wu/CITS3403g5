from app import db
from flask_login import UserMixin


# ------------------ USER ------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    # hashed password
    password = db.Column(
        db.String(200),
        nullable=False
    )

    # relationship to Task table
    task = db.relationship(
        'Task',
        backref='user',
        lazy=True
    )


# ------------------ TASK ------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(
        db.String(128),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )


# ------------------ TIMER SESSION ------------------
class TimerSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    start_time = db.Column(
        db.Integer,
        nullable=False
    )

    end_time = db.Column(
        db.Integer,
        nullable=False
    )

    taskforsession = db.Column(
        db.ForeignKey('task.content'),
        nullable=False
    )


# ------------------ USER SETTINGS ------------------
class Settings(db.Model):
    id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        nullable=False
    )

    flow_restratio = db.Column(
        db.Integer,
        nullable=False,
        default=5
    )

    pom_restratio = db.Column(
        db.Integer,
        nullable=False,
        default=5
    )

    pom_worklength = db.Column(
        db.Integer,
        nullable=False,
        default=25
    )
    