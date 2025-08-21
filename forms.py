from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SelectField, PasswordField, DateTimeLocalField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, ValidationError
from datetime import datetime, timezone
from models import User, Category

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    role = SelectField('Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller')], default='buyer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class AuctionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    starting_bid = FloatField('Starting Bid ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    start_time = DateTimeLocalField('Start Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_time = DateTimeLocalField('End Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')

    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    def validate_start_time(self, start_time):
        if start_time.data < datetime.now():
            raise ValidationError('Start time must be in the future.')

    def validate_end_time(self, end_time):
        if hasattr(self, 'start_time') and self.start_time.data:
            if end_time.data <= self.start_time.data:
                raise ValidationError('End time must be after start time.')

class BidForm(FlaskForm):
    amount = FloatField('Bid Amount ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    auction_id = HiddenField('Auction ID', validators=[DataRequired()])

    def validate_amount(self, amount):
        from models import Auction, Bid
        auction = Auction.query.get(self.auction_id.data)
        if not auction:
            raise ValidationError('Invalid auction.')
        
        if not auction.is_active:
            raise ValidationError('This auction is no longer active.')
        
        # Check if bid is higher than current highest bid or starting bid
        highest_bid = auction.highest_bid
        min_bid = highest_bid.amount if highest_bid else auction.starting_bid
        
        if amount.data <= min_bid:
            raise ValidationError(f'Bid must be higher than ${min_bid:.2f}')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('admin', 'Admin')])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')])
