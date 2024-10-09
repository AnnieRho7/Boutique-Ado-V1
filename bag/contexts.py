from decimal import Decimal
from django.conf import settings

def bag_contents(request):
    """ Context processor that returns the bag contents """
    
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    product_count = 0
    
    for item_id, quantity in bag.items():
        product = ...  # Fetch the product based on item_id
        total += product.price * quantity
        bag_items.append({
            'product': product,
            'quantity': quantity,
        })
        product_count += quantity
    
    # Calculate delivery costs
    delivery = 0
    free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD
    standard_delivery_percentage = settings.STANDARD_DELIVERY_PERCENTAGE
    
    if total < free_delivery_threshold:
        delivery = total * standard_delivery_percentage / 100
    free_delivery_delta = max(0, free_delivery_threshold - total)

    grand_total = total + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': free_delivery_threshold,
        'grand_total': grand_total,
    }
