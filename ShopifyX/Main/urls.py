from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', home_page, name='home_page'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path("regiser/", registration, name='register'),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/login/', include('allauth.urls'), name='google_login'),
]
