from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Definition
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

# Create Database Tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables created!")
    except Exception as e:
        print(f"Error creating database: {e}")

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/show")
def show_todos():
    alltodo = Todo.query.all()  # Retrieve all todos
    return render_template("show.html", alltodo=alltodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update_todos(sno):
    todo = Todo.query.get_or_404(sno)  # Automatically raises 404 if not found
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to home after update
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:sno>', methods=['GET'])
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if not todo:  # Handle missing record
        return "Record not found", 404
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))  # Redirect back to home after deleting

# Run Application
if __name__ == "__main__":
    app.run(debug=True)
