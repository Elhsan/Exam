from django.shortcuts import render, redirect
# Create your views here.
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):


    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
        user_status = {
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'username': request.user.username,
        }
        context = {
            'form': form,
            'user_status': user_status,
        }

    return render(request, 'profile/profile.html', context)

def news_profile(request):
    profiles = UserProfile.objects.all()
    user_status = {
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'username': request.user.username,
    }
    context = {
        'profiles': profiles,
        'user_status': user_status,
    }
    return render (request, 'profile/news_profiles.html', context)

class ProfileDetailViews(DetailView):
    model = UserProfile
    template_name = 'profile/detail_views.html'
    context_object_name = 'profile'

class ProfileDeleteViews(DeleteView):
    model = UserProfile
    success_url = '/profile/news/'
    template_name = 'profile/delete.html'

