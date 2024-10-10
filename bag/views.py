from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from decimal import Decimal

def view_bag(request):
    """ A view that renders the bag contents page """
    bag = request.session.get('bag', {})
    bag_items = []

    for product_id_str, quantity in bag.items():
        try:
            product_id = int(product_id_str)  # Convert to int
            product = get_object_or_404(Product, id=product_id)  # Fetch the product
            total = product.price * quantity  # Calculate total price for this item
            bag_items.append({
                'product': product,
                'quantity': quantity,
                'total': total,
            })
        except ValueError:
            print(f"Invalid product ID: {product_id_str}")  # Handle non-integer IDs
        except Exception as e:
            print(f"Error fetching product with ID {product_id_str}: {e}")

    context = {
        'bag_items': bag_items,  # Prepare the context with bag items
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
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not specified
    redirect_url = request.POST.get('redirect_url')

    # Get the existing bag from the session or create a new one
    bag = request.session.get('bag', {})

    # Update the bag with the item id and quantity
    item_id_str = str(item_id)  # Convert to string
    if item_id_str in bag:
        bag[item_id_str] += quantity  # Increment existing quantity
    else:
        bag[item_id_str] = quantity  # Add new item

    # Update the session bag
    request.session['bag'] = bag
    
    messages.success(request, f'Added {quantity} of item {item_id} to your bag!')
    return redirect(redirect_url)