from django.shortcuts import render
import random
from . import models
from user.models import UserProfile
from .forms import PublishPostForm


def news_feed(request):

    if request.method == "GET":

        form = PublishPostForm()
        posts = models.Post.objects.all()
        profile = UserProfile.objects.get(user=request.user)
        all_profiles = UserProfile.objects.all()

        sorted_profiles_list = []

        for profile_item in all_profiles:
            if profile_item == profile:
                pass
            else:
                sorted_profiles_list.append(profile_item)
        
        recommended_profiles = random.sample(sorted_profiles_list, 4)

    return render(request, 'feed/news_feed.html', 
                {'posts': posts, 'profile': profile, 'recommended_profiles': recommended_profiles, 'form': form})