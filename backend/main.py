from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///klient.db'
app.config['SECRET_KEY'] = 'you_son_materi'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/donat')
def donat():
    return render_template("donat.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    feck_zag = 0
    feck_pro = 0
    feck_chi = 0

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        two_password = request.form['two_password']

        for i in range(len(password)):
            if password[i].isupper():
                feck_zag = 1

        for i in range(len(password)):
            if password[i].islower():
                feck_pro = 1

        for i in range(len(password)):
            if password[i].isdigit():
                feck_chi = 1

        if password != two_password:
            return 'Пароли не совпадают'

        elif len(password) < 8:
            return 'Длина пароля слишком маленькая'

        elif len(password) > 40:
            return 'Длина пароля слишком большая'

        elif feck_zag == 0:
            return 'В пароле не содержится заглавная буква'

        elif feck_pro == 0:
            return 'В пароле не содержится прописная буква'

        elif feck_chi == 0:
            return 'В пароле не содержится цифра'

        with app.app_context():  # Важно: Используем контекст приложения
            existing_user = Post.query.filter_by(name=name).first()
            if existing_user:
                return "Имя пользователя уже занято"

        post = Post(name=name, password=password)
        try:
            with app.app_context():
                db.session.add(post)
                db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return render_template('registration.html')
    else:
        return render_template("registration.html")

@app.route('/login')
def login():
    return render_template("entrance.html")

# Добавленные маршруты
@app.route('/smoking')
def smoking():
    return render_template("smoking.html")

@app.route('/upgrade')
def upgrade():
    return render_template("UpGrade.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)