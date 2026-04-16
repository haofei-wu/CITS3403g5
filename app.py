from flask import Flask, render_template, request

# Create Flask app
app = Flask(__name__)

# Login page route
@app.route("/")
def login():
    return render_template("login.html")


# Forgot password route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        return f"Reset link sent to {email} (demo)"

    return render_template("forgot_password.html")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)