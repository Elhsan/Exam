from django.contrib import messages 
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import JsonResponse
from Profile.models import UserProfile

def home_page(request):
    return render(request, 'main/home.html')

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



