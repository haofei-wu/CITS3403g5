from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, db
from app.models import User, Task
from app.forms import LoginForm, RegisterForm, ForgotPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash


# ------------------ HOME ------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['user_email'] = user.email
            return redirect(url_for('dashboard'))

        return render_template("login.html", form=form, error="Invalid credentials")

    return render_template("login.html", form=form)


# ------------------ REGISTER ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html", form=form)


# ------------------ FORGOT PASSWORD ------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        return render_template("forgot_password.html", form=form, success=True)

    return render_template("forgot_password.html", form=form)


# ------------------ DASHBOARD ------------------
@app.route("/dashboard")
def dashboard():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_email'])
    return render_template("dashboard.html", user=user)


# ------------------ LOGOUT ------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


# ------------------ LEADERBOARD ------------------
@app.route("/leaderboard")
def leaderboard():
    users = User.query.all()
    top_users = []

    return render_template(
        "leaderboard.html",
        users=users,
        top_users=top_users
    )


# ------------------ TASK SYSTEM ------------------
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    if 'user_email' not in session:
        return jsonify({"tasks": []})

    user = User.query.get(session['user_email'])
    tasks = Task.query.filter_by(user_id=user.id).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


@app.route('/add_task', methods=['POST'])
def add_task():
    if "user_email" not in session:
        return jsonify({"error": "no login"}), 401
    
    user = User.query.get(session['user_email'])

    data = request.get_json()
    content = data.get('task')

    if content:
        new_task = Task(
            content=content,
            user_id=user.id
        )

        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=user.id).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
def delete_tasks(id):

    if 'user_email' not in session:
        return jsonify({"error": "no login"}), 401

    user = User.query.get(session['user_email'])

    task = Task.query.filter_by(id=id, user_id=user.id).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=user.id).all()
    
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


# ------------------ TIMER ------------------
@app.route("/timer")
def timer():
    return render_template("timer.html")

