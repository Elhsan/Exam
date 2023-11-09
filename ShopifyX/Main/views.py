from django.contrib import messages 
from django.shortcuts import render, redirect
from .forms import UserForm
from .usecases import *
from .models import *
def home_page(request):
    return render(request, 'main/home.html')

def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request,
                             f"Welcome to our site {username}!")
            form.save(commit=True)
            context = {'user': request.user}
            return render(request, 'main/home.html', context)
        else:
            messages.error(request,
                           "Please correct the errors below.")
            context = {'form': form}
            return render(request, 'main/create_user.html', context)

    context = {'form': UserForm()}
    return render(request, 'main/create_user.html', context)