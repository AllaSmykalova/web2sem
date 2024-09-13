from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

# Flask-Session для сохранения сессий
Session(app)

# Flask-Login для аутентификации
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Для доступа к запрашиваемой странице необходимо пройти аутентификацию."

# Модель пользователя
class User(UserMixin):
    pass

# Словарь с данными пользователей
users = {
    'user': {'password': 'qwerty'},
    'alla': {'password': 'alla'},
}

# Поддержка загрузки пользователя для Flask-Login
@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница счётчика посещений
@app.route('/counter')
def counter():
    if 'visit_count' not in session:
        session['visit_count'] = 0
    session['visit_count'] += 1
    visit_count = session['visit_count']
    return render_template('counter.html', visit_count=visit_count)


# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form

        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user, remember=remember)
            flash('Вы успешно вошли!', 'success')

            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Неверный логин или пароль!', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# Страница выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы!', 'success')
    return redirect(url_for('index'))

# Секретная страница, доступная только аутентифицированным пользователям
@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)
