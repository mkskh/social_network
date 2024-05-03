from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserEditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from .models import UserProfile

from feed.models import Post, Like


def registration(request):

    if request.method == "GET":
        form = RegistrationForm()
        return render(request, 'user/registration.html', {"form": form})
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/user/login/')
        else:
            error = "You put wrong information. Please try again"
            return render(request, 'user/registration.html', {"form": form, "error": error})


def user_login(request):

    if request.method == "GET":
        return render(request, 'user/login.html', {})
    
    elif request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('/')
        else:
            messages.error(request, ("Incorrect information were provided. Please try again"))
            return render(request, 'user/login.html', {})


def user_logout(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('/')

@login_required
def user_profile_page(request, user_id):
    ''' Users can access profiles page'''   
    profile_user = User.objects.get(pk=user_id)
    user_profile = profile_user.userprofile

    posts = Post.objects.filter(profile=user_profile).order_by('-created_at')

    context = {
        'profile_user': profile_user, # passing the whole user object for more flexibility.
        'user_profile': user_profile,
        'posts': posts,
    }
    return render(request, 'user/profile_page.html', context)



@login_required
def edit_profile(request, user_id):
    ''' User logged in can edit their own profile'''
    if request.user.id != user_id:
        raise Http404("You are not authorized to edit this profile.")
        
    user_profile = get_object_or_404(UserProfile, user__id=user_id)  # Ensures that the profile belongs to the logged-in user

    if request.method == 'POST':
        form = UserEditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user:my_user_profile', user_id=user_id)
    else:
        messages.error(request, ("Incorrect information were provided. Please try again"))
        form = UserEditProfileForm(instance=request.user.userprofile)
    return render(request, 'user/edit_profile.html', {'form': form})



# want to implement the view of feeds. post of the user.
# should appear as '' your publications'

