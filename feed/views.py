from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random
from django.contrib import messages
import markdown2

from . import models
from user.models import UserProfile
from .models import Post, Like, Comment
from .forms import PublishPostForm


def news_feed(request):

    posts = models.Post.objects.all().order_by('-created_at')
    profile = UserProfile.objects.get(user=request.user)

    #recommended profiles
    all_profiles = UserProfile.objects.all()

    sorted_profiles_list = []

    for profile_item in all_profiles:
        if profile_item == profile:
            pass
        else:
            sorted_profiles_list.append(profile_item)
    
    recommended_profiles = random.sample(sorted_profiles_list, 4)

    if request.method == "GET":

        form = PublishPostForm()
        
    if request.method == "POST":

        form = PublishPostForm(request.POST, request.FILES)
        if form.is_valid():
            text = markdown2.markdown(form.cleaned_data['text'])
            image = form.cleaned_data['image']
            post = Post.objects.create(profile=profile, text=text, image=image)
            post.save()
            messages.success(request, "You have added a new post.")
            return redirect('/feed/')
        else:
            messages.error(request, "Form is not valid. Please check your input.")

    return render(request, 'feed/news_feed.html', 
                {'posts': posts, 'profile': profile, 'recommended_profiles': recommended_profiles, 'form': form})


def like_unlike_post(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = UserProfile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(profile=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
            post_obj.save()
            like.save()
        else:
            like.value='Like'

            post_obj.save()
            like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)


