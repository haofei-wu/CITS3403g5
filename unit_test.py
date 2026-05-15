from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from app.routes import *

def add_test_data_to_db():
    users = [
        User(
            email="A123@example.com", 
            nickname="A123", 
            password=generate_password_hash("password1")),
        User(
            email="B123@example.com", 
            nickname="B123", 
            password=generate_password_hash("password2")),
        User(
            email="C123@example.com", 
            nickname="C123", 
            password=generate_password_hash("password3")),
        User(
            email="D123@example.com", 
            nickname="D123", 
            password=generate_password_hash("password4")),
        User(
            email="E123@example.com", 
            nickname="E123", 
            password=generate_password_hash("password5")),
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
            taskdate="2025-04-15",
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
    
    today = date.today()
    d123_sessions = [
        TimerSession(user_id=users[3].id, taskforsession="CITS3403 project",
                     start_time=0, end_time=7_200_000, timeCost=7_200_000,
                     sessiondate=today.isoformat()),                            # 120 min, today
        TimerSession(user_id=users[3].id, taskforsession="CITS3403 project",
                     start_time=0, end_time=5_400_000, timeCost=5_400_000,
                     sessiondate=today.isoformat()),                            #  90 min, today
        TimerSession(user_id=users[3].id, taskforsession="Fluids revision",
                     start_time=0, end_time=5_400_000, timeCost=5_400_000,
                     sessiondate=today.isoformat()),                            #  90 min, today
        TimerSession(user_id=users[3].id, taskforsession="Dynamics tutorial",
                     start_time=0, end_time=1_800_000, timeCost=1_800_000,
                     sessiondate=(today - timedelta(days=2)).isoformat()),      #  30 min, 2d ago
        TimerSession(user_id=users[3].id, taskforsession="Reading",
                     start_time=0, end_time=1_500_000, timeCost=1_500_000,
                     sessiondate=(today - timedelta(days=8)).isoformat()),      #  25 min, 8d ago
        TimerSession(user_id=users[3].id, taskforsession="CITS1402 SQL",
                     start_time=0, end_time=1_800_000, timeCost=1_800_000,
                     sessiondate=(today - timedelta(days=15)).isoformat()),     #  30 min, 15d ago
        TimerSession(user_id=users[3].id, taskforsession="Reading",
                     start_time=0, end_time=1_200_000, timeCost=1_200_000,
                     sessiondate=(today - timedelta(days=22)).isoformat()),     #  20 min, 22d ago
    ]
    db.session.add_all(d123_sessions)
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

    def login(self, email, password):
        return self.client.post('/login', data={
            "email":email,
            "password":password})

    

# ---------TASK TESTS--------------------
class TaskModelTest(BasicTests):

    #--------MODEL PART------
    def test_task_saved_correctly(self):
        task = Task.query.filter_by(content="ABCDEF").first()
        self.assertIsNotNone(task)
        self.assertEqual(task.content, "ABCDEF")
        self.assertFalse(task.status)
        self.assertEqual(task.taskdate, "2026-05-13")

    def test_task_user_relationship(self):
        user = User.query.filter_by(email="A123@example.com").first()
        task = Task.query.filter_by(content="ABCDEF").first()

        self.assertIsNotNone(user)
        self.assertIsNotNone(task)
        self.assertEqual(task.user_id, user.id)
    
    #--------ROUTE PART------
    def test_get_tasks(self):
        self.login("A123@example.com", "password1")

        response = self.client.get('/get_tasks?taskdate=2026-05-13')
        data = response.get_json()

        self.assertIn("tasks", data)
        self.assertEqual(len(data["tasks"]), 1)
        self.assertEqual(data["tasks"][0]["content"], "ABCDEF")
        self.assertFalse(data["tasks"][0]["status"])  
    
    def test_task_history(self):
        self.login("A123@example.com", "password1")

        response = self.client.get('/task_history')
        data = response.get_json()

        contents = [t["content"] for t in data["tasks"]]

        self.assertIn("ABCDEF", contents)
        self.assertIn("123456", contents)
        self.assertNotIn("!@#$%%", contents)
        self.assertNotIn("iiiiiiii", contents)

    def test_add_task(self):
        self.login("A123@example.com", "password1")

        response = self.client.post('/add_task', json={
            "task": "New Task Test",
            "taskdate": "2026-05-13"
        })

        task = Task.query.filter_by(content="New Task Test").first()

        self.assertIsNotNone(task)
        self.assertEqual(task.content, "New Task Test")
        self.assertEqual(task.taskdate, "2026-05-13")

    def test_delete_task(self):
        self.login("B123@example.com", "password2")

        task = Task.query.filter_by(content="!@#$%%").first()

        response = self.client.delete(f"/delete_tasks/{task.id}?taskdate=2026-05-05")
        #SQL recommand to instead of using Task.query.get(task.id)
        deleted_task = db.session.get(Task, task.id)

        self.assertIsNone(deleted_task)
    
    def test_toggle_task_status(self):
        self.login("B123@example.com", "password2")

        task = Task.query.filter_by(content="!@#$%%").first()
        self.assertFalse(task.status)

        response = self.client.post(f"/toggle_status/{task.id}?taskdate=2026-05-05")
        updated_task = db.session.get(Task, task.id)

        self.assertIsNotNone(updated_task)
        self.assertTrue(updated_task.status)


# ---------LOGIN & REGISTER TESTS--------------------
class AuthenTest(BasicTests):

    #--------LOGIN TESTS------
    def test_login_wrong_password(self):
        response = self.login("A123@example.com", "password_wrong")

        self.assertIn(b"Incorrect password", response.data)

    def test_login_wrong_email(self):
        response = self.login("wrong_email@example.com", "password1")

        self.assertIn(b"Email not found", response.data)

    #--------REGISTER TESTS------
    def test_register_success(self):
        response = self.client.post('/register', data={
            "email": "newuser@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword"
        })

        user = User.query.filter_by(email="newuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "newuser@example.com")
        self.assertEqual(user.nickname, "newuser")
        self.assertTrue(check_password_hash(user.password, "newpassword"))

    def test_register_exist_email(self):
        response = self.client.post('/register', data={
            "email": "A123@example.com",
            "password": "password1",
            "confirm_password": "password1"
        })

        self.assertIn(b"Email is already registered", response.data)

    def test_register_wrong_confirm(self):
        response = self.client.post('/register', data={
            "email": "newuser@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword_wrong"
        })

        self.assertIn(b"Passwords must match", response.data)

    #------------FORGET PASSWORD TESTS------
    def test_forgot_password_success(self):
        response = self.client.post('/forgot_password', data={
            "email": "A123@example.com",
            "new_password": "newpassword1",
            "confirm_password": "newpassword1"
        }) 
        user = User.query.filter_by(email="A123@example.com").first()
        self.assertIsNotNone(user)
        self.assertTrue(check_password_hash(user.password, "newpassword1"))
        self.assertIn(b"Password reset successfully", response.data)

    def test_forgot_password_wrong_email(self):
        response = self.client.post('/forgot_password', data={
            "email": "wrong_email@example.com",
            "new_password": "newpassword1",
            "confirm_password": "newpassword1"
        })

        self.assertIn(b"Email not found", response.data)

    def test_forgot_password_wrong_confirm(self):
        response = self.client.post('/forgot_password', data={
            "email": "A123@example.com",
            "new_password": "newpassword1",
            "confirm_password": "newpassword_wrong"
        })

        self.assertIn(b"Passwords must match", response.data)

#---------ANALYTICS TESTS--------------------
class AnalyticsTest(BasicTests):
    def setUp(self):
        super().setUp()                                  # parent BasicTests builds app/DB/client
        self.login("D123@example.com", "password4")      # then log in on top

    def test_startdate_week(self):
        start_date = findstartdate("week")
        self.assertEqual(start_date, (date.today() - timedelta(days=7)).isoformat())

    def test_startdate_month(self):
        start_date = findstartdate("month")
        self.assertEqual(start_date, (date.today() - relativedelta(months=1)).isoformat())

    def test_startdate_day(self):
        start_date = findstartdate("day")
        self.assertEqual(start_date, date.today().isoformat())

    def test_formatchartdataday(self):
        user = User.query.filter_by(email="D123@example.com").first()
        with self.testApp.test_request_context():
            login_user(user)
            chart_data = formatchartdata(findstartdate("day"))
        self.assertEqual(chart_data, {
            "labels": ["CITS3403 project", "Fluids revision"],
            "data": [3.5, 1.5]
        })

    def test_formatchartdataweek(self):
        user = User.query.filter_by(email="D123@example.com").first()
        with self.testApp.test_request_context():
            login_user(user)
            chart_data = formatchartdata(findstartdate("week"))
        self.assertEqual(chart_data, {
            "labels": ["CITS3403 project", "Fluids revision", "Dynamics tutorial"],
            "data": [3.5, 1.5, 0.5]
        })

    def test_formatchartdatamonth(self):
        user = User.query.filter_by(email="D123@example.com").first()
        with self.testApp.test_request_context():
            login_user(user)
            chart_data = formatchartdata(findstartdate("month"))
        self.assertEqual(chart_data, {
            "labels": ["CITS3403 project", "Fluids revision", "Dynamics tutorial", "Reading", "CITS1402 SQL"],
            "data": [3.5, 1.5, 0.5, 0.75, 0.5]
        })