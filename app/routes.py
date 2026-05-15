from flask import render_template, request, redirect, url_for, jsonify, flash, current_app as app
from app import db
from app.blueprints import main
from app.models import *
from app.forms import *
from flask_login import *
from werkzeug.security import *
from app.timecost import *
from datetime import date, timedelta
from sqlalchemy import func
from dateutil.relativedelta import relativedelta

#------------------ IMAGE IMPORT ------------------
import os
from werkzeug.utils import secure_filename


#------------------ SETTINGS ------------------
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
@main.route('/')
def index():
    return render_template('index.html', **get_user_settings_values())


# ------------------ LOGIN ------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and not form.validate_on_submit():
        errors = []
        for field_errors in form.errors.values():
            errors.extend(field_errors)

        return render_template(
            "login.html",
            form=form,
            error=errors[0] if errors else "Please check your login details"
        )

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            return render_template(
                "login.html",
                form=form,
                error="Email not found"
            )

        if not check_password_hash(user.password, form.password.data):
            return render_template(
                "login.html",
                form=form,
                error="Incorrect password"
            )
            
        login_user(user, remember=True)

        return redirect(url_for('main.index'))

    return render_template("login.html", form = form)


# ------------------ REGISTER ------------------
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if request.method == 'POST' and not form.validate_on_submit():
        errors = []
        for field_errors in form.errors.values():
            errors.extend(field_errors)

        return render_template(
            "register.html",
            form=form,
            error=errors[0] if errors else "Please check your registration details"
        )

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            return render_template(
                "register.html",
                form=form,
                error="Email is already registered"
            )

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            email=form.email.data,
            nickname=form.email.data.split('@', 1)[0],
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        if current_user.is_authenticated:
            logout_user()
            
        return redirect(url_for('main.login'))

    return render_template("register.html", form = form)


# ------------------ FORGOT PASSWORD ------------------
@main.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if request.method == 'POST' and not form.validate_on_submit():
        errors = []
        for field_errors in form.errors.values():
            errors.extend(field_errors)

        return render_template(
            "forgot_password.html",
            form=form,
            error=errors[0] if errors else "Please check your password reset details"
        )

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
@main.route("/dashboard")
@login_required
def dashboard():
    user = current_user

    tasks = Task.query.filter_by(user_id=user.id).all()

    total_tasks=len(tasks)
    done_tasks=sum(1 for t in tasks if t.status)

    avatar_form = profileform()

    analytics_tasks = db.session.query(
        TimerSession.taskforsession,
        (func.sum(TimerSession.timeCost) / 3600000).label('totalhrs'),
    ).filter(
        TimerSession.sessiondate >= (date.today() - timedelta(days=7)).isoformat(),
        TimerSession.user_id == current_user.id,
    ).group_by(TimerSession.taskforsession).all()

    chart_data = {
        "labels": [task.taskforsession for task in analytics_tasks],
        "data": [task.totalhrs for task in analytics_tasks]
    }

    return render_template("dashboard.html", 
    user=user,
    total_tasks=total_tasks,
    done_tasks=done_tasks,
    avatar_form=avatar_form,
    chart_data=chart_data)


# ------------------ LOGOUT ------------------
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


# ------------------ LEADERBOARD ------------------
@main.route("/leaderboard")
@login_required
def leaderboard():
    period = request.args.get('period', 'week')
    if period not in ('day', 'week', 'month'):
        period = 'week'

    users = get_leaderboard(period)

    return render_template(
        "leaderboard.html",
        users=users,
        period=period,
    )


# ------------------ TASK SYSTEM ------------------
@main.route('/get_tasks', methods=['GET'])
@login_required
def get_tasks():
    taskdate = request.args.get('taskdate')
    tasks = Task.query.filter_by(user_id=current_user.id, taskdate=taskdate).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content, "status": t.status} for t in tasks]
    })

# get tasks history and add back to todays task
@main.route('/task_history', methods=['GET'])
@login_required
def task_history():
    tasks = (
        Task.query
        .filter_by(user_id=current_user.id)
        .order_by(Task.taskdate.desc(), Task.id.desc())
        .all()
    )

    seen = set()
    history = []
    for t in tasks:
        key = t.content.strip().lower()  # Normalize the content for comparison
        if key not in seen:
            seen.add(key)
            history.append({
                "id" : t.id,
                "content": t.content,
            })

    return jsonify({
        "tasks": history
    })

@main.route('/add_task', methods=['POST'])
@login_required
def add_task():

    data = request.get_json()
    content = data.get('task')
    taskdate = data.get('taskdate')

    if content and taskdate:
        new_task = Task(content=content, 
                    user_id=current_user.id,
                    taskdate=taskdate)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(
        user_id=current_user.id, 
        taskdate=taskdate,
    ).all()

    return jsonify({
        "tasks": [{"id": t.id, "content": t.content, "status": t.status} for t in tasks]
    })


