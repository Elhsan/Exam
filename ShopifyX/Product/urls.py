from django.urls import path, include
from .views import *

urlpatterns = [
    path('product/', product, name='product'),
    path('product/my_product/', my_products, name='my_product'),
    path('product/create/', create_product, name='create_product'),
    path('product/<int:product_id>/', view_product, name='view_product'),
    path('product/<int:product_id>/edit', edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    
]
