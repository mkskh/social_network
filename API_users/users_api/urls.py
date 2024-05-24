from django.urls import path
from . import views


app_name = "users_api"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registration, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
  path('user/create/', views.ApiUserCreate.as_view(), name='user-create'),
    path('user/create_bulk/', views.BulkCreateUsers.as_view(), name='user-create-bulk'),
    path('user/get/<int:pk>/', views.ApiUserGet.as_view(), name='user-get'),
    path('user/list/', views.ApiUserList.as_view(), name='user-list'),
    path('user/update/<int:pk>/', views.ApiUserUpdate.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', views.ApiUserDelete.as_view(), name='user-delete'),
    path('profile/create/', views.ApiUserProfileCreate.as_view(), name='profile-create'),
    path('profile/create_bulk/', views.BulkCreateUserProfile.as_view(), name='profile-create-bulk'),
    path('profile/get/<int:pk>/', views.ApiUserProfileGet.as_view(), name='profile-get'),
    path('profile/list/', views.ApiUserProfileList.as_view(), name='profile-list'),
    path('profile/update/<int:pk>/', views.ApiUserProfileUpdate.as_view(), name='profile-update'),
    path('profile/delete/<int:pk>/', views.ApiUserProfileDelete.as_view(), name='profile-delete'),



]
