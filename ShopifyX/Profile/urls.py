from django.urls import path, include
from .views import *
urlpatterns = [
    path('', profile, name='profiles'),
    path('news/', news_profile, name='profile'),
    path('news/<int:pk>', ProfileDetailViews.as_view(), name='profile_detail'),
    path('news/<int:pk>/delete', ProfileDeleteViews.as_view(), name='delete_detail')
]