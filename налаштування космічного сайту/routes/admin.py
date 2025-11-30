from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user 
from functools import wraps 
from models import db, Feedback, Product, Order, OrderDetail, Client, User 

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# !!! ДЕКОРАТОР ДЛЯ ПЕРЕВІРКИ РОЛІ АДМІНІСТРАТОРА !!!
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ заборонено: потрібні права адміністратора.', 'danger')
            return redirect(url_for('auth.login')) 
        return f(*args, **kwargs)
    return decorated_function
# --------------------------------------------------

# ==========================================================
# АДМІН-ПАНЕЛЬ (Dashboard)
# ==========================================================

@admin_bp.route('/')
@login_required 
@admin_required 
def dashboard():
    feedback_count = db.session.query(Feedback).count()
    product_count = db.session.query(Product).count()
    order_count = db.session.query(Order).count()
    client_count = db.session.query(Client).count()
    # Вам потрібно створити admin/dashboard.html у templates/
    return render_template('admin/dashboard.html', title='Адмін-панель',
                           fb_count=feedback_count, prod_count=product_count, 
                           ord_count=order_count, client_count=client_count)

# ==========================================================
# КЕРУВАННЯ ВІДГУКАМИ (Feedback CRUD)
# ==========================================================

@admin_bp.route('/feedback')
@login_required 
@admin_required 
def manage_feedback():
    feedbacks = Feedback.query.order_by(Feedback.date_posted.desc()).all()
    # Вам потрібно створити admin/feedback.html у templates/
    return render_template('admin/feedback.html', title='Керування Відгуками', feedbacks=feedbacks)

@admin_bp.route('/feedback/delete/<int:id>', methods=['POST'])
@login_required 
@admin_required 
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    flash(f'Відгук #{id} видалено.', 'success')
    return redirect(url_for('admin.manage_feedback')) 

# ==========================================================
# КЕРУВАННЯ КЛІЄНТАМИ (Clients CRUD - Рівень 2)
# ==========================================================

@admin_bp.route('/clients')
@login_required 
@admin_required 
def manage_clients():
    clients = Client.query.all()
    # Вам потрібно створити admin/clients.html у templates/
    return render_template('admin/clients.html', title='Керування Клієнтами', clients=clients)

# ==========================================================
# КЕРУВАННЯ ТОВАРАМИ (Products CRUD)
# ==========================================================

@admin_bp.route('/products')
@login_required 
@admin_required 
def manage_products():
    products = Product.query.all()
    # Вам потрібно створити admin/products.html у templates/
    return render_template('admin/products.html', title='Керування Товарами', products=products)

# ==========================================================
# КЕРУВАННЯ ЗАМОВЛЕННЯМИ (Orders CRUD)
# ==========================================================

@admin_bp.route('/orders')
@login_required 
@admin_required 
def manage_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    statuses = ['New', 'Processing', 'Shipped', 'Completed', 'Canceled']
    # Вам потрібно створити admin/orders.html у templates/
    return render_template('admin/orders.html', title='Керування Замовленнями', orders=orders, statuses=statuses)

@admin_bp.route('/orders/update_status/<int:id>', methods=['POST'])
@login_required 
@admin_required 
def update_order_status(id):
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    order.status = new_status
    db.session.commit()
    flash(f'Статус замовлення #{id} оновлено на {new_status}.', 'info')
    return redirect(url_for('admin.manage_orders'))

@admin_bp.route('/orders/details/<int:id>')
@login_required 
@admin_required 
def order_details(id):
    order = Order.query.get_or_404(id)
    # Вам потрібно створити admin/order_details.html у templates/
    return render_template('admin/order_details.html', title=f'Замовлення #{id}', order=order)
