from app import db

# The first argument defines the type of the column, then the rest you can defineoptional columns in any order after.
#foreign key references table name, not class name -> table name is tolower in the database automatically. 

# Foreign Key: db.Column(db.Integer, db.ForeignKey('tablename.primary_key_column'))
class User(db.Model):
    email = db.Column(db.String(120), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class TimerSession(db.Model):
    email = db.Column(db.Integer, db.ForeignKey('user.email'), primary_key=True, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)


class Tasks(db.Model):
    email = db.Column(db.Integer, db.ForeignKey('user.email'), primary_key=True, nullable=False)
    subjects = db.Column(db.String(128), nullable=False)




