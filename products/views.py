from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category

# Create your views here.

def all_products(request):
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    # Dictionary to map sort fields
    sort_options = {
        'price': 'price',
        'rating': 'rating',
        'name': 'name',
        'category': 'category__name'
    }

    # Apply sorting if sort and direction parameters exist
    if request.GET.get('sort') and request.GET.get('direction'):
        sort = request.GET['sort']
        direction = request.GET['direction']
        
        # Check if the sort field exists in our mapping
        if sort in sort_options:
            sort_field = sort_options[sort]
            if direction == 'desc':
                sort_field = f'-{sort_field}'
            products = products.order_by(sort_field)

    # Filter by category if provided
    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        products = products.filter(category__name__in=categories)

    # Search functionality
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Construct the current sorting value
    current_sorting = f'{sort}_{direction}' if sort and direction else 'None_None'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)




def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)