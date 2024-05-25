from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import random
from django.contrib import messages
import markdown2

from . import models
from user.models import UserProfile, Subscription
from .models import Post, Like, Comment
from .forms import PublishPostForm, LeaveCommentForm


def news_feed(request):

    # all people from subscriptions and people who have posts (rest_posts) /// We need it for recommendation section
    covered_people = []

    # Collect the posts from subscriptions
    posts_from_subscriptions = []

    all_subscriptions = request.user.userprofile.subscriptions.all()
    for subscription in all_subscriptions:
        covered_people.append(subscription.subscribed_to)
        for post in subscription.subscribed_to.posts.all():
            posts_from_subscriptions.append(post)
    for post in request.user.userprofile.posts.all():
        posts_from_subscriptions.append(post)
    
    posts_from_subscriptions.sort(key=lambda post: post.created_at, reverse=True)

    # Collect the rest of the posts
    rest_posts = []

    posts = models.Post.objects.all()
    for post in posts:
        if post not in posts_from_subscriptions:
            rest_posts.append(post)

    rest_posts.sort(key=lambda post: post.created_at, reverse=True)


    #RECOMMENDATION section
    my_profile = UserProfile.objects.get(user=request.user)
    recommended_profiles = set()

    for post in rest_posts:
        if post.profile == my_profile:
            pass
        else:
            recommended_profiles.add(post.profile)
    
    if len(list(recommended_profiles)) <= 4:
        for profile in list(recommended_profiles):
            covered_people.append(profile)
        
        quantity_profiles_needed = 5 - len(recommended_profiles)

        all_profiles = UserProfile.objects.exclude(user=request.user)
        all_additional_profiles_list = []

        for profile_item in all_profiles:
            if profile_item not in covered_people:
                all_additional_profiles_list.append(profile_item)
    
        additional_profiles = random.sample(all_additional_profiles_list, min(quantity_profiles_needed, len(all_additional_profiles_list))) if len(all_additional_profiles_list) > (quantity_profiles_needed - 1) else all_additional_profiles_list

        recommended_profiles_result = list(recommended_profiles) + additional_profiles

    elif len(list(recommended_profiles)) >= 5:

        recommended_profiles_result = random.sample(list(recommended_profiles), min(5, len(list(recommended_profiles)))) if len(list(recommended_profiles)) > 4 else list(recommended_profiles)


    if request.method == "GET":

        form = PublishPostForm()
        comment_form = LeaveCommentForm()
        
    if request.method == "POST":

        form = PublishPostForm(request.POST, request.FILES)
        comment_form = LeaveCommentForm(request.POST)

        post_id = request.POST.get('post_id_comment')
        try:
            post_obj = Post.objects.get(id=post_id)
        except:
            post_obj = None

        if post_obj:
            if comment_form.is_valid():
                text = comment_form.cleaned_data['text']
                
                comment = Comment.objects.create(profile=my_profile, text=text, post=post_obj)
                comment.save()
                messages.success(request, "You have added a comment.")
                return redirect('/feed/')
            else:
                messages.error(request, "Form is not valid. Please check your input.")


        if form.is_valid():
            text = markdown2.markdown(form.cleaned_data['text'])
            image = form.cleaned_data['image']
            post = Post.objects.create(profile=my_profile, text=text, image=image)
            post.save()
            messages.success(request, "You have added a new post.")
            return redirect('/feed/')
        else:
            messages.error(request, "Form is not valid. Please check your input.")

    return render(request, 'feed/news_feed.html', 
                {'posts': posts_from_subscriptions, 
                'profile': my_profile, 
                'recommended_profiles': recommended_profiles_result, 
                'form': form, 
                'comment_form': comment_form,
                'rest_posts': rest_posts})


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


def delete_post(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            messages.success(request, "Post deleted successfully.")
        except Post.DoesNotExist:
            messages.error(request, "Post does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('/feed/')