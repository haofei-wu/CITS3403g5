from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, redirect, url_for

app = Flask(__name__)
app.secret_key = "Himakshi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    study_hours = db.Column(db.Float, default=0)

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
               return render_template("login.html", success="Login successful!")
            else:
                return render_template("login.html", error="Incorrect password")
        else:
            return render_template("login.html", error="User not found")

    return render_template("login.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")

        # TEMPORARY (for now)
        return render_template("forgot_password.html", success=True)

    return render_template("forgot_password.html")
from sqlalchemy.exc import IntegrityError

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
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template("dashboard.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))
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


