| UWA ID | Name | GitHub Username |
|--------------|------------------|-----------------|
| 24982075 | Haofei Wu        | haofei-wu       |
| 24284436     | Himakshi Nayyar  | Himakshi28      |
| 24245253     | Michael Jiang    | Sol1t4ry        |

# Study & Fitness Tracker App

A productivity app with a built-in timer that lets you track time completed for different tasks, see your personal analytics on time spent for each task, and a leaderboard to compare your aggregate task time to other users.

---

## User Stories

1. Creating an account As a new user. I want a straightforward sign-up process so that I can begin tracking my study sessions without unnecessary friction.
2. Studying without a fixed time limit. As someone whose focus varies day to day, I want a timer that counts up from zero rather than down from a preset duration, so that I can study for as long as I remain productive without feeling rushed or artificially constrained.
3. Taking a break proportional to my effort. As a user who has just completed a long focus block, I want my break length to scale with the time I just put in, so that my rest feels appropriately earned rather than arbitrary.
4. Using a structured timer when I need one. As a user who sometimes struggles to begin, I want the option to switch to a traditional Pomodoro format with fixed focus and break intervals, so that I have a reliable structure to fall back on when motivation is low.
5. Attributing sessions to specific tasks. As a student balancing multiple subjects, I want to label each session with the task I am working on, so that I can later understand how my time is distributed across my commitments.
6. Tracking trends across weeks and months As a user planning my study load, I want to see how my time is distributed across tasks over the past week or month, so that I can identify subjects I have neglected and rebalance my effort.
7. Comparing my progress with others, on my terms As a user motivated by friendly competition, I want the option to appear on a global leaderboard ranked by total study time, but I also want this disabled by default so that my data is never shared without my explicit consent.
8. Tailoring the app to my preferences As a user, I want to adjust settings such as my rest ratio, Pomodoro durations, long-break interval, and daily quote visibility, so that the app aligns with my personal study habits rather than forcing me to adapt to its defaults.

---

## Pages

| Page | Description |
|------|-------------|
| **Login** | User authentication |
| **Home** | Pomodoro/Flowmodoro Timers and Tasks |
| **Leaderboard** | Compare progress globally |
| **Dashboard/Analytics Page** | See your own progress for the last day, week or month |
| **Settings Page** | Customise your settings for timers, opt into leaderboard|



## How to Run

### Windows Powershell

```powershell
python -m venv venv
venv\scripts\activate

pip install -r requirements.txt

$env:FLASK_APP = "run.py"

flask db upgrade

python run.py // flask run
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=run.py

flask db upgrade

python run.py // flask run
```


