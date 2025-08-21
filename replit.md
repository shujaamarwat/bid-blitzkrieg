# Bid Blitzkrieg - Online Auction Platform

## Overview

Bid Blitzkrieg is a feature-rich online auction platform built with Flask, designed to provide a seamless bidding experience for buyers and sellers. The platform supports role-based user management, real-time bidding, auction management, and comprehensive admin controls. Users can register as buyers or sellers, with sellers able to create and manage auctions while buyers can browse and bid on items. The system includes automated auction lifecycle management, email notifications, and a responsive web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask with SQLAlchemy**: Chosen for its simplicity and flexibility in building web applications. Flask provides a lightweight foundation while SQLAlchemy offers robust ORM capabilities for database operations.
- **Blueprint Architecture**: The application uses a modular approach with separate route handlers, forms, and models to maintain code organization and scalability.

### Database Design
- **SQLite/PostgreSQL Support**: The application is configured to work with SQLite for development and PostgreSQL for production environments through environment variable configuration.
- **User Role System**: Implements a three-tier role system (admin, seller, buyer) with appropriate permission controls and access restrictions.
- **Auction Lifecycle Management**: Database schema supports complete auction workflows from creation to completion, including status tracking and bidding history.

### Authentication & Security
- **Flask-Login Integration**: Provides session management and user authentication with role-based access control.
- **CSRF Protection**: Flask-WTF CSRF protection enabled across all forms to prevent cross-site request forgery attacks.
- **Password Security**: Uses Werkzeug's password hashing utilities for secure password storage and verification.

### File Management
- **Image Upload System**: Handles product images with file validation, secure filename generation, and organized storage in static directories.
- **File Size Limits**: Implements 16MB maximum file size restriction with proper error handling.

### Frontend Architecture
- **Bootstrap Integration**: Uses Bootstrap for responsive design and consistent UI components across the platform.
- **Real-time Features**: JavaScript-based countdown timers and auto-refresh functionality for active auctions.
- **Template Inheritance**: Jinja2 template system with base template inheritance for consistent layout and navigation.

### Email Notifications
- **Flask-Mail Integration**: Configured with Gmail SMTP for sending auction-related notifications to users.
- **Automated Messaging**: System sends notifications for auction outcomes, bid confirmations, and status updates.

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **SQLAlchemy**: Database ORM and connection management
- **Flask-Login**: User session and authentication management
- **Flask-WTF**: Form handling and CSRF protection
- **Flask-Mail**: Email notification system

### Frontend Libraries
- **Bootstrap CSS Framework**: Responsive UI components and styling
- **Font Awesome**: Icon library for enhanced visual elements
- **Custom CSS/JavaScript**: Additional styling and interactive features

### Database Systems
- **SQLite**: Development database (default)
- **PostgreSQL**: Production database support through environment configuration

### Email Service
- **Gmail SMTP**: Email delivery service for notifications and user communications

### File Storage
- **Local File System**: Static file storage for uploaded auction images with organized directory structure

## User Manual: Getting Started with Bid Blitzkrieg

### Prerequisites
- Basic familiarity with web applications
- Access to email for account verification
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Initial Setup for New Users

#### Step 1: Account Registration
1. **Visit the Homepage**: Navigate to your Bid Blitzkrieg application URL
2. **Click "Join Now"**: Located in the hero section or navigation bar
3. **Fill Registration Form**:
   - Enter a unique username (letters, numbers, underscores only)
   - Provide a valid email address
   - Create a strong password (minimum 8 characters)
   - Select your role: "Buyer" or "Seller"
4. **Submit Registration**: Click "Register" to create your account
5. **Login**: Use your credentials to access the platform

#### Step 2: First-Time User Experience

**For Buyers:**
1. **Browse Auctions**: Visit "All Auctions" to see available items
2. **Filter by Category**: Use category filters to find specific items
3. **View Auction Details**: Click on any auction to see full details
4. **Place Your First Bid**: Enter amount higher than current bid and click "Place Bid"
5. **Monitor Auctions**: Track your bids from your dashboard

**For Sellers:**
1. **Access Seller Dashboard**: Navigate to your dashboard after login
2. **Create First Auction**: Click "Create New Auction"
3. **Fill Auction Details**:
   - Enter compelling title and detailed description
   - Set competitive starting bid
   - Select appropriate category
   - Upload high-quality product images
   - Set auction start and end times
4. **Submit for Review**: Admin approval required for new sellers
5. **Manage Active Auctions**: Monitor bids and communicate with buyers

#### Step 3: Platform Features

