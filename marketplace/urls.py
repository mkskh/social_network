from django.urls import path
from . import views


app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace_page, name='marketplace_page'),
    path('about/', views.about, name='about'),
]