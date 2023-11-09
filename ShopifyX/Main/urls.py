from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
urlpatterns = [

    path('', home_page, name='home_page'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='main/logout.html'), name='logout'),
    path("regiser/", registration, name='register'),
]
