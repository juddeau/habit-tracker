from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///klient.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    password= db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/donat')
def donat():
    return render_template("donat.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("registration.html")

@app.route('/login')
def login():
    return render_template("entrance.html")


if __name__ == '__main__':

    app.run(debug=True)