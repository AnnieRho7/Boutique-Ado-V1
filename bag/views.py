from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def view_bag(request):
    """ A view that renders the bag contents page """

    bag = request.session.get('bag', {})  # Retrieve the bag from the session
    bag_items = []

    for product_id, quantity in bag.items():
        product = get_object_or_404(Product, id=product_id)  # Get the product from the database
        total = product.price * quantity  # Calculate total for the product
        bag_items.append({
            'product': product,  # Add the actual Product instance
            'quantity': quantity,
            'total': total,  # Include the total in the item dict
        })

    context = {
        'bag_items': bag_items,
    }

    return render(request, 'bag/bag.html', context)


def remove_from_bag(request, product_id):
    """ A view to remove an item from the bag """
    
    bag = request.session.get('bag', {})
    
    if product_id in bag:
        del bag[product_id]
        messages.success(request, "Item removed from your bag.")
    else:
        messages.error(request, "Item not found in your bag.")
    
    request.session['bag'] = bag  # Save updated bag to the session
    return redirect('view_bag')  # Redirect back to the bag view


def add_to_bag(request, item_id):
    """Add a product to the shopping bag."""
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    
    # Get the existing bag from the session or create a new one
    bag = request.session.get('bag', {})
    
    # Update the bag with the item id and quantity
    if item_id in bag:
        bag[item_id] += quantity  # Increment existing quantity
    else:
        bag[item_id] = quantity  # Add new item

    # Update the session bag
    request.session['bag'] = bag
    
    # Optional: Add a message to inform the user
    messages.success(request, f'Added {quantity} of item {item_id} to your bag!')

    return redirect(redirect_url)