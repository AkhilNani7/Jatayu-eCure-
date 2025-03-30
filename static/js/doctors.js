// JavaScript for the Doctors page

document.addEventListener('DOMContentLoaded', function() {
    // Doctor specialty filter
    const specialtySelect = document.querySelector('select[name="specialty"]');
    if (specialtySelect) {
        specialtySelect.addEventListener('change', function() {
            // Optional: auto-submit form when specialty changes
            if (this.form && this.value) {
                this.form.submit();
            }
        });
    }

    // Doctor search functionality
    const searchInput = document.getElementById('doctor-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const doctors = document.querySelectorAll('.doctor-card');
            
            doctors.forEach(function(doctor) {
                const doctorName = doctor.querySelector('.doctor-name').textContent.toLowerCase();
                const doctorSpecialty = doctor.querySelector('.doctor-specialty').textContent.toLowerCase();
                
                if (doctorName.includes(searchTerm) || doctorSpecialty.includes(searchTerm)) {
                    doctor.style.display = '';
                } else {
                    doctor.style.display = 'none';
                }
            });
        });
    }
    
    // Animation for doctor cards on hover
    const doctorCards = document.querySelectorAll('.doctor-card');
    doctorCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // Add highlight to doctor avatar on hover
            const doctorAvatar = card.querySelector('.doctor-avatar');
            if (doctorAvatar) {
                doctorAvatar.classList.add('pulse-animation');
            }
            
            // Add shine effect to doctor banner
            const doctorBanner = card.querySelector('.doctor-banner');
            if (doctorBanner) {
                doctorBanner.classList.add('shimmer-animation');
                
                setTimeout(() => {
                    doctorBanner.classList.remove('shimmer-animation');
                }, 1500);
            }
        });
        
        card.addEventListener('mouseleave', () => {
            // Remove avatar animation on mouse leave
            const doctorAvatar = card.querySelector('.doctor-avatar');
            if (doctorAvatar) {
                doctorAvatar.classList.remove('pulse-animation');
            }
        });
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
    
    // Observer for staggered items in doctor cards
    const staggerObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add delay based on index for stagger effect
                setTimeout(() => {
                    entry.target.classList.add('is-visible');
                }, 100 * index);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all fade-in elements specific to doctors page
    document.querySelectorAll('.doctors-header .fade-in, .feature-card').forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Observe all stagger items in doctor list
    document.querySelectorAll('.stagger-item').forEach((el, index) => {
        staggerObserver.observe(el);
    });
    
    // Add subtle animation to specialty badges
    const specialtyBadges = document.querySelectorAll('.badge');
    specialtyBadges.forEach(badge => {
        badge.addEventListener('mouseenter', () => {
            badge.classList.add('hover-zoom');
        });
        
        badge.addEventListener('mouseleave', () => {
            badge.classList.remove('hover-zoom');
        });
    });
    
    // Add animation for star rating icons
    const ratingStars = document.querySelectorAll('.fa-star');
    ratingStars.forEach(star => {
        star.addEventListener('mouseenter', () => {
            star.classList.add('animate-icon');
        });
        
        star.addEventListener('mouseleave', () => {
            star.classList.remove('animate-icon');
        });
    });
});