@main.route('/delete_tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_tasks(id):
    taskdate = request.args.get('taskdate')

    task = Task.query.filter_by(id=id, user_id=current_user.id).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=current_user.id, taskdate=taskdate).all()
    
    return jsonify({
        "tasks": [{"id": t.id, "content": t.content, "status": t.status} for t in tasks]
    })

# ------------------ STATUS ------------------
@main.route('/toggle_status/<int:id>', methods=['POST'])
@login_required

def toggle_status(id):
    taskdate = request.args.get('taskdate')

    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if task:
        task.status = not task.status
        db.session.commit()

    tasks = Task.query.filter_by(user_id=current_user.id, taskdate=taskdate).all()

    return jsonify(tasks=[{
        "id": t.id,
        "content": t.content,
        "status": t.status
    } for t in tasks])
    
# ------------------ TIMER ------------------
@main.route("/timer", methods = ['GET'])
@login_required

def timer():
    return render_template("timer.html", **get_user_settings_values())

#-------flow + pomodoro timer sessions commit to database------------------
@main.route("/sessiontimes", methods=['POST'])
@login_required
def sessiontimes():
    data = request.get_json()
    startTime = data.get('startTime')
    endTime = data.get('endTime')
    task = data['task']
    sessiondate = data['sessiondate']
    timeCost = data.get('timeCost')
    if timeCost is None:
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
@main.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data.strip()

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
        s.show_leaderboard = form.show_leaderboard.data

        db.session.commit()
        flash("Settings saved successfully")
        return redirect(url_for('main.index'))

    if request.method == 'GET':
        form.nickname.data = current_user.nickname
        current_settings = get_user_settings_values()
        user_settings = Settings.query.get(current_user.id)
        form.show_leaderboard.data = True if user_settings is None else user_settings.show_leaderboard
        form.flow_restratio.data = current_settings["flow_restratio"]
        form.pom_worklength.data = current_settings["pom_worklength"]
        form.pom_short_break.data = current_settings["pom_short_break"]
        form.pom_long_break.data = current_settings["pom_long_break"]

    return render_template("settings.html", form = form)

# ------------------ TIMERSESSION CAUCULATE ------------------
@main.route("/calculate", methods=['GET'])
@login_required
def calculate():
    sessiondate = request.args.get('sessiondate')
    sessionsum = db.session.query(
        db.func.sum(TimerSession.timeCost)).filter_by(
            user_id=current_user.id,
            sessiondate=sessiondate).first()
    today_total = sessionsum[0] or 0

    return jsonify({'sessiondate': sessiondate, 'today_total': today_total})

#-------------------- Task Cost ------------------
@main.route("/analytics", methods=['GET'])
@login_required
def analytics():
    period = request.args.get("period", "week")

    def findstartdate(period):
        if period == "day":
            return date.today().isoformat()
        elif period == "month":
            return (date.today() - relativedelta(months=1)).isoformat()
        else:
            return (date.today() - timedelta(days=7)).isoformat()
    start_date = findstartdate(period)

    def formatchartdata(start_date):
        tasks = db.session.query(
            TimerSession.taskforsession,
            (func.sum(TimerSession.timeCost) / 3600000).label('totalhrs'),
        ).filter(
            TimerSession.sessiondate >= start_date,
            TimerSession.user_id == current_user.id,
        ).group_by(TimerSession.taskforsession).all()

        chart_data = {
                "labels": [task.taskforsession for task in tasks],
                "data": [task.totalhrs for task in tasks]
            }
        return chart_data
    chart_data = formatchartdata(start_date)

    total_tasks = Task.query.filter_by(user_id=current_user.id).count()
    done_tasks = Task.query.filter_by(user_id=current_user.id, status=True).count()

    return render_template(
        "dashboard.html",
        user=current_user,
        total_tasks=total_tasks,
        done_tasks=done_tasks,
        avatar_form=profileform(),
        chart_data=chart_data,
        analytics_period=period
    )

# ------------------UPDATE AVATAR ------------------
@main.route("/update_avatar", methods=['POST'])
@login_required
def update_avatar():
    form = profileform()
    if form.validate_on_submit():
        avatar_file = form.avatar.data
        
        if avatar_file:
            filename = secure_filename(avatar_file.filename)
            # Set allowed file extensions
            extension = filename.rsplit('.',1)[1].lower()

            avatar_filename = f"user_{current_user.id}.{extension}"

            upload_folder= os.path.join(app.root_path, 'static', 'uploads','avatar')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            avatar_file.save(os.path.join(upload_folder, avatar_filename))

            current_user.avatar = f"uploads/avatar/{avatar_filename}"
            db.session.commit()

    return redirect(request.referrer or url_for('main.dashboard'))
