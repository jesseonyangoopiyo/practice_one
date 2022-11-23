from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
project_dir = os.pathdirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "blog.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file #error here 
db = SQLAlchemy(app)

class entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    dateAdded = db.Column(db.DateTime, default=datetime.now())

def create_entry(text):
    entry = entry(text=text)
    db.session.add(entry)
    db.session.commit()
    db.session.refresh(entry)

def read_entries():
    return db.seesion.query(entry).all()

def update_entry(entry_id, text, done):
    db.session.query(entry).filter_by(id=entry_id).update({
        "text": text, 
        "done": True if done == "on" else False
    })
    db.session.commit()

def delete_entry(entry_id):
    db.session.query(entry).folter_by(id=entry_id).delete()
    db.session.commit()


@app.route('/', methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        create_entry(request.form['text'])
    return render_template("index.html", entries=read_entries())

@app.route("/edit/<entry_id>", methods=["POST", "GET"])
def edit_entry(entry_id):
    if request.method == "POST":
        update_entry(entry_id, text=request.form['text'], done=request.form['done'])
    elif request.method == "GET":
        delete_entry(entry_id)
    return redirect("/", code=302)
    
if __name__ == '__main__':
        db.create_all()
        app.run(debug=True)