from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ==========================================================
# СИСТЕМА КОРИСТУВАЧІВ (Рівень 3)
# ==========================================================

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='client') 
    
    orders = db.relationship('Order', backref='user', lazy=True) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

# ==========================================================
# МАГАЗИН (Рівень 1)
# ==========================================================

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0) 

    order_details = db.relationship('OrderDetail', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(50), default='New') 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True) 

    details = db.relationship('OrderDetail', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id}>'

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# ==========================================================
# ВІДГУКИ ТА КЛІЄНТИ (Рівень 1 & 2)
# ==========================================================

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f'<Feedback {self.id}>'

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    registration_date = db.Column(db.DateTime, default=db.func.now())
    
    orders = db.relationship('Order', backref='client_info', lazy=True) 
    
    def __repr__(self):
        return f'<Client {self.full_name}>'
