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
