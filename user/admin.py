from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile




admin.site.register(UserProfile)

# Mix profile info and profile into one.
class ProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    model = User
    #fields = ['Username']
    inlines = [ProfileInline]

# i think group can be taken off and user & profile put into one in the admin panel.

''' i have seen a editing, where in admin panel, we can take off the 'profile' Have only user showing which will
 have profile inside. As technically each user will have their own profile. and can make it look better and easier 
 when accessing such things. '''