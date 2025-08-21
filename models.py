from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='buyer')  # admin, seller, buyer
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    auctions = db.relationship('Auction', backref='seller', lazy=True, foreign_keys='Auction.seller_id')
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def can_sell(self):
        return self.role in ['seller', 'admin']

    def can_admin(self):
        return self.role == 'admin'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationships
    auctions = db.relationship('Auction', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starting_bid = db.Column(db.Float, nullable=False)
    current_bid = db.Column(db.Float, default=0.0)
    image_filename = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    
    # Foreign Keys
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    bids = db.relationship('Bid', backref='auction', lazy=True, cascade='all, delete-orphan')
    winner = db.relationship('User', foreign_keys=[winner_id])

    def __repr__(self):
        return f'<Auction {self.title}>'

    @property
    def is_active(self):
        now = datetime.now(timezone.utc)
        # Convert naive datetimes to timezone-aware if needed
        start_time = self.start_time
        end_time = self.end_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        return (self.status == 'active' and 
                start_time <= now <= end_time)

    @property
    def is_ended(self):
        now = datetime.now(timezone.utc)
        # Convert naive datetime to timezone-aware if needed
        end_time = self.end_time
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        return now > end_time or self.status == 'completed'

    @property
    def time_remaining(self):
        if self.is_ended:
            return None
        now = datetime.now(timezone.utc)
        # Convert naive datetimes to timezone-aware if needed
        start_time = self.start_time
        end_time = self.end_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        if now < start_time:
            return start_time - now
        return end_time - now

    @property
    def highest_bid(self):
        return Bid.query.filter_by(auction_id=self.id).order_by(Bid.amount.desc()).first()

    def get_bid_count(self):
        return Bid.query.filter_by(auction_id=self.id).count()

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Foreign Keys
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)
    bidder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Bid ${self.amount} on {self.auction.title}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f'<Notification {self.id}>'
