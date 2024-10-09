# bag/urls.py

from django.urls import path
from .views import view_bag, remove_from_bag, add_to_bag # Ensure you import your views

urlpatterns = [
    path('add_to_bag/<int:item_id>/', add_to_bag, name='add_to_bag'),
    path('', view_bag, name='view_bag'),  # URL for viewing the bag
    path('remove/<int:product_id>/', remove_from_bag, name='remove_from_bag'),  # URL for removing items
]
