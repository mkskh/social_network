from django.contrib import admin
from .models import ApiUser, ApiUserProfile

# Register your models here.
admin.site.register(ApiUser)
admin.site.register(ApiUserProfile)