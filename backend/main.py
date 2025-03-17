import datetime

from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
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
    cigarettes = db.Column(db.Integer, default=0)
    last_smoked = db.Column(db.DateTime, default=None)
    monthly_cigarettes = db.Column(db.Integer, default=0)
    target_cigarettes = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Post('{self.name}', '{self.cigarettes}', '{self.last_smoked}')"




@app.route('/')
def index():
    return render_template("index.html", user=session.get("user"))


@app.route('/about')
def about():
    return render_template("about.html", user=session.get("user"))


@app.route('/donate')
def donat():
    return render_template("donate.html", user=session.get("user"))


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

        new_user = Post(name=name, password=password, cigarettes=0)

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


from datetime import datetime

@app.route('/smoking', methods=['GET', 'POST'])
def smoking():
    if not session.get("user"):
        return redirect(url_for('login'))

    username = session.get("user")
    user = Post.query.filter_by(name=username).first()

    if request.method == 'POST':
        puffs = request.form.get('puffs')
        try:
            puffs = int(puffs)
        except (ValueError, TypeError):
            error = "Пожалуйста, введите целое число для количества сигарет."
            return render_template('smoking.html', user=session.get("user"), error=error, **get_smoking_data(user))

        if puffs is not None and puffs >= 0:
            user.cigarettes = puffs
            now = datetime.utcnow()
            user.last_smoked = now

            # Проверяем, нужно ли начинать новый месяц
            if user.last_smoked is None or user.last_smoked.month != now.month:
                # Новый месяц, обнуляем счетчик
                user.monthly_cigarettes = puffs
            else:
                # Текущий месяц, добавляем к счетчику
                user.monthly_cigarettes += puffs

            db.session.commit()
            return redirect(url_for('smoking'))
        else:
            error = "Пожалуйста, введите корректное количество сигарет (неотрицательное число)."
            return render_template('smoking.html', user=session.get("user"), error=error, **get_smoking_data(user))

    return render_template("smoking.html", user=session.get("user"), **get_smoking_data(user))


def get_smoking_data(user):
    if user:
        # Количество сигарет до цели
        cigarettes_to_target = max(0, user.cigarettes - user.target_cigarettes)

        # Расчет среднего количества сигарет (упрощенный пример за последние 7 дней)
        # В реальном проекте потребуется хранить историю курения
        average_cigarettes = user.cigarettes  # Пока просто текущее значение

        # Процент прогресса (чем меньше сигарет, тем больше прогресс)
        progress = max(0, min(100, 100 - (user.cigarettes / 2)))  # Пример

        return {
            "current_cigarettes": user.cigarettes,
            "average_cigarettes": average_cigarettes,
            "target_cigarettes": user.target_cigarettes,
            "cigarettes_to_target": cigarettes_to_target,
            "progress": progress,
        }
    else:
        return {}





@app.route('/upgrade')
def upgrade():
    return render_template("UpGrade.html", user=session.get("user"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)