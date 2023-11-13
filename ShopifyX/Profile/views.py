from django.shortcuts import render, redirect
# Create your views here.
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView


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

    return render(request, 'profile/profile.html', {'form': form})

def news_profile(request):
    profiles = UserProfile.objects.all()
    return render (request, 'profile/news_profiles.html', {'profiles': profiles})

class ProfileDetailViews(DetailView):
    model = UserProfile
    template_name = 'profile/detail_views.html'
    context_object_name = 'profile'

class ProfileDeleteViews(DeleteView):
    model = UserProfile
    success_url = '/profile/news/'
    template_name = 'profile/delete.html'

