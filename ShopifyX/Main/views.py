from django.contrib import messages 
from .forms import *
from .models import *
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from Profile.models import *
from django.contrib.auth.models import Group



@login_required
def donate_overlord(request):
    current_group = get_user_group(request.user)
    
    if current_group == 'King' or current_group == 'Dragon' or current_group == 'Admin':
        messages.error(request, 'You cannot downgrade your support tier.')
        return redirect('donate')
    if current_group == 'Overlord':
        messages.error(request, "You can't buy a Overlord again")
        return redirect('donate')
    overlord_group, created = Group.objects.get_or_create(name='Overlord')
    
    request.user.groups.clear()
    request.user.groups.add(overlord_group)
    
    messages.success(request, 'You are now an Overlord!')
    return redirect('donate')

@login_required
def donate_King(request):
    current_group = get_user_group(request.user)
    
    if current_group == 'Dragon' or current_group == 'Admin':
        messages.error(request, 'You cannot downgrade your support tier.')
        return redirect('donate')
    if current_group == 'King':
        messages.error(request, "You can't buy a King again")
        return redirect('donate')
    king_group, created = Group.objects.get_or_create(name='King')
    
    request.user.groups.clear()
    request.user.groups.add(king_group)
    
    messages.success(request, 'You are now a King!')
    return redirect('donate')

@login_required
def donate_Dragon(request):
    current_group = get_user_group(request.user)
    if current_group == 'Admin':
        messages.error(request, 'You cannot downgrade your support tier.')
        return redirect('donate')
    if current_group == 'Dragon':
        messages.error(request, "You can't buy a dragon again")
        return redirect('donate')
    
    dragon_group, created = Group.objects.get_or_create(name='Dragon')
    
    request.user.groups.clear()
    request.user.groups.add(dragon_group)
    
    messages.success(request, 'You are now a Dragon!')
    return redirect('donate')

def get_user_group(user):
    groups = user.groups.values_list('name', flat=True)
    return groups[0] if groups else None


def donate(request):
    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
   
    user_status = {

        'username': request.user.username,
    }
    return render(request, 'main/donate.html', {'user_status': user_status, 'user_profile': user_profile, 'user_group': user_group})

def home_page(request):
    profile = UserProfile.objects.all()
    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
        
    user_status = {
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'username': request.user.username,
    }
    return render(request, 'main/home.html', {'user_status': user_status, 'profiles': profile, 'user_profile': user_profile, 'user_group': user_group})

def about(request):
    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None

    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
        
    user_status = {
        'username': request.user.username,
    }
    return render(request, 'main/about.html', {'user_status': user_status, 'user_profile': user_profile, 'user_group': user_group})

def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_profile = form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            login(request, user)
            return redirect('home_page')  # Replace 'home' with your actual home page URL
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'main/create_user.html', context)

def handler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response