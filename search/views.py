from django.shortcuts import render, redirect
import random
import requests
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

from user.models import UserProfile, Subscription
from .forms import SearchForm
from user.forms import SubscriptionForm


@login_required
def search(request):

    #API
    load_dotenv()
    url_profile = "http://127.0.0.1:9000/profile/list/"
    url_user = "http://127.0.0.1:9000/user/list/"

    token = os.getenv('TOKEN')
    headers = {
        "Authorization": f"token {token}"
    }


    authenticated_profile = UserProfile.objects.get(user=request.user)

    #recommended profiles
    all_profiles = UserProfile.objects.exclude(user=request.user)

    all_profiles_with_status = []

    for profile in all_profiles:
        is_subscribed = Subscription.objects.filter(subscriber=authenticated_profile, subscribed_to=profile).exists()
        all_profiles_with_status.append({
            'profile': profile,
            'is_subscribed': is_subscribed,
        })


    if request.method == "GET":
        searched = False

        form = SearchForm()
        sub_form = SubscriptionForm()

        recommended_profiles = random.sample(list(all_profiles), 4)

        recommended_profiles_with_status = []

        for profile in recommended_profiles:
            is_subscribed = Subscription.objects.filter(subscriber=authenticated_profile, subscribed_to=profile).exists()
            recommended_profiles_with_status.append({
                'profile': profile,
                'is_subscribed': is_subscribed
            })


        try:
            response_profile = requests.get(url_profile, headers=headers).json()
            response_user = requests.get(url_user, headers=headers).json()

            return render(request, 'search/search.html', {'all_profiles_with_status': all_profiles_with_status,
                                                    'form': form, 'searched': searched,
                                                    'sub_form': sub_form,
                                                    'recommended_profiles_with_status': recommended_profiles_with_status,
                                                    'response_profile': response_profile,
                                                    'response_user': response_user})
        except:
            pass

        return render(request, 'search/search.html', {'all_profiles_with_status': all_profiles_with_status,
                                                    'form': form, 'searched': searched,
                                                    'sub_form': sub_form,
                                                    'recommended_profiles_with_status': recommended_profiles_with_status,})

    elif request.method == "POST":
        searched = True

        form = SearchForm(request.POST)
        sub_form = SubscriptionForm(request.POST)

        if form.is_valid():

            key = str(form.cleaned_data['search']).lower()
            location = form.cleaned_data['city']
            gender = form.cleaned_data['gender']
            age_more_than = form.cleaned_data['age_more_than']
            age_less_than = form.cleaned_data['age_less_than']

            search_res = []

            for item in all_profiles:
                if not key:
                    search_res.append(item)
                else:
                    if key in str(item.user.first_name).lower() or key in str(item.user.last_name).lower():
                        search_res.append(item)
            
            if location:
                search_res = [item for item in search_res if str(item.location).lower() == str(location).lower()]

            if gender:
                search_res = [item for item in search_res if item.gender == gender]

            if age_more_than:
                search_res = [item for item in search_res if int(item.age()) > age_more_than]

            if age_less_than:
                search_res = [item for item in search_res if int(item.age()) < age_less_than]

            quantity = len(search_res)

            search_res_with_status = []

            for profile in search_res:
                is_subscribed = Subscription.objects.filter(subscriber=authenticated_profile, subscribed_to=profile).exists()
                search_res_with_status.append({
                    'profile': profile,
                    'is_subscribed': is_subscribed,
                })
            
            # API 

            try:
                response_profile = requests.get(url_profile, headers=headers).json()
                response_user = requests.get(url_user, headers=headers).json()
                
                search_res_user = []

                for item in response_user:
                    if not key:
                        search_res.append(item)
                    else:
                        if key in str(item['first_name']).lower() or key in str(item['last_name']).lower():
                            search_res_user.append(item)
                
                if location:
                    response_profile = [item  for item in response_profile if str(item['location']).lower() == str(location).lower()]
                
                if gender:
                    response_profile = [item for item in response_profile if item['gender'] == gender]
                    

                if age_more_than:
                    response_profile = [item for item in response_profile if int(item['age']) > age_more_than]
                    

                if age_less_than:
                    response_profile = [item for item in response_profile if int(item['age']) < age_less_than]
                
                if not search_res_user:
                    search_res_user = response_user
                
                return render(request, 'search/search.html', {'search_res_with_status': search_res_with_status,
                                                            'form': form,
                                                            'searched': searched,
                                                            'search_res_profile': response_profile,
                                                            'search_res_user': search_res_user})
            except:
                pass

        # Subscription
        profile_id = request.POST.get('profile_id')
        
        if profile_id:
            if sub_form.is_valid():
                profile_id = sub_form.cleaned_data['profile_id']
                subscriber_profile = request.user.userprofile
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

        return render(request, 'search/search.html', {'search_res_with_status': search_res_with_status, 'form': form, 'searched': searched})
