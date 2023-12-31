from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib import messages 
from .forms import *
from .models import *
from Profile.models import *




def wishlist(request):
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
    user_status = {
        'username': request.user.username,
    }
    products = Product.objects.all()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    total_price = wishlist_items.aggregate(Sum('product__price'))['product__price__sum'] or 0
    return render(request, 'product/wishlist.html', {'wishlist_items': wishlist_items, 'user_status': user_status, 'user_group': user_group, 'total_price': total_price, 'product': product})

def add_to_wishlist(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('product')

    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.quantity += 1
        wishlist_item.save()

    messages.success(request, f"{product.name} added to your wishlist!")

    # Check the referring page and redirect accordingly
    referring_page = request.META.get('HTTP_REFERER', '')
    if 'wishlist' in referring_page:
        return redirect('wishlist')
    else:
        return redirect('product')


def remove_from_wishlist(request, wishlist_id):
    wishlist_item = Wishlist.objects.get(id=wishlist_id)


    if wishlist_item.quantity > 0:
        wishlist_item.delete()

    messages.success(request, f"{wishlist_item.product.name} removed from your wishlist!")
    return redirect('wishlist')

def product(request):
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
    products = Product.objects.all()
    user_status = {
        'username': request.user.username,
    }
    sort_order = request.GET.get('sort_order', 'ascending')

    if sort_order == 'ascending':
        products = Product.objects.all().order_by('price')
    elif sort_order == 'descending':
        products = Product.objects.all().order_by('-price')
    else:
        products = Product.objects.all()

    return render(request, 'product/product.html', {'products': products, 'user_status': user_status, 'user_group': user_group, 'products': products})
def credit_card_page(request):
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
    user_status = {
        'username': request.user.username,
    }
    wishlist_items = Wishlist.objects.filter(user=request.user)
    total_price = wishlist_items.aggregate(Sum('product__price'))['product__price__sum'] or 0
    Subtotal = total_price + 5% + 5
    return render(request, 'product/credit_card.html', {'user_status': user_status, 'user_group': user_group, 'Subtotal':Subtotal, 'wishlist_items':wishlist_items})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    profile = UserProfile.objects.all()
    user_status = {
        'username': request.user.username,
    }

    # Проверяем, является ли текущий пользователь создателем товара
    if request.user != product.user and not request.user.is_superuser and request.user.groups.first().name != 'Admin':
        # Если не является, перенаправляем на страницу просмотра товара
        return redirect('product')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product/edit_product.html', {'form': form, 'product': product, 'user_status': user_status})

def view_product(request, product_id):
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
    product = get_object_or_404(Product, id=product_id)
    creator_profile = UserProfile.objects.get(user=product.user)
    comments = product.comments.all() 

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = product
            new_comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('view_product', product_id=product.id)
    else:
        comment_form = CommentForm()

    return render(request, 'product/view_product.html', {'comment_form': comment_form,'comments': comments, 'product': product, 'user_status': {'username': request.user.username}, 'creator_profile': creator_profile, 'user_group': user_group})
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, является ли текущий пользователь создателем товара
    if request.user == product.user or request.user.is_superuser:
        product.delete()

    return redirect('product') 

def create_product(request):
    profile = UserProfile.objects.all()
    user_status = {
        'username': request.user.username,
    }
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('product') 
    else:
        form = ProductForm()

    return render(request, 'product/create_product.html', {'form': form, 'user_group': user_group,'user_status': user_status})

def my_products(request):
    user_status = {
        'username': request.user.username,
    }

    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
        
    if request.user.is_authenticated:
        
        user_products = Product.objects.filter(user=request.user)
        return render(request, 'product/my_products.html', {'user_products': user_products, 'user_group': user_group, 'user_status': user_status})
    else:
        return render(request, 'product/my_products.html', {'user_products': [], 'user_group': user_group, 'user_status': user_status})