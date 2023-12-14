from django.contrib import admin
from .models import Product, Wishlist, Comment

admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Comment)