import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location ="sqlite:///" + os.path.join(basedir, "app.db")

class Config:
    SECRET_KEY = "cits3403"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_database_location