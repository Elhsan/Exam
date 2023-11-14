from django.contrib import messages 
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import JsonResponse
from Profile.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
def home_page(request):
    user_status = {
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'username': request.user.username,
    }
    return render(request, 'main/home.html', {'user_status': user_status})


def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request, f"Welcome to our site {username}!")
            form.save()
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'main/create_user.html', context)


def product(request):
    products = Product.objects.all()
    return render(request, 'main/product.html', {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, является ли текущий пользователь создателем товара
    if request.user != product.user:
        # Если не является, перенаправляем на страницу просмотра товара
        return redirect('product')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm(instance=product)

    return render(request, 'main/edit_product.html', {'form': form, 'product': product})

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'main/view_product.html', {'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, является ли текущий пользователь создателем товара
    if request.user == product.user:
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

    return render(request, 'main/create_product.html', {'form': form})

def my_products(request):
    if request.user.is_authenticated:
        user_products = Product.objects.filter(user=request.user)
        return render(request, 'main/my_products.html', {'user_products': user_products})
    else:
        return render(request, 'main/my_products.html', {'user_products': []})