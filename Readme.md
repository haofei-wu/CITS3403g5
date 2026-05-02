# Study & Fitness Tracker App

A productivity app with a built-in timer that lets you track time studied and exercised, with social features including friends and a leaderboard.

---

## Features

- Logging study hours
As a student I want to be able to see my total hours studied and exercised, so I can see if I am working hard enough. 
- Pomodoro / Flowmodoro timer
As a student I want to use the pomodoro/flowmodoro techniquem, so I can stay productive over long periods of time. 
- Motivational quotes
As a student I want to feel motivated to work, so the latency of starting work is reduced. 
- Streaks for how many consecutive days you have studied/exercised
As a student I want to consistently work, so a streak system would encourage me to stay consistent in order to not break the streak. 
- Task management for current and next day via a timebox planner
- Google Calendar integration — push and pull tasks made in both apps
- Roll-over feature so that today's uncompleted tasks can be pushed to the next day
- Forgot password page 
- Friend Request 
- Small friend groups would be trolls. 
- Doing tasks -within. 
- Pop out page for timer
- Send task to time
- Gameify? 
- Working together as a group -> group page, timer on the page. How long u worked together with ecach other. Data transferred to eberyone (GROUP)
- Chat room on the homme page -> blurred out when studying
- Group project shared tasks, and add individuak ours, as well as a group timer.
-Multiple groups
- Leaderbaord add commments or reaction as support
- Task creation tool, and pull google calendar. 

-IMPROVE USER INTERACTON

-dont want ot encourage more study, just encourage consistency?

---

## Pages

| Page | Description |
|------|-------------|
| **Login** | User authentication |
| **Home** | Summary of everything done today, weekly hours, stats, and tasks to complete today |
| **Leaderboard** | Compare progress with friends |
| **Timer** | Pomodoro / Flowmodoro session timer |
| **Task Management** | Daily planner with timebox scheduling |

---

## Work Distribution

> Deadline: **25/03/26** — draft design (drawing) + HTML of all pages

| Page | Assignee |
|------|----------|
| Login | Himakshi |
| Leaderboard | Himakshi |
| Forgot password page | Himakshi |
| Timer | Haofei |
| Home | Michael |
| Task Management | Haofei + Michael |


## How to Run

```bash
python -m venv venv

venv\scripts\activate #window
source venv/bin/activate #Mac/Linux

#instal dependencies
pip install -r requirements.txt

#update database
flask db upgrade

flask run

