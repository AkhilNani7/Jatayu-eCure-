from datetime import datetime

def format_datetime(value, format='%Y-%m-%d'):
    """Format a datetime object to a string."""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
    return value.strftime(format)

def calculate_total(cart_items):
    """Calculate the total price of items in the cart."""
    total = 0
    for item in cart_items:
        total += item.medicine.price * item.quantity
    return total
