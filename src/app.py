from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("user", usr=user))
    else:
        return render_template("home.html")
    
@app.route("/planner", methods = ["POST", "GET"])
def planner():
    if request.method == "POST":
        return redirect(url_for("user", usr=user))
    else:
        return render_template("planner.html")
    
@app.route("/to-do", methods = ["POST", "GET"])
def todo():
    if request.method == "POST":
        return redirect(url_for("user", usr=user))
    else:
        return render_template("to-do.html")
    
@app.route("/exercise", methods = ["POST", "GET"])
def exercise():
    if request.method == "POST":
        return redirect(url_for("user", usr=user))
    else:
        return render_template("exercise.html") 

@app.route("/<usr>")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("planner"))

if __name__ == "__main__":
    app.run(debug=True) 