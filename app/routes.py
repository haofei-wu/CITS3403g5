from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, db
from app.models import User, Tasks

# ------------------ HOME ------------------
@app.route('/')
def index():
    return redirect(url_for('login'))


# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_email'] = user.email   # ✅ important fix
            return redirect(url_for('dashboard'))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ------------------ REGISTER ------------------
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


# ------------------ FORGOT PASSWORD ------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        return render_template("forgot_password.html", success=True)

    return render_template("forgot_password.html")


# ------------------ DASHBOARD ------------------
@app.route("/dashboard")
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_email'])  # ✅ fix
    return render_template("dashboard.html", user=user)

# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


# ------------------ LEADERBOARD ------------------
@app.route("/leaderboard")
def leaderboard():
    users = User.query.order_by(User.study_hours.desc()).all()
    top_users = users[:3]

    return render_template(
        "leaderboard.html",
        users=users,
        top_users=top_users
    )


# ------------------ TASK SYSTEM ------------------
#@app.route('/get_tasks', methods=['GET'])
#def get_tasks():
    tasks = Task.query.all()
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


#@app.route('/add_task', methods=['POST'])
#def add_task():
    data = request.get_json()
    content = data.get('task')

    if content:
        new_task = Task(content=content)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.all()
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


#@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
#def delete_tasks(id):
    task = Task.query.get(id)

    if task:
        db.session.delete(task)
        db.session.commit()

    tasks = Task.query.all()
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


# ------------------ TIMER ------------------
@app.route("/timer")
def timer():
    return render_template("timer.html")
