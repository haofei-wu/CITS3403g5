from app import db

# The first argument defines the type of the column,
# then the rest define optional properties.

# Foreign Key:
# db.Column(db.Integer, db.ForeignKey('tablename.primary_key_column'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    # hashed password
    password = db.Column(db.String(200), nullable=False)

    # connection to Task table
    task = db.relationship('Task', backref='user', lazy=True)


# Unimplemented features:
# class TimerSession(db.Model):
#     email = db.Column(
#         db.String(120),
#         db.ForeignKey('user.email'),
#         primary_key=True,
#         nullable=False
#     )
#
#     start_time = db.Column(db.Integer, nullable=False)
#     end_time = db.Column(db.Integer, nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(128), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    