from django.shortcuts import render
from . import models
from user.models import UserProfile


def news_feed(request):

    posts = models.Post.objects.all()
    profile = UserProfile.objects.get(user=request.user)

    return render(request, 'feed/news_feed.html', {'posts': posts, 'profile': profile})