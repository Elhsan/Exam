from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from Product.models import *

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile/profile.html', {'form': form})
 
@login_required
def news_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    user_group = None
    if request.user.groups.exists():
        user_group = request.user.groups.first().name

    user_status = {
        'username': request.user.username,
    }
    products = Product.objects.filter(user=request.user)
    context = {
        'user_profile': user_profile,
        'user_status': user_status,
        'products': products,
        'user_group': user_group
    }
    return render(request, 'profile/news_profiles.html', context)
    
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

