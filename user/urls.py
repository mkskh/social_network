from django.urls import path
from . import views



app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/<int:user_id>/', views.user_profile_page, name='my_user_profile'),
    path('profile/<int:user_id>/edit', views.edit_profile, name='edit_profile'),

    # might add these path after when function is fully done.
    path('profile/<int:user_id>/albums/create/', views.create_album, name='create_album'),
    path('profile/<int:user_id>/albums/', views.album_list, name='album_list'),
    path('profile/<int:user_id>/albums/<int:album_id>/edit/', views.edit_album, name='edit_album'),
    path('profile/<int:user_id>/albums/<int:album_id>/delete/', views.delete_album, name='delete_album'),

    path('profile/<int:user_id>/albums/<int:album_id>/photos/add/', views.create_photo, name='create_photo'),
    path('profile/<int:user_id>/albums/<int:album_id>/photos/', views.photo_list, name='photo_list'),
    path('profile/<int:user_id>/albums/<int:album_id>/photos/<int:photo_id>/delete', views.delete_photo, name='delete_photo'),
    path('profile/<int:user_id>/albums/<int:album_id>/photos/<int:photo_id>/edit', views.edit_photo, name='edit_photo'),

    path('profile/<int:user_id>/albums/<int:album_id>/photos/<int:photo_id>/', views.photo_gallery, name='photo_gallery')
]
