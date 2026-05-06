from flask import render_template, request, redirect, url_for, jsonify, flash
from app import app, db
from app.models import User, Task, Settings
from app.forms import (
    LoginForm,
    RegisterForm,
    ForgotPasswordForm,
    SettingsForm
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required
)


# ------------------ HOME ------------------
@app.route('/')
def index():
    return redirect(url_for('login'))


# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user, remember=True)

            return redirect(url_for('dashboard'))

        return render_template(
            "login.html",
            form=form,
            error="Invalid credentials"
        )

    return render_template(
        "login.html",
        form=form
    )


# ------------------ REGISTER ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(
            form.password.data
        )

        new_user = User(
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template(
        "register.html",
        form=form
    )


# ------------------ FORGOT PASSWORD ------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():

    form = ForgotPasswordForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user:

            user.password = generate_password_hash(
                form.new_password.data
            )

            db.session.commit()

            return render_template(
                "forgot_password.html",
                form=form,
                success="Password updated successfully!"
            )

        return render_template(
            "forgot_password.html",
            form=form,
            error="Email not found"
        )

    return render_template(
        "forgot_password.html",
        form=form
    )


# ------------------ DASHBOARD ------------------
@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        user=current_user
    )


# ------------------ LOGOUT ------------------
@app.route("/logout")
@login_required
def logout():

    logout_user()

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
@login_required
def get_tasks():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify({
        "tasks": [
            {
                "id": t.id,
                "content": t.content
            }
            for t in tasks
        ]
    })


@app.route('/add_task', methods=['POST'])
@login_required
def add_task():

    data = request.get_json()

    content = data.get('task')

    if content:

        new_task = Task(
            content=content,
            user_id=current_user.id
        )

        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify({
        "tasks": [
            {
                "id": t.id,
                "content": t.content
            }
            for t in tasks
        ]
    })


@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_tasks(id):

    task = Task.query.filter_by(
        id=id,
        user_id=current_user.id
    ).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify({
        "tasks": [
            {
                "id": t.id,
                "content": t.content
            }
            for t in tasks
        ]
    })


# ------------------ TIMER ------------------
@app.route("/timer")
def timer():
    return render_template("timer.html")


# ------------------ SETTINGS ------------------
@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():

    form = SettingsForm()

    if form.validate_on_submit():

        s = Settings.query.get(current_user.id)

        if s is None:
            s = Settings(id=current_user.id)
            db.session.add(s)

        s.flow_restratio = form.flow_restratio.data
        s.pom_restratio = form.pom_restratio.data
        s.pom_worklength = form.pom_worklength.data

        db.session.commit()

        flash("Settings saved successfully")

        return redirect(url_for('settings'))

    return render_template(
        "settings.html",
        form=form
    )
