from flask import render_template, request, redirect, url_for, jsonify, flash
from app import app, db
from app.models import *
from app.forms import *
from flask_login import *

from werkzeug.security import *

DEFAULT_SETTINGS = {
    "flow_restratio": 5,
    "pom_worklength": 25,
    "pom_short_break": 5,
    "pom_long_break": 15
}


def get_user_settings_values():
    values = DEFAULT_SETTINGS.copy()

    if current_user.is_authenticated:
        user_settings = Settings.query.get(current_user.id)
        if user_settings:
            values.update({
                "flow_restratio": user_settings.flow_restratio,
                "pom_worklength": user_settings.pom_worklength,
                "pom_short_break": user_settings.pom_short_break,
                "pom_long_break": user_settings.pom_long_break
            })

    return values


# ------------------ HOME ------------------
@app.route('/')
def index():
    return render_template('index.html', **get_user_settings_values())


# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            
            login_user(user, remember=True)

            return redirect(url_for('index'))

    return render_template("login.html", form = form)


# ------------------ REGISTER ------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        #HASH PASSWORDS?

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html", form = form)


# ------------------ FORGOT PASSWORD ------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():

        user=User.query.filter_by(
            email=form.email.data
        ).first()

        if not user:
            return render_template(
                "forgot_password.html",
                form=form,
                error="Email not found"
            )
        
        user.password = generate_password_hash(form.new_password.data)
        db.session.commit()

        return render_template(
            "forgot_password.html",
            form=form,
            success="Password reset successfully",
        )    

    return render_template("forgot_password.html", form = form)


# ------------------ DASHBOARD ------------------
@app.route("/dashboard")
@login_required
@login_required
def dashboard():
    user = current_user

    tasks = Task.query.filter_by(user_id=user.id).all()

    total_tasks=len(tasks)
    done_tasks=sum(1 for t in tasks if t.status)

    return render_template("dashboard.html", user=user,total_tasks=total_tasks,done_tasks=done_tasks)


# ------------------ LOGOUT ------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    logout_user()
    return redirect(url_for('login'))


# ------------------ LEADERBOARD ------------------
@app.route("/leaderboard")
@login_required
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
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content, "status": t.status} for t in tasks]
    })


@app.route('/add_task', methods=['POST'])
@login_required
@login_required
def add_task():

    data = request.get_json()
    content = data.get('task')

    if content:
        new_task = Task(content=content, 
                    user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content, "status": t.status} for t in tasks]
    })


@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
@login_required
@login_required
def delete_tasks(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content, "status": t.status} for t in tasks]
    })

# ------------------ STATUS ------------------
@app.route('/toggle_status/<int:id>', methods=['POST'])
@login_required

def toggle_status(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    task.status = not task.status
    db.session.commit()

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return jsonify(tasks=[{
        "id": t.id,
        "content": t.content,
        "status": t.status
    } for t in tasks])
    
# ------------------ TIMER ------------------
@app.route("/timer", methods = ['GET'])
@login_required
def timer():
    return render_template("timer.html", **get_user_settings_values())

#can write inline if else in 

@app.route("/sessiontimes", methods=['POST'])
@login_required
def sessiontimes():
    data = request.get_json()
    startTime = data['startTime']
    endTime = data['endTime']
    task = data['task']
    sessiondate = data['sessiondate']
    timeCost = endTime - startTime
    new_session = TimerSession(user_id=current_user.id,
                               start_time=startTime,
                               end_time=endTime,
                               taskforsession=task,
                               sessiondate=sessiondate,
                               timeCost=timeCost)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'Session times committed successfully'})

# ------------------ SETTINGS ------------------
@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        #validation
        if form.pom_short_break.data >= form.pom_long_break.data:
            flash("Short break must be less than long break")
            return render_template("settings.html", form = form)

        s = Settings.query.get(current_user.id)

        if s is None:
            s = Settings(id=current_user.id)
            db.session.add(s)
        s.flow_restratio = form.flow_restratio.data
        s.pom_worklength = form.pom_worklength.data
        s.pom_short_break = form.pom_short_break.data
        s.pom_long_break = form.pom_long_break.data

        db.session.commit()
        flash("Settings saved successfully")
        return redirect(url_for('index'))

    if request.method == 'GET':
        current_settings = get_user_settings_values()
        form.flow_restratio.data = current_settings["flow_restratio"]
        form.pom_worklength.data = current_settings["pom_worklength"]
        form.pom_short_break.data = current_settings["pom_short_break"]
        form.pom_long_break.data = current_settings["pom_long_break"]

    return render_template("settings.html", form = form)

# ------------------ TIMERSESSION CAUCULATE ------------------
@app.route("/calculate", methods=['GET'])
@login_required
def calculate():
    sessiondate = request.args.get('sessiondate')
    sessionsum = db.session.query(
        db.func.sum(TimerSession.timeCost)).filter_by(
            user_id=current_user.id,
            sessiondate=sessiondate).first()
    today_total = sessionsum[0] or 0

    return jsonify({'sessiondate': sessiondate, 'today_total': today_total})