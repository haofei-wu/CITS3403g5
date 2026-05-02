from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import Task

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')


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

@app.route('/tasks')
def tasks_page():
  return render_template('tasks.html')


# ------------------ LOGIN ------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_email'] = user.email
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", error="Incorrect password")

# ------------------ REGISTER ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return render_template("register.html", success=True)

        except IntegrityError:
            db.session.rollback()
            return render_template("register.html", error="Email already exists")

    return render_template("register.html")


# ------------------ FORGOT PASSWORD ------------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        return render_template("forgot_password.html", success=True)

    return render_template("forgot_password.html")


# ------------------ DASHBOARD ------------------
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    return render_template("dashboard.html", user=user)

# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


# ------------------ LEADERBOARD ------------------
@app.route("/leaderboard")
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    users = User.query.order_by(User.study_hours.desc()).all()
    top_users = users[:3]

    return render_template(
        "leaderboard.html",
        users=users,
        top_users=top_users
    )
