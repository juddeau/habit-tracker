from flask import Flask, render_template, request, flash, redirect, url_for, session
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
    return render_template("index.html", user=session.get("user"))


@app.route('/about')
def about():
    return render_template("about.html", user=session.get("user"))


@app.route('/donat')
def donat():
    return render_template("donat.html", user=session.get("user"))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        two_password = request.form['two_password']

        if password != two_password:
            flash('❌ Пароли не совпадают.', 'danger')
            return redirect(url_for('register'))

        if len(password) < 8:
            flash('❌ Пароль слишком короткий (мин. 8 символов).', 'danger')
            return redirect(url_for('register'))

        if not any(char.isupper() for char in password):
            flash('❌ Пароль должен содержать хотя бы одну ЗАГЛАВНУЮ букву.', 'danger')
            return redirect(url_for('register'))

        if not any(char.islower() for char in password):
            flash('❌ Пароль должен содержать хотя бы одну строчную букву.', 'danger')
            return redirect(url_for('register'))

        if not any(char.isdigit() for char in password):
            flash('❌ Пароль должен содержать хотя бы одну цифру.', 'danger')
            return redirect(url_for('register'))

        existing_user = Post.query.filter_by(name=name).first()
        if existing_user:
            flash("❌ Имя пользователя уже занято.", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        new_user = Post(name=name, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user'] = name  # Сохраняем пользователя в сессии
            flash("✅ Регистрация успешна! Добро пожаловать, " + name, "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('❌ Ошибка при регистрации, попробуйте снова.', 'danger')
            return redirect(url_for('register'))

    return render_template("registration.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        user = Post.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.name
            flash("✅ Успешный вход! Добро пожаловать, " + name, "success")
            return redirect(url_for('index'))
        else:
            flash('❌ Неверное имя пользователя или пароль.', 'danger')

    return render_template("entrance.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("✅ Вы вышли из аккаунта.", "info")
    return redirect(url_for('index'))


# Добавленные маршруты
@app.route('/smoking')
def smoking():
    return render_template("smoking.html", user=session.get("user"))


@app.route('/upgrade')
def upgrade():
    return render_template("UpGrade.html", user=session.get("user"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)