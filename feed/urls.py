from django.urls import path
from . import views


app_name = 'feed'

urlpatterns = [
    path('', views.news_feed, name='news_feed'),
    path('liked/', views.like_unlike_post, name='like_unlike_post'),
]