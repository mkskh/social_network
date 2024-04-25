from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404


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


def user_profile_page(request, user_id):
    # ensure that user is logged in/authenticated to access profile pages.
    if not request.user.is_authenticated:
        raise Http404("You must be logged in to access this page")
    
    user = User.objects.get(pk=user_id)
    user_profile = user.userprofile

    context = {
        'user_profile': user_profile,
        'user': user, # passing the whole user object for more flexibility.
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    return render(request, 'user/profile_page_temp.html', context)