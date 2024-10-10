from django.urls import path
from .views import view_bag, add_to_bag, adjust_bag, remove_from_bag  # Import view_bag here

urlpatterns = [
    path('', view_bag, name='view_bag'),
    path('add/<int:item_id>/', add_to_bag, name='add_to_bag'),
    path('adjust/<item_id>/', adjust_bag, name='adjust_bag'),  # Ensure the view function is correctly referenced
    path('remove/<int:item_id>/', remove_from_bag, name='remove_from_bag'),  # Change product_id to item_id to match your views
]
