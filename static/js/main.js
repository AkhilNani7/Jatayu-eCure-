// Main JavaScript file for the HealthCare Portal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert.alert-info');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Handle mobile navigation
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            if (navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            } else {
                navbarCollapse.classList.add('show');
            }
        });
    }

    // Add active class to current page in sidebar if exists
    const currentLocation = window.location.pathname;
    const sidebarLinks = document.querySelectorAll('.list-group-item');
    sidebarLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    // Observer for fade-in elements
    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observer for staggered items
    const staggerObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add delay based on index for stagger effect
                setTimeout(() => {
                    entry.target.classList.add('is-visible');
                }, 150 * index);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all fade-in elements
    document.querySelectorAll('.fade-in').forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Observe all stagger items
    document.querySelectorAll('.stagger-item').forEach((el, index) => {
        staggerObserver.observe(el);
    });
    
    // Observe slide-in-left elements
    document.querySelectorAll('.slide-in-left').forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Observe slide-in-right elements
    document.querySelectorAll('.slide-in-right').forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Add hover effects to elements with hover-lift class
    document.querySelectorAll('.hover-lift').forEach(el => {
        el.addEventListener('mouseenter', () => {
            el.classList.add('is-lifted');
        });
        el.addEventListener('mouseleave', () => {
            el.classList.remove('is-lifted');
        });
    });
    
    // Add rotation effect to hover-rotate-icon elements
    document.querySelectorAll('.hover-rotate-icon').forEach(el => {
        el.addEventListener('mouseenter', () => {
            el.classList.add('is-rotating');
        });
        el.addEventListener('mouseleave', () => {
            el.classList.remove('is-rotating');
        });
    });
});

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    }).format(amount);
}

// Helper function to format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}
