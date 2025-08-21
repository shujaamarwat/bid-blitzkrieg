// Auction platform JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize countdown timers
    initCountdownTimers();
    
    // Initialize bid form validation
    initBidFormValidation();
    
    // Initialize image preview for auction creation
    initImagePreview();
    
    // Initialize auto-refresh for active auctions
    initAutoRefresh();
    
    // Initialize tooltips
    initTooltips();
});

// Countdown Timer Functionality
function initCountdownTimers() {
    const countdownElements = document.querySelectorAll('.countdown');
    
    countdownElements.forEach(element => {
        const endTime = element.dataset.end;
        if (endTime) {
            updateCountdown(element, endTime);
            setInterval(() => updateCountdown(element, endTime), 1000);
        }
    });
}

function updateCountdown(element, endTimeString) {
    const endTime = new Date(endTimeString).getTime();
    const now = new Date().getTime();
    const timeLeft = endTime - now;
    
    if (timeLeft <= 0) {
        element.innerHTML = '<i class="fas fa-flag-checkered"></i> Ended';
        element.classList.add('text-danger');
        return;
    }
    
    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
    
    let countdownText = '';
    
    if (days > 0) {
        countdownText = `${days}d ${hours}h ${minutes}m`;
    } else if (hours > 0) {
        countdownText = `${hours}h ${minutes}m ${seconds}s`;
    } else if (minutes > 0) {
        countdownText = `${minutes}m ${seconds}s`;
    } else {
        countdownText = `${seconds}s`;
        element.classList.add('urgent');
    }
    
    element.innerHTML = `<i class="fas fa-clock"></i> ${countdownText}`;
    
    // Add urgency styling for last hour
    if (timeLeft <= 3600000) { // 1 hour in milliseconds
        element.classList.add('text-warning');
    }
    
    // Add critical styling for last 5 minutes
    if (timeLeft <= 300000) { // 5 minutes in milliseconds
        element.classList.add('text-danger', 'urgent');
        element.classList.remove('text-warning');
    }
}

// Bid Form Validation
function initBidFormValidation() {
    const bidForms = document.querySelectorAll('.bid-form');
    
    bidForms.forEach(form => {
        const amountInput = form.querySelector('input[name="amount"]');
        const submitButton = form.querySelector('button[type="submit"]');
        
        if (amountInput && submitButton) {
            amountInput.addEventListener('input', function() {
                validateBidAmount(this, submitButton);
            });
            
            form.addEventListener('submit', function(e) {
                if (!validateBidAmount(amountInput, submitButton)) {
                    e.preventDefault();
                }
            });
        }
    });
}

function validateBidAmount(input, submitButton) {
    const amount = parseFloat(input.value);
    const minBid = parseFloat(input.getAttribute('data-min-bid') || 0);
    
    if (isNaN(amount) || amount <= minBid) {
        input.classList.add('is-invalid');
        submitButton.disabled = true;
        return false;
    } else {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
        submitButton.disabled = false;
        return true;
    }
}

// Image Preview for Auction Creation
function initImagePreview() {
    const imageInput = document.querySelector('input[name="image"]');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

function showImagePreview(src) {
    // Remove existing preview
    const existingPreview = document.querySelector('.image-preview');
    if (existingPreview) {
        existingPreview.remove();
    }
    
    // Create new preview
    const preview = document.createElement('div');
    preview.className = 'image-preview mt-2';
    preview.innerHTML = `
        <div class="card" style="max-width: 200px;">
            <img src="${src}" class="card-img-top" alt="Preview" style="height: 150px; object-fit: cover;">
            <div class="card-body text-center p-2">
                <small class="text-muted">Image Preview</small>
            </div>
        </div>
    `;
    
    // Insert after the file input
    const imageInput = document.querySelector('input[name="image"]');
    imageInput.parentNode.insertBefore(preview, imageInput.nextSibling);
}

// Auto-refresh for Active Auctions
function initAutoRefresh() {
    // Only refresh auction detail pages with active auctions
    const isAuctionDetail = window.location.pathname.includes('/auction/');
    const hasActiveAuction = document.querySelector('.countdown');
    
    if (isAuctionDetail && hasActiveAuction) {
        // Refresh bid section every 30 seconds
        setInterval(refreshBidSection, 30000);
    }
}

function refreshBidSection() {
    const bidSection = document.querySelector('.bid-history');
    if (bidSection) {
        // Get current auction ID from URL
        const auctionId = window.location.pathname.split('/').pop();
        
        fetch(`/auction/${auctionId}/bids`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.bids) {
                updateBidHistory(data.bids);
            }
            if (data.current_bid) {
                updateCurrentBid(data.current_bid);
            }
        })
        .catch(error => {
            console.log('Auto-refresh failed:', error);
        });
    }
}

function updateBidHistory(bids) {
    const bidHistory = document.querySelector('.bid-history');
    if (bidHistory && bids.length > 0) {
        bidHistory.innerHTML = bids.map(bid => `
            <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
                <div>
                    <strong>${bid.bidder_name}</strong><br>
                    <small class="text-muted">${bid.timestamp}</small>
                </div>
                <div class="text-end">
                    <strong class="text-success">$${bid.amount.toFixed(2)}</strong>
                </div>
            </div>
        `).join('');
    }
}

function updateCurrentBid(bidData) {
    const currentBidSection = document.querySelector('.card-body .text-success');
    if (currentBidSection && bidData) {
        currentBidSection.innerHTML = `$${bidData.amount.toFixed(2)}`;
        // Add animation for new bid
        currentBidSection.parentElement.classList.add('new-bid');
        setTimeout(() => {
            currentBidSection.parentElement.classList.remove('new-bid');
        }, 2000);
    }
}

// Initialize Bootstrap Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl + / to focus search
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        // Skip if href is just "#" or invalid
        if (href === '#' || !href || href.length <= 1) {
            return;
        }
        
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission with loading states
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton) {
        // Show loading state
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
        submitButton.disabled = true;
        
        // Reset button after 5 seconds (fallback)
        setTimeout(() => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }, 5000);
    }
});

// Image lazy loading
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Service Worker Registration (for future offline support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}
