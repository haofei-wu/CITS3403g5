from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    content = db.Column(db.String(128), nullable=False)
