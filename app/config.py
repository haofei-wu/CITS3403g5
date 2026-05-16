import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location ="sqlite:///" + os.path.join(basedir, "app.db")

class Config:
    # General Configurations
    SECRET_KEY = "cits3403"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_database_location

class TestConfig(Config):
    # Unit_Testing Configurations
    TESTING = True

    # Close WTF_CSRF protection for testing purposes
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY ="test3403"

class SeleniumTestConfig(TestConfig):
    # Selenium_Testing Configurations
    TESTING = True
    
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "selenium_test.db")
    SECRET_KEY ="seleniumtest3403"