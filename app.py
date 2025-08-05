from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "goatifi"
app.permanent_session_lifetime = timedelta(minutes=5)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(20))
    finish = db.Column(db.String(20))

def create_tables():
    db.create_all()

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
        activity_type = request.form.get("activity_type")
        time = request.form.get("time")

        if activity_type and time:
            new_task = Task(name=activity_type, start=time)
            db.session.add(new_task)
            db.session.commit()
            flash(f"{activity_type} added at {time}", "info")
        else:
            flash("Missing activity type or time", "error")
        return redirect(url_for("exercise"))

    return render_template("exercise.html")

if __name__ == "__main__":
    app.run(debug=True) 