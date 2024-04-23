from django.shortcuts import render
from . import models


def news_feed(request):

    posts = models.Post.objects.all()

    return render(request, 'feed/news_feed.html', {'posts': posts})