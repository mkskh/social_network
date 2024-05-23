from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Album, Photo, Subscription

admin.site.register(UserProfile)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Subscription)
