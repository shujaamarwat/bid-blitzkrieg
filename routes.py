import os
from datetime import datetime, timezone
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_, desc

from app import app, db
from models import User, Auction, Bid, Category, Notification
from forms import LoginForm, RegisterForm, AuctionForm, BidForm, CategoryForm, UserForm

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def index():
    # Get active auctions
    now = datetime.now(timezone.utc)
    active_auctions = Auction.query.filter(
        Auction.status == 'active',
        Auction.start_time <= now,
        Auction.end_time > now
    ).order_by(Auction.end_time.asc()).limit(6).all()
    
    # Get featured categories
    categories = Category.query.limit(4).all()
    
    return render_template('index.html', auctions=active_auctions, categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact admin.', 'danger')
                return render_template('auth/login.html', form=form)
            
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to next page or dashboard based on role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'seller':
                return redirect(url_for('seller_dashboard'))
            else:
                return redirect(url_for('buyer_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/auctions')
def auction_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    status = request.args.get('status', 'active')
    
    query = Auction.query
    
    if search:
        query = query.filter(or_(
            Auction.title.contains(search),
            Auction.description.contains(search)
        ))
    
    if category:
        query = query.filter(Auction.category_id == category)
    
    if status == 'active':
        now = datetime.now(timezone.utc)
        query = query.filter(
            Auction.status == 'active',
            Auction.start_time <= now,
            Auction.end_time > now
        )
    elif status == 'ended':
        now = datetime.now(timezone.utc)
        query = query.filter(or_(
            Auction.end_time <= now,
            Auction.status == 'completed'
        ))
    
    auctions = query.order_by(Auction.end_time.asc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('auctions/list.html', 
                         auctions=auctions, 
                         categories=categories,
                         search=search, 
                         selected_category=category,
                         selected_status=status)

@app.route('/auction/<int:id>')
def auction_detail(id):
    auction = Auction.query.get_or_404(id)
    bids = Bid.query.filter_by(auction_id=id).order_by(desc(Bid.timestamp)).limit(10).all()
    
    form = BidForm()
    form.auction_id.data = id
    
    return render_template('auctions/detail.html', auction=auction, bids=bids, form=form)

@app.route('/create_auction', methods=['GET', 'POST'])
@login_required
def create_auction():
    if not current_user.can_sell():
        flash('You need seller privileges to create auctions.', 'danger')
        return redirect(url_for('index'))
    
    form = AuctionForm()
    if form.validate_on_submit():
        # Handle file upload
        filename = None
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                
                # Ensure upload directory exists
                upload_path = os.path.join(current_app.instance_path, 'static', 'uploads')
                os.makedirs(upload_path, exist_ok=True)
                
                file.save(os.path.join(upload_path, filename))
        
        auction = Auction(
            title=form.title.data,
            description=form.description.data,
            starting_bid=form.starting_bid.data,
            category_id=form.category_id.data,
            image_filename=filename,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            seller_id=current_user.id,
            status='pending' if current_user.role != 'admin' else 'active'
        )
        
        db.session.add(auction)
        db.session.commit()
        
        if auction.status == 'pending':
            flash('Your auction has been submitted for admin approval.', 'info')
        else:
            flash('Auction created successfully!', 'success')
        
        return redirect(url_for('seller_dashboard'))
    
    return render_template('auctions/create.html', form=form)

@app.route('/bid', methods=['POST'])
@login_required
def place_bid():
    form = BidForm()
    if form.validate_on_submit():
        auction = Auction.query.get_or_404(form.auction_id.data)
        
        # Additional server-side validation
        if not auction.is_active:
            flash('This auction is no longer active.', 'danger')
            return redirect(url_for('auction_detail', id=auction.id))
        
        if auction.seller_id == current_user.id:
            flash('You cannot bid on your own auction.', 'danger')
            return redirect(url_for('auction_detail', id=auction.id))
        
        # Create bid
        bid = Bid(
            amount=form.amount.data,
            auction_id=auction.id,
            bidder_id=current_user.id
        )
        
        # Update auction current bid
        auction.current_bid = form.amount.data
        
        db.session.add(bid)
        db.session.commit()
        
        flash(f'Bid of ${form.amount.data:.2f} placed successfully!', 'success')
        
        # Create notification for seller
        notification = Notification(
            user_id=auction.seller_id,
            message=f'New bid of ${form.amount.data:.2f} on your auction "{auction.title}"'
        )
        db.session.add(notification)
        db.session.commit()
        
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'danger')
    
    return redirect(url_for('auction_detail', id=form.auction_id.data))

# Dashboard routes
@app.route('/dashboard/admin')
@login_required
def admin_dashboard():
    if not current_user.can_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('index'))
    
    # Statistics
    total_users = User.query.count()
    total_auctions = Auction.query.count()
    active_auctions = Auction.query.filter_by(status='active').count()
    pending_auctions = Auction.query.filter_by(status='pending').all()
    
    return render_template('dashboard/admin.html',
                         total_users=total_users,
                         total_auctions=total_auctions,
                         active_auctions=active_auctions,
                         pending_auctions=pending_auctions)

@app.route('/dashboard/seller')
@login_required
def seller_dashboard():
    if not current_user.can_sell():
        flash('Seller access required.', 'danger')
        return redirect(url_for('index'))
    
    # Get seller's auctions
    my_auctions = Auction.query.filter_by(seller_id=current_user.id).order_by(desc(Auction.created_at)).all()
    
    return render_template('dashboard/seller.html', auctions=my_auctions)

@app.route('/dashboard/buyer')
@login_required
def buyer_dashboard():
    # Get user's bids
    my_bids = Bid.query.filter_by(bidder_id=current_user.id).order_by(desc(Bid.timestamp)).limit(10).all()
    
    # Get auctions user won
    won_auctions = Auction.query.filter_by(winner_id=current_user.id).all()
    
    return render_template('dashboard/buyer.html', bids=my_bids, won_auctions=won_auctions)

# Admin management routes
@app.route('/admin/approve_auction/<int:id>')
@login_required
def approve_auction(id):
    if not current_user.can_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('index'))
    
    auction = Auction.query.get_or_404(id)
    auction.status = 'active'
    db.session.commit()
    
    # Notify seller
    notification = Notification(
        user_id=auction.seller_id,
        message=f'Your auction "{auction.title}" has been approved and is now live!'
    )
    db.session.add(notification)
    db.session.commit()
    
    flash('Auction approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users')
