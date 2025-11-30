from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Користувач з таким ім’ям або email вже існує.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, role='client')
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна! Тепер ви можете увійти.', 'success')
        return redirect(url_for('auth.login'))

    # Вам потрібно створити auth/register.html у templates/
    return render_template('auth/register.html', title='Реєстрація')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Вхід успішний!', 'success')
            next_page = request.args.get('next') 
            # Перенаправляє на головну, якщо не було іншої сторінки
            return redirect(next_page or url_for('main.home')) 
        else:
            flash('Невірний логін або пароль.', 'danger')
            
    # Вам потрібно створити auth/login.html у templates/
    return render_template('auth/login.html', title='Вхід')

@auth_bp.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('main.home'))
