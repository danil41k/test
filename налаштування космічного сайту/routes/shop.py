from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Product, Feedback, Order, OrderDetail
from flask_login import current_user, login_required

shop_bp = Blueprint('shop', __name__)

# ==========================================================
# ВІДГУКИ (CRUD: Create, Read)
# ==========================================================

@shop_bp.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        author = request.form.get('author')
        text = request.form.get('text')
        
        new_feedback = Feedback(author=author, text=text)
        db.session.add(new_feedback)
        db.session.commit()
        
        flash('Дякуємо за ваш відгук!', 'success')
        return redirect(url_for('shop.submit_feedback'))
    
    feedbacks = Feedback.query.order_by(Feedback.date_posted.desc()).all()
    # Вам потрібно створити feedback_form.html у templates/
    return render_template('feedback_form.html', title='Залишити Відгук', feedbacks=feedbacks)

# ==========================================================
# МАГАЗИН (Shop Logic)
# ==========================================================

@shop_bp.route('/shop')
def shop_index():
    products = Product.query.all()
    # Вам потрібно створити shop/index.html у templates/
    return render_template('shop/index.html', products=products)

# ==========================================================
# ІСТОРІЯ ЗАМОВЛЕНЬ (Рівень - Додаткова Функція)
# ==========================================================

@shop_bp.route('/orders/history')
@login_required # Доступно тільки залогіненим користувачам
def order_history():
    # Фільтруємо замовлення, які належать поточному користувачу
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    # Вам потрібно створити shop/order_history.html у templates/
    return render_template('shop/order_history.html', title='Історія Моїх Замовлень', orders=orders)
