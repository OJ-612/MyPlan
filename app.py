# Import required libraries
from flask import Flask, redirect, url_for, render_template, request, session, flash  # Flask framework tools
from datetime import timedelta  # For session lifetime
from flask_sqlalchemy import SQLAlchemy  # ORM to handle database
import os  # OS functions for file paths

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "goatifi"  # Secret key for sessions and flash messages
app.permanent_session_lifetime = timedelta(minutes=5)  # Sessions last 5 minutes

# Configure SQLite database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking overhead

# Ensure absolute path for database (cross-platform safe)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Directory of this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'tasks.db')

# Initialize database with SQLAlchemy
db = SQLAlchemy(app)

# Define Task model (represents a row in the database table)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each task
    name = db.Column(db.String(100), nullable=False)  # Task name (required)
    start = db.Column(db.String(20))  # Start time
    finish = db.Column(db.String(20))  # Finish time
    description = db.Column(db.String(100))  # Optional description

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# Helper to create database tables
def create_tables():
    db.create_all()

# Ensure the "description" column exists in Task table
with app.app_context():
    db.create_all()  # Create base table if missing

    # Check existing columns in Task table
    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(task)")
    cols = [row[1] for row in cursor.fetchall()]

    # Add description column if it doesn’t exist
    if "description" not in cols:
        cursor.execute("ALTER TABLE task ADD COLUMN description STRING")
        conn.commit()
    cursor.close()
    conn.close()

# ---------------- ROUTES ---------------- #

@app.route("/", methods=["POST", "GET"])
def home():
    """Home page route."""
    if request.method == "POST":
        # (Currently unused: would handle user form submission)
        return redirect(url_for("user", usr=user))
    else:
        # Render home page
        return render_template("home.html")
    
@app.route("/planner", methods=["GET"])
def planner():
    """Planner page - shows all tasks and allows selecting one for description view."""
    task_id = request.args.get("task_id")  # Get selected task ID from query string
    tasks = Task.query.order_by(Task.start).all()  # Fetch all tasks sorted by start time
    selected_task = None

    if task_id:
        selected_task = Task.query.get(task_id)  # Fetch the selected task

    return render_template("planner.html", tasks=tasks, selected_task=selected_task)
    
@app.route("/to-do", methods=["POST", "GET"])
def todo():
    """To-do page - allows adding and viewing tasks."""
    if request.method == "POST":
        # Collect form inputs
        name = request.form.get("name")
        start = request.form.get("start")
        finish = request.form.get("finish")
        description = request.form.get("description")
        
        # Validate and save new task
        if name:
            new_task = Task(name=name, start=start, finish=finish, description=description)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully", "info")  # Success message
        else:
            flash("Task name is required", "error")  # Error message
        return redirect(url_for("todo"))

    # GET request: show all tasks
    tasks = Task.query.all()
    return render_template("to-do.html", tasks=tasks)
    
@app.route("/exercise", methods=["POST", "GET"])
def exercise():
    """Exercise page - allows adding exercise tasks."""
    if request.method == "POST":
        # Collect form inputs
        activity_type = request.form.get("activity_type")
        start = request.form.get("start")
        finish = request.form.get("finish")

        # Validate and save new task
        if activity_type:
            new_task = Task(name=activity_type, start=start, finish=finish)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully", "info")
        else:
            flash("Missing activity type or time", "error")
        return redirect(url_for("exercise"))

    # GET request: render exercise form
    return render_template("exercise.html")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Delete a task by its ID."""
    task = Task.query.get_or_404(task_id)  # Fetch or return 404 if not found
    db.session.delete(task)  # Delete task
    db.session.commit()
    flash(f"Task '{task.name}' deleted.", "info")  # Show success message
    return redirect(url_for("todo"))

# Run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
 