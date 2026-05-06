from flask import render_template, request, redirect, url_for, session, jsonify, flash
from app import app, db
from app.models import *
from app.forms import *
from flask_login import login_user, current_user
# ------------------ HOME ------------------
@app.route('/')
def index():
    return render_template('index.html')


# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['user_email'] = user.email
            login_user(user, remember=True)

            return redirect(url_for('index'))

    return render_template("login.html", form = form)


# ------------------ REGISTER ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(email=form.email.data, 
                        password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html", form = form)


# ------------------ FORGOT PASSWORD ------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        return render_template("forgot_password.html", success=True)

    return render_template("forgot_password.html", form = form)


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
    users = User.query.order_by(User.study_hours.desc()).all()
    top_users = users[:3]

    return render_template(
        "leaderboard.html",
        users=users,
        top_users=top_users
    )


# ------------------ TASK SYSTEM ------------------
@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return jsonify({"tasks": []})

    tasks = Task.query.filter_by(user_id=session['user_id']).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


@app.route('/add_task', methods=['POST'])
def add_task():
    print(session.get('user_id'))
    if "user_id" not in session:
        return jsonify({"error": "no login"}), 401
    
    data = request.get_json()
    content = data.get('task')

    if content:
        new_task = Task(content=content, 
                    user_id=session['user_id'])

        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
def delete_tasks(id):

    task = Task.query.filter_by(id=id, user_id=session['user_id']).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content} for t in tasks]
    })


# ------------------ TIMER ------------------
@app.route("/timer")
def timer():
    return render_template("timer.html")

# ------------------ SETTINGS ------------------
@app.route("/settings", methods=['GET', 'POST'])
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

    return render_template("settings.html", form = form)