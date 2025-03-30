// JavaScript for the Cart page

document.addEventListener('DOMContentLoaded', function() {
    // Update quantity
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            // Auto-submit the form when quantity changes
            if (this.form) {
                this.form.submit();
            }
        });
    });

    // Calculate and update cart totals
    function updateCartTotals() {
        let subtotal = 0;
        const cartItems = document.querySelectorAll('.cart-item');
        
        cartItems.forEach(function(item) {
            const price = parseFloat(item.querySelector('.item-price').dataset.price);
            const quantity = parseInt(item.querySelector('input[name="quantity"]').value);
            const itemTotal = price * quantity;
            
            item.querySelector('.item-total').textContent = '$' + itemTotal.toFixed(2);
            subtotal += itemTotal;
        });
        
        const subtotalElement = document.getElementById('cart-subtotal');
        const totalElement = document.getElementById('cart-total');
        
        if (subtotalElement) {
            subtotalElement.textContent = '$' + subtotal.toFixed(2);
        }
        
        if (totalElement) {
            // Add shipping or other costs if needed
            totalElement.textContent = '$' + subtotal.toFixed(2);
        }
    }

    // Initial update
    updateCartTotals();
});
