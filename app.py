from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = "goatifi"
app.permanent_session_lifetime = timedelta(minutes=5)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'tasks.db')

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(20))
    finish = db.Column(db.String(20))

with app.app_context():
    db.create_all()


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
        name = request.form.get("name")
        start = request.form.get("start")
        finish = request.form.get("finish")
        
        if name:
            new_task = Task(name=name, start=start, finish=finish)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully", "info")
        else:
            flash("Task name is required", "error")
        return redirect(url_for("todo"))
   
    tasks = Task.query.all()
    return render_template("to-do.html", tasks=tasks)
    
@app.route("/exercise", methods = ["POST", "GET"])
def exercise():
    if request.method == "POST":
        activity_type = request.form.get("activity_type")
        start = request.form.get("start")
        finish = request.form.get("finish")

        if activity_type:
            new_task = Task(name=activity_type, start=start, finish=finish)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully", "info")
        else:
            flash("Missing activity type or time", "error")
        return redirect(url_for("exercise"))

    return render_template("exercise.html")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash(f"Task '{task.name}' deleted.", "info")
    return redirect(url_for("todo"))


if __name__ == "__main__":
    app.run(debug=True) 