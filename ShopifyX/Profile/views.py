from django.shortcuts import render, redirect
from django.contrib import messages
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
            messages.success(request, 'Your profile has been updated!')
            return redirect('profiles')
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
        'is_superuser': request.user.is_superuser,
        'username': request.user.username,
    }
    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name
    context = {
        'profiles': profiles,
        'user_status': user_status,
        'user_group': user_group
    }
    return render (request, 'profile/news_profiles.html', context)


class ProfileDetailViews(DetailView):
    model = UserProfile
    template_name = 'profile/detail_views.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ваш код для определения user_group
        user_group = None
        if self.request.user.groups.exists():
            user_group = self.request.user.groups.first().name
        

        context['user_group'] = user_group

        # Добавление профиля в контекст
        context['profile'] = self.object

        return context

        
class ProfileDeleteViews(DeleteView):
    model = UserProfile
    success_url = '/profile/news/'
    template_name = 'profile/delete.html'

