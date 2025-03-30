// JavaScript for the Medicines page

document.addEventListener('DOMContentLoaded', function() {
    // Medicine category filter
    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            // Optional: auto-submit form when category changes
            if (this.form && this.value) {
                this.form.submit();
            }
        });
    }

    // Medicine search
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // This would be used for client-side filtering if needed
            // But since we're using server-side filtering, this is just for reference
        });
    }

    // Calculate price total when quantity changes in medicine detail
    const quantityInput = document.getElementById('quantity');
    const priceElement = document.getElementById('medicine-price');
    const totalElement = document.getElementById('total-price');
    
    if (quantityInput && priceElement && totalElement) {
        const unitPrice = parseFloat(priceElement.textContent.replace('$', ''));
        
        quantityInput.addEventListener('change', function() {
            const quantity = parseInt(this.value) || 1;
            const total = (unitPrice * quantity).toFixed(2);
            totalElement.textContent = '$' + total;
            
            // Add a quick pulse animation to the total price when it changes
            totalElement.classList.add('pulse-animation');
            setTimeout(() => {
                totalElement.classList.remove('pulse-animation');
            }, 1000);
        });
    }
    
    // Animation for medicine cards on hover
    const medicineCards = document.querySelectorAll('.medicine-card');
    medicineCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('is-lifted');
            
            // Add shine effect
            const shineEffect = document.createElement('div');
            shineEffect.classList.add('shine-effect');
            card.appendChild(shineEffect);
            
            setTimeout(() => {
                card.removeChild(shineEffect);
            }, 1000);
        });
        
        card.addEventListener('mouseleave', () => {
            card.classList.remove('is-lifted');
        });
    });
    
    // Intersection Observer for fade-in elements specific to medicines page
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
    
    // Observer for staggered items in medicine cards
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
    
    // Observe all fade-in elements specific to medicines page
    document.querySelectorAll('.medicines-header .fade-in, .information-section .fade-in').forEach(el => {
        fadeObserver.observe(el);
    });
    
    // Observe all stagger items in medicine lists
    document.querySelectorAll('.stagger-item').forEach((el, index) => {
        staggerObserver.observe(el);
    });
    
    // Add animation to medicine category badges
    const categoryBadges = document.querySelectorAll('.badge');
    categoryBadges.forEach(badge => {
        badge.addEventListener('mouseenter', () => {
            badge.classList.add('hover-zoom');
        });
        
        badge.addEventListener('mouseleave', () => {
            badge.classList.remove('hover-zoom');
        });
    });
});
