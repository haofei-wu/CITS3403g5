from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.models import *


def add_test_data_to_db():
    users = [
        User(
            email="A123@example.com", 
            nickname="A123", 
            password="password1"),
        User(
            email="B123@example.com", 
            nickname="B123", 
            password="password2"),
        User(
            email="C123@example.com", 
            nickname="C123", 
            password="password3"),
    ]
    db.session.add_all(users)
    db.session.commit()

    tasks = [
        Task(
            content="ABCDEF",
            user_id=users[0].id,
            taskdate="2026-05-13",
        ),
        Task(
            content="123456",
            user_id=users[0].id,
            taskdate="2026-05-12",
            status=True,
        ),
        Task(
            content="!@#$%%",
            user_id=users[1].id,
            taskdate="2026-05-05",
        ),
        Task(
            content="iiiiiiii",
            user_id=users[2].id,
            taskdate="2026-05-15",
        ),
    ]
    db.session.add_all(tasks)
    db.session.commit()
    sessions = [
        TimerSession(
            user_id=users[0].id,
            start_time=1000,
            end_time=3701000,
            taskforsession="ABCDEF",
            sessiondate="2026-05-13",
            timeCost=3700000,
        ),
        TimerSession(
            user_id=users[0].id,
            start_time=4000000,
            end_time=5800000,
            taskforsession="123456",
            sessiondate="2026-05-12",
            timeCost=1800000,
        ),
        TimerSession(
            user_id=users[1].id,
            start_time=1000,
            end_time=2401000,
            taskforsession="!@#$%%",
            sessiondate="2026-05-05",
            timeCost=2400000,
        ),
        TimerSession(
            user_id=users[2].id,
            start_time=1000,
            end_time=6100000,
            taskforsession="iiiiiiii",
            sessiondate="2025-04-15",
            timeCost=6099000,
        ),
    ]
    db.session.add_all(sessions)
    db.session.commit()

    settings = [
        Settings(
            id=users[0].id,
            flow_restratio=5,
            pom_worklength=25,
            pom_short_break=5,
            pom_long_break=15,
            show_leaderboard=True,
        ),
        Settings(
            id=users[1].id,
            flow_restratio=4,
            pom_worklength=30,
            pom_short_break=10,
            pom_long_break=20,
            show_leaderboard=False,
        ),
        Settings(
            id=users[2].id,
            flow_restratio=6,
            pom_worklength=45,
            pom_short_break=15,
            pom_long_break=30,
            show_leaderboard=True,
        ),  
    ]
    db.session.add_all(settings)
    db.session.commit()



class BasicTests(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()

        db.create_all()
        add_test_data_to_db()

        self.client = self.testApp.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

