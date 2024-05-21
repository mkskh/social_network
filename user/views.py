from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, UserEditProfileForm, AlbumForm, PhotoForm, SubscriptionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from .models import UserProfile, Album, Photo, Subscription
from feed.forms import LeaveCommentForm
from feed.forms import Comment

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
    passed_user = User.objects.get(pk=user_id)
    passed_profile = UserProfile.objects.get(user=passed_user)
    authenticated_profile = UserProfile.objects.get(user=request.user)

    posts_passed_profile = Post.objects.filter(profile=passed_profile).order_by('-created_at')
    albums = Album.objects.filter(profile=passed_profile).prefetch_related('photos')

    try:
        button_status = Subscription.objects.get(subscriber=authenticated_profile, subscribed_to=passed_profile)
    except:
        button_status = False

    if request.method == "GET":
        comment_form = LeaveCommentForm()
        sub_form = SubscriptionForm()

    if request.method == "POST":
        comment_form = LeaveCommentForm(request.POST)
        sub_form = SubscriptionForm(request.POST)

        # COMMENT
        post_id = request.POST.get('post_id_comment')
        try:
            post_obj = Post.objects.get(id=post_id)
        except:
            post_obj = None
        if post_obj:
            if comment_form.is_valid():
                text = comment_form.cleaned_data['text']
                
                comment = Comment.objects.create(profile=authenticated_profile, text=text, post=post_obj)
                comment.save()
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                pass
        
        # Subscription
        profile_id = request.POST.get('profile_id')
        
        if profile_id:
            if sub_form.is_valid():
                profile_id = sub_form.cleaned_data['profile_id']
                subscriber_profile = request.user.userprofile
                print(subscriber_profile)
                subscribed_to_profile = UserProfile.objects.get(user_id=profile_id)

                # Check if a subscription already exists
                subscription_exists = Subscription.objects.filter(
                    subscriber=subscriber_profile,
                    subscribed_to=subscribed_to_profile
                ).exists()

                # Create or delete the subscription
                if subscription_exists:
                    Subscription.objects.filter(
                        subscriber=subscriber_profile,
                        subscribed_to=subscribed_to_profile
                    ).delete()
                else:
                    Subscription.objects.create(
                        subscriber=subscriber_profile,
                        subscribed_to=subscribed_to_profile
                    )
                
                return redirect(request.META.get('HTTP_REFERER', '/'))


    context = {
        'profile_user': passed_user, # passing the whole user object for more flexibility.
        'profile': passed_profile,
        'posts': posts_passed_profile,
        'albums': albums,
        'authenticated_profile': authenticated_profile,
        'button_status': button_status,
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





def create_album(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.profile = user_profile
            new_album.save()
            return redirect('user:album_list', user_id=user_id)
    else:
        form = AlbumForm()
    return render(request, 'user/create_album.html', {
        'form': form,
        'profile_user': user_profile
    })

def album_list(request, user_id):
    ''' Users can access albums page'''
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    albums = Album.objects.filter(profile=user_profile)
    is_owner = request.user.userprofile == user_profile
    return render(request, 'user/album_list.html', {
        'albums': albums,
        'is_owner': is_owner,
        'profile_user': user_profile.user
    })


def edit_album(request, user_id, album_id):
    ''' User owner of the profile/album can edit it.'''
    album = get_object_or_404(Album, id=album_id, profile__user__id=user_id)
    if request.user.userprofile.id != album.profile.id:
        messages.error(request, "You do not have permission to edit this album.")
        return redirect('user:album_list', user_id=user_id)

    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, "Album updated successfully.")
            return redirect('user:album_list', user_id=user_id)
    else:
        form = AlbumForm(instance=album)

    return render(request, 'user/edit_album.html', {
        'form': form,
        'album': album
    })



@login_required
def delete_album(request, user_id, album_id):
    ''' User can delete their own albums.'''
    album = get_object_or_404(Album, id=album_id, profile__user_id=user_id)

    # Check if the logged-in user is the owner of the album
    if request.user.id == user_id:
        album.delete()
        return redirect('user:album_list', user_id=user_id)
    else:
        messages.error(request, "You do not have permission to delete this album.")
        return redirect('user:album_list', user_id=user_id)


def create_photo(request, album_id, user_id):
    '''User can add photos to an album'''
    album = get_object_or_404(Album, id=album_id)
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = form.save(commit=False)
            new_photo.album = album
            new_photo.save()
            return redirect('user:photo_list', user_id=user_id, album_id=album_id)
    else:
        form = PhotoForm()
    return render(request, 'user/create_photo.html', {
        'form': form,
        'album': album,
        'profile_user': user_profile.user
    })

def photo_list(request, user_id, album_id):
    ''' Users can access photos page'''
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    album = get_object_or_404(Album, id=album_id)
    photos = album.photos.all()
    is_owner = request.user.userprofile == user_profile
    return render(request, 'user/photo_list.html', {
        'album': album,
        'photos': photos,
        'is_owner': is_owner,
        'profile_user': user_profile.user
    })




@login_required
def delete_photo(request, user_id, album_id, photo_id):
    ''' User can delete it their own photos '''
    photo = get_object_or_404(Photo, id=photo_id, album__id=album_id, album__profile__user_id=user_id)

    # Check if the logged-in user is the owner of the photo's album
    if request.user.id == user_id:
        photo.delete()
        return redirect('user:photo_list', user_id=user_id, album_id=album_id)
    else:
        messages.error(request, "You do not have permission to delete this photo.")
        return redirect('user:photo_list', user_id=user_id, album_id=album_id)



def edit_photo(request, user_id, album_id, photo_id):
    ''' User can edit their own photos '''
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    album = get_object_or_404(Album, id=album_id)
    photo = get_object_or_404(Photo, id=photo_id, album=album)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('user:photo_list', user_id=user_id, album_id=album_id)
    else:
        form = PhotoForm(instance=photo)

    return render(request, 'user/edit_photo.html', {
        'form': form,
        'album': album,
        'photo': photo,
        'profile_user': user_profile.user
    })
