from django.shortcuts import render, redirect, get_object_or_404, redirect

from django.contrib import messages 
from .forms import *
from .models import *



# Create your views here.

def product(request):
    products = Product.objects.all()
    user_status = {
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'username': request.user.username,
    }
    return render(request, 'product/product.html', {'products': products, 'user_status': user_status})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, является ли текущий пользователь создателем товара
    if request.user != product.user and not request.user.is_superuser:
        # Если не является, перенаправляем на страницу просмотра товара
        return redirect('product')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product/edit_product.html', {'form': form, 'product': product})

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/view_product.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, является ли текущий пользователь создателем товара
    if request.user == product.user or request.user.is_superuser:
        product.delete()

    return redirect('product') 

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Привязываем пользователя к создаваемому продукту
            form.instance.user = request.user
            form.save()
            return redirect('product')  # Предполагается, что 'index' - ваша страница со списком товаров
    else:
        form = ProductForm()

    return render(request, 'product/create_product.html', {'form': form})

def my_products(request):
    if request.user.is_authenticated:
        user_products = Product.objects.filter(user=request.user)
        return render(request, 'product/my_products.html', {'user_products': user_products})
    else:
        return render(request, 'product/my_products.html', {'user_products': []})