@login_required
def manage_users():
    if not current_user.can_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('index'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('dashboard/manage_users.html', users=users)

@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if not current_user.can_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('index'))
    
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('manage_categories'))
    
    categories = Category.query.all()
    return render_template('dashboard/manage_categories.html', categories=categories, form=form)

# Background task to close ended auctions and determine winners
@app.route('/admin/close_ended_auctions')
@login_required
def close_ended_auctions():
    if not current_user.can_admin():
        flash('Admin access required.', 'danger')
        return redirect(url_for('index'))
    
    now = datetime.now(timezone.utc)
    ended_auctions = Auction.query.filter(
        Auction.status == 'active',
        Auction.end_time <= now
    ).all()
    
    for auction in ended_auctions:
        highest_bid = auction.highest_bid
        if highest_bid:
            auction.winner_id = highest_bid.bidder_id
            auction.current_bid = highest_bid.amount
            
            # Notify winner
            winner_notification = Notification(
                user_id=highest_bid.bidder_id,
                message=f'Congratulations! You won the auction for "{auction.title}" with a bid of ${highest_bid.amount:.2f}'
            )
            db.session.add(winner_notification)
            
            # Notify seller
            seller_notification = Notification(
                user_id=auction.seller_id,
                message=f'Your auction "{auction.title}" has ended. Winner: {highest_bid.bidder.username} - ${highest_bid.amount:.2f}'
            )
            db.session.add(seller_notification)
        
        auction.status = 'completed'
    
    db.session.commit()
    flash(f'Closed {len(ended_auctions)} ended auctions.', 'success')
    return redirect(url_for('admin_dashboard'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