**Dashboard Navigation:**
- **Overview**: See your activity summary and quick stats
- **Active Auctions**: Current auctions you're bidding on or selling
- **Bid History**: Complete record of your bidding activity
- **Won Auctions**: Items you've successfully won
- **Account Settings**: Update profile and preferences

**Bidding System:**
- **Real-time Updates**: Bid status updates automatically
- **Countdown Timers**: See exact time remaining on auctions
- **Outbid Notifications**: Get alerts when someone outbids you
- **Winning Notifications**: Instant notification when you win

**Search and Filtering:**
- **Category Browsing**: Organized by item types
- **Search Bar**: Find specific items by keywords
- **Price Filters**: Set minimum and maximum price ranges
- **Status Filters**: Active, ended, or upcoming auctions

---

## Developer Setup Guide

### Environment Configuration

#### Required Environment Variables
Create a `.env` file in your project root with the following variables:

```bash
# Database Configuration
DATABASE_URL=your_database_connection_string
PGHOST=your_postgres_host
PGPORT=5432
PGDATABASE=your_database_name
PGUSER=your_database_user
PGPASSWORD=your_database_password

# Application Security
SESSION_SECRET=your_secure_random_session_key
FLASK_SECRET_KEY=your_flask_secret_key

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

#### Database Setup Steps

**Option 1: PostgreSQL (Recommended for Production)**
1. **Install PostgreSQL**: Download and install PostgreSQL from official website
2. **Create Database**: 
   ```sql
   CREATE DATABASE bid_blitzkrieg;
   CREATE USER auction_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE bid_blitzkrieg TO auction_user;
   ```
3. **Update DATABASE_URL**: 
   ```bash
   DATABASE_URL=postgresql://auction_user:secure_password@localhost:5432/bid_blitzkrieg
   ```

**Option 2: SQLite (Development Only)**
1. **Simple Setup**: No additional installation required
2. **Update DATABASE_URL**: 
   ```bash
   DATABASE_URL=sqlite:///bid_blitzkrieg.db
   ```

#### Installation Commands

**1. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**2. Initialize Database:**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

**3. Create Admin User:**
```bash
python -c "
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username='admin',
        email='admin@auction.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print('Admin user created!')
"
```

**4. Add Sample Categories:**
```bash
python -c "
from app import app, db
from models import Category

with app.app_context():
    categories = [
        Category(name='Electronics', description='Gadgets, computers, phones'),
        Category(name='Collectibles', description='Rare items, antiques, memorabilia'),
        Category(name='Art & Crafts', description='Artwork, handmade items'),
        Category(name='Home & Garden', description='Furniture, tools, decorations'),
        Category(name='Fashion', description='Clothing, accessories, jewelry'),
        Category(name='Books & Media', description='Books, movies, music')
    ]
    for category in categories:
        db.session.add(category)
    db.session.commit()
    print('Sample categories added!')
"
```

**5. Start Application:**
```bash
python main.py
```

#### Email Configuration (Optional)

**Gmail Setup:**
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**: 
   - Go to Google Account Settings > Security > App Passwords
   - Generate password for "Mail" application
3. **Update Environment Variables**:
   ```bash
   MAIL_USERNAME=your_gmail@gmail.com
   MAIL_PASSWORD=your_16_character_app_password
   ```

#### File Upload Configuration

**Image Storage:**
- **Upload Directory**: `static/uploads/`
- **Supported Formats**: JPG, PNG, GIF
- **File Size Limit**: 16MB maximum
- **Automatic Cleanup**: Old unused images cleaned periodically

**Setup Upload Directory:**
```bash
mkdir -p static/uploads
chmod 755 static/uploads
```

#### Security Recommendations

**Production Deployment:**
1. **Use Strong Secrets**: Generate cryptographically secure session keys
2. **HTTPS Only**: Always use SSL/TLS in production
3. **Database Security**: Use connection pooling and prepared statements
4. **File Uploads**: Validate file types and scan for malware
5. **Rate Limiting**: Implement rate limiting for bid submissions
6. **Regular Backups**: Automated database backups recommended

#### Troubleshooting Common Issues

**Database Connection Errors:**
- Verify DATABASE_URL format and credentials
- Check if PostgreSQL service is running
- Ensure database exists and user has proper permissions

**File Upload Issues:**
- Check `static/uploads/` directory permissions
- Verify file size limits in web server configuration
- Ensure sufficient disk space available

**Email Delivery Problems:**
- Confirm SMTP settings and credentials
- Check spam folders for outgoing emails
- Verify app password generation for Gmail

#### Default Login Credentials

**Admin Account:**
- Username: `admin`
- Email: `admin@auction.com`
- Password: `admin123`
- Role: Administrator

**Note**: Change default admin password immediately after first login for security.