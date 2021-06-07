from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# App configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# DB Models
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# Application routes
@app.route("/")
def hello_world():

    return "Hello, World!"


# Create Todo Item
@app.route("/home", methods=["GET", "POST"])
def home():
    todo = Todo()
    if request.method == "POST":
        # Form fields
        title = request.form["title"]
        desc = request.form["desc"]

        # Sending data to DB
        data = Todo(title=title, desc=desc)
        db.session.add(data)
        db.session.commit()

    display_records = todo.query.all()

    return render_template("index.html", data=display_records)


# Update Todo Item
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    if request.method == "POST":
        # Form fields
        item = Todo.query.filter_by(sno=id).first()
        item.title = request.form["title"]
        item.desc = request.form["desc"]

        # Sending updated data to DB
        db.session.add(item)
        db.session.commit()
        return redirect("/home")

    item = Todo.query.filter_by(sno=id).first()
    return render_template("update.html", data=item)


# Delete Todo Item
@app.route("/delete/<int:id>")
def delete(id):
    item = Todo.query.filter_by(sno=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/home")


# App Starter code
if __name__ == "__main__":
    app.run(debug=True, port=8000)
