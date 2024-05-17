from django.urls import path
from . import views


app_name = "users_api"

urlpatterns = [
    path('user/create/', views.ApiUserCreate.as_view()),
    path('user/create_bulk/', views.BulkCreateUsers.as_view()),
    path('user/get/<int:pk>/', views.ApiUserGet.as_view()),
    path('user/list/', views.ApiUserList.as_view()),
    path('user/update/<int:pk>/', views.ApiUserUpdate.as_view()),
    path('user/delete/<int:pk>/', views.ApiUserDelete.as_view()),

    path('profile/create/', views.ApiUserProfileCreate.as_view()),
    path('profile/create_bulk/', views.BulkCreateUserProfile.as_view()),
    path('profile/get/<int:pk>/', views.ApiUserProfileGet.as_view()),
    path('profile/list/', views.ApiUserProfileList.as_view()),
    path('profile/update/<int:pk>/', views.ApiUserProfileUpdate.as_view()),
    path('profile/delete/<int:pk>/', views.ApiUserProfileDelete.as_view()),



]
