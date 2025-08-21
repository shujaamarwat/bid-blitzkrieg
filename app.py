import os
import logging
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///auction.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# initialize extensions
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
mail.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Template filters
@app.template_filter('datetime')
def datetime_filter(dt):
    if dt is None:
        return ''
    return dt.strftime('%B %d, %Y at %I:%M %p')

@app.template_filter('currency')
def currency_filter(amount):
    if amount is None:
        return '$0.00'
    return f'${amount:.2f}'

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create tables
    db.create_all()
    
    # Create admin user if it doesn't exist
    from models import User, Category
    from werkzeug.security import generate_password_hash
    
    admin = User.query.filter_by(email='admin@auction.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@auction.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Created admin user: admin@auction.com / admin123")
    
    # Create default categories if they don't exist
    default_categories = [
        {'name': 'Electronics', 'description': 'Computers, phones, gadgets and electronic devices'},
        {'name': 'Collectibles', 'description': 'Rare items, antiques, and collectible memorabilia'},
        {'name': 'Art & Crafts', 'description': 'Paintings, sculptures, handmade items and artwork'},
        {'name': 'Home & Garden', 'description': 'Furniture, decor, tools and garden equipment'},
        {'name': 'Fashion', 'description': 'Clothing, accessories, shoes and fashion items'},
        {'name': 'Books & Media', 'description': 'Books, movies, music and educational materials'}
    ]
    
    for cat_data in default_categories:
        existing = Category.query.filter_by(name=cat_data['name']).first()
        if not existing:
            category = Category(name=cat_data['name'], description=cat_data['description'])
            db.session.add(category)
    
    db.session.commit()
