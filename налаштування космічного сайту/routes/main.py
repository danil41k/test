from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Вам потрібно створити index.html у templates/
    return render_template('index.html', title='Головна')

@main_bp.route('/about')
def about():
    # Вам потрібно створити about.html у templates/
    return render_template('about.html', title='Про нас')

@main_bp.route('/missions')
def missions():
    # Вам потрібно створити missions.html у templates/
    return render_template('missions.html', title='Актуальні Місії')

@main_bp.route('/planets')
def planets():
    # Вам потрібно створити planets.html у templates/
    return render_template('planets.html', title='Планети Сонячної Системи')
