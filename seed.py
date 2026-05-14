from app import create_app, db
from app.models import User, Task, TimerSession
from werkzeug.security import generate_password_hash
from datetime import date, timedelta
from app.config import Config

app = create_app(Config)
with app.app_context():
    db.drop_all()
    db.create_all()

    today = date.today()

    # ── users ────────────────────────────────────────────────
    alice = User(email="alice@test.com",
                 password=generate_password_hash("test123"), study_seconds=0)
    bob = User(email="bob@test.com",
               password=generate_password_hash("test123"), study_seconds=0)
    charlie = User(email="charlie@test.com",
                   password=generate_password_hash("test123"), study_seconds=0)
    dave = User(email="dave@test.com",
                password=generate_password_hash("test123"), study_seconds=0)
    db.session.add_all([alice, bob, charlie, dave])
    db.session.commit()

    # ── tasks ────────────────────────────────────────────────
    user_tasks = {
        alice:   ["CITS3403 project", "Fluids revision", "Dynamics tutorial",
                  "CITS1402 SQL", "Reading"],
        bob:     ["CITS1402 assignment", "Quantum notes", "Gym programming",
                  "Mandarin Anki", "Resume polish"],
        charlie: ["CITS3402 OpenMP", "Robotics RC car", "Fusion 360",
                  "Leetcode", "Eng dynamics"],
        dave:    ["Thesis reading", "Calculus revision", "Job applications",
                  "Side project", "Lecture catch-up"],
    }
    for user, tasks in user_tasks.items():
        for content in tasks:
            db.session.add(Task(
                content=content,
                user_id=user.id,
                taskdate=today.isoformat(),
            ))
    db.session.commit()

    # (user, task, days_ago, minutes)
    # Designed so:
    #   DAY (today)     winner = Alice  (burst studier)
    #   WEEK (0-6 days) winner = Bob    (consistent grinder)
    #   MONTH (0-29)    winner = Charlie (had a marathon 2-3 weeks ago)
    sessions_data = [
        # ── Alice: huge burst TODAY, otherwise quiet ──
        (alice, "CITS3403 project",  0, 120),
        (alice, "CITS3403 project",  0, 90),
        (alice, "Fluids revision",   0, 90),
        (alice, "Dynamics tutorial", 2, 30),
        (alice, "Reading",           8, 25),
        (alice, "CITS1402 SQL",     15, 30),
        (alice, "Reading",          22, 20),

        # ── Bob: steady every day this week ──
        (bob, "CITS1402 assignment", 0, 75),
        (bob, "CITS1402 assignment", 1, 80),
        (bob, "Quantum notes",       2, 70),
        (bob, "Gym programming",     3, 90),
        (bob, "Mandarin Anki",       4, 60),
        (bob, "Resume polish",       5, 75),
        (bob, "CITS1402 assignment", 6, 65),
        (bob, "Quantum notes",      14, 30),
        (bob, "Gym programming",    21, 40),

        # ── Charlie: was on fire weeks ago, slow now ──
        (charlie, "Leetcode",         0, 40),
        (charlie, "Eng dynamics",     4, 30),
        (charlie, "CITS3402 OpenMP", 14, 180),
        (charlie, "CITS3402 OpenMP", 15, 220),
        (charlie, "Robotics RC car", 16, 200),
        (charlie, "Fusion 360",      17, 160),
        (charlie, "Robotics RC car", 18, 190),
        (charlie, "Leetcode",        19, 150),
        (charlie, "Eng dynamics",    20, 180),

        # ── Dave: low-medium and consistent ──
        (dave, "Thesis reading",     0, 90),
        (dave, "Calculus revision",  1, 30),
        (dave, "Job applications",   2, 40),
        (dave, "Side project",       3, 35),
        (dave, "Lecture catch-up",   4, 45),
        (dave, "Thesis reading",     5, 30),
        (dave, "Calculus revision",  6, 40),
        (dave, "Side project",      10, 50),
        (dave, "Job applications",  14, 60),
        (dave, "Thesis reading",    18, 70),
        (dave, "Lecture catch-up",  24, 55),
    ]

    for user, content, days_ago, minutes in sessions_data:
        ms = minutes * 60 * 1000
        d = (today - timedelta(days=days_ago)).isoformat()
        db.session.add(TimerSession(
            user_id=user.id, taskforsession=content,
            start_time=0, end_time=ms, timeCost=ms, sessiondate=d,
        ))
    db.session.commit()

    print(f"seeded {User.query.count()} users, "
          f"{Task.query.count()} tasks, "
          f"{TimerSession.query.count()} sessions")