from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        return f"Logged in as {email}"  # temporary

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

        try:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return render_template("register.html", success=True)

        except IntegrityError:
            db.session.rollback()
            return render_template("register.html", error="Email already exists")

    return render_template("register.html")
