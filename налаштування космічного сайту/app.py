from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager
from models import db, User 
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.auth import auth_bp
from routes.main import main_bp

app = Flask(__name__)

# КОНФІГУРАЦІЯ
app.config['SECRET_KEY'] = 'ТВОЯ_СЕКРЕТНА_ФРАЗА_ЗАМІНИ_ЇЇ' # ВАЖЛИВО!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація бази даних
db.init_app(app)

# Ініціалізація Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
login_manager.login_message = 'Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки.'

@login_manager.user_loader
def load_user(user_id):
    """Функція завантаження користувача для Flask-Login."""
    return User.query.get(int(user_id))

# ==========================================================
# ІНІЦІАЛІЗАЦІЯ ТАБЛИЦЬ ТА АДМІН-КОРИСТУВАЧА
# ==========================================================

with app.app_context():
    db.create_all() 
    
    # Створення першого адміна, якщо його немає
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', email='admin@space.com', role='admin')
        admin_user.set_password('admin_password') # !!! ЗАМІНІТЬ ПАРОЛЬ !!!
        db.session.add(admin_user)
        db.session.commit()
        print("Створено адміністратора: admin / admin_password")

# ==========================================================
# РЕЄСТРАЦІЯ BLUEPRINT
# ==========================================================

app.register_blueprint(main_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)

# Запуск
if __name__ == '__main__':
    app.run(debug=True)
