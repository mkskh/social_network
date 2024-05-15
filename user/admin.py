from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Album, Photo

admin.site.register(UserProfile)
admin.site.register(Album)
admin.site.register(Photo)