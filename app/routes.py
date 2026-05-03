from flask import render_template, request, redirect, url_for, session
from app import app, db
from app.models import User

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
  tasks = Task.query.all()
  return jsonify({"tasks": [ {"id": task.id, "content": task.content} for task in tasks ]})

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    task_content = data.get('task')

    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.all()

    return jsonify({
        "tasks": [
            {"id": t.id, "content": t.content}
            for t in tasks
        ]
    })

@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
def delete_tasks(id):
  task_thing= Task.query.get(id)

  if task_thing:
    db.session.delete(task_thing)
    db.session.commit()

  tasks = Task.query.all()

  return jsonify({"tasks": [ {"id": task.id, "content": task.content} for task in tasks ]})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            # temporary simple check (since hashing may not be set up here)
            if user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route('/tasks')
def tasks_page():
  return render_template('tasks.html')

@app.route("/leaderboard")
def leaderboard():
    users = User.query.order_by(User.study_hours.desc()).all()
    top_users = users[:3]

    return render_template(
        "leaderboard.html",
        users=users,
        top_users=top_users
    )

@app.route("/timer")
def timer():
    return render_template("timer.html")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    return render_template("dashboard.html", user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        return render_template("forgot_password.html", success=True)

    return render_template("forgot_password.html")



