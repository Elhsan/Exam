from django.contrib import messages 
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import JsonResponse
from Profile.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from Profile.models import *
from django.contrib.auth.models import Group

def donate_overlord(request):
   
    overlord_group, created = Group.objects.get_or_create(name='Overlord')
    
    request.user.groups.clear()

    request.user.groups.add(overlord_group)
    
    messages.success(request, 'Вы теперь overlord')
    return redirect('donate')

def donate_King(request):
   
    King_group, created = Group.objects.get_or_create(name='King')
    
    request.user.groups.clear()

    request.user.groups.add(King_group)
    
    messages.success(request, 'Вы теперь King')
    return redirect('donate')

def donate_Dragon(request):
   
    Dragon_group, created = Group.objects.get_or_create(name='Dragon')
    
    request.user.groups.clear()

    request.user.groups.add(Dragon_group)
    
    messages.success(request, 'Вы теперь Dragon')
    return redirect('donate')

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


    