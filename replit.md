# Overview

Bid Blitzkrieg is an online auction platform built with Flask that enables users to create, manage, and participate in auctions. The platform supports role-based access with three user types: admins, sellers, and buyers. It provides comprehensive auction management features including real-time bidding, countdown timers, image uploads, email notifications, and administrative controls.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Flask with SQLAlchemy**: Uses Flask as the web framework with SQLAlchemy ORM for database operations. Flask provides lightweight structure while SQLAlchemy handles database interactions and relationships.
- **Blueprint-based Architecture**: Organizes code into separate modules with dedicated route handlers, forms, and models for maintainability and scalability.

## Database Design
- **SQLite/PostgreSQL Support**: Configured for SQLite in development and PostgreSQL in production through environment variables, providing flexibility across deployment environments.
- **Role-based User System**: Implements three-tier user roles (admin, seller, buyer) with granular permission controls and access restrictions.
- **Auction Lifecycle Management**: Complete auction workflow support from creation to completion, including status tracking, bidding history, and automated closure.

## Authentication & Security
- **Flask-Login Integration**: Manages user sessions and authentication with role-based access control and permission validation.
- **CSRF Protection**: Flask-WTF provides CSRF token protection across all forms to prevent cross-site request forgery attacks.
- **Password Security**: Uses Werkzeug's secure password hashing for credential storage and verification.

## File Management
- **Image Upload System**: Handles product images with file validation, secure filename generation using Werkzeug, and organized storage in static directories.
- **Upload Restrictions**: 16MB maximum file size limit with proper error handling and file type validation.

## Frontend Architecture
- **Bootstrap Integration**: Responsive design using Bootstrap CSS framework for consistent UI components and mobile compatibility.
- **Real-time Features**: JavaScript-powered countdown timers, auto-refresh functionality, and dynamic bid validation for active auctions.
- **Template System**: Jinja2 templates with base template inheritance ensuring consistent navigation and layout across pages.

## Email Notifications
- **Flask-Mail Integration**: SMTP configuration for automated email notifications using Gmail as the mail server.
- **Event-driven Messaging**: Sends notifications for auction outcomes, bid confirmations, and status updates to relevant users.

# External Dependencies

## Core Framework
- **Flask**: Primary web application framework
- **SQLAlchemy**: Database ORM and connection management
- **Flask-Login**: User session management and authentication
- **Flask-WTF**: Form handling, validation, and CSRF protection
- **Flask-Mail**: Email notification system
- **Werkzeug**: Password hashing and secure file handling utilities

## Frontend Libraries
- **Bootstrap CSS Framework**: Responsive UI components and grid system
- **Font Awesome**: Icon library for user interface elements
- **Custom CSS/JavaScript**: Application-specific styling and interactive features

## Production Infrastructure
- **PostgreSQL**: Production database (configurable via environment variables)
- **SQLite**: Development database
- **Gmail SMTP**: Email service for notifications
- **File System Storage**: Static file hosting for uploaded images

# Recent Updates

## Database Configuration and Deployment Documentation (August 21, 2025)
- **Comprehensive README.md**: Added detailed database configuration instructions for both development (SQLite) and production (PostgreSQL) environments
- **Deployment Guide**: Included step-by-step deployment instructions for both Replit and manual deployment options
- **Environment Variables**: Documented all required environment variables including DATABASE_URL, SESSION_SECRET, and email configuration
- **Troubleshooting Section**: Added common issues and solutions for database connections, image uploads, and email functionality
- **Security Guidelines**: Included production security considerations and best practices
- **Demo Credentials**: Documented test admin account for development purposes