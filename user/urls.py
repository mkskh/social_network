from django.urls import path
from . import views



app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/<int:user_id>/', views.user_profile_page, name='my_user_profile'),
    path('profile/<int:user_id>/edit', views.edit_profile, name='edit_profile'),
]

