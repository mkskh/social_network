from django.shortcuts import render
import random

from user.models import UserProfile
from .forms import SearchForm


def search(request):
    
    profile = UserProfile.objects.get(user=request.user)
    form = SearchForm()

    #recommended profiles
    all_profiles = UserProfile.objects.all()

    sorted_profiles_list = []

    for profile_item in all_profiles:
        if profile_item == profile:
            pass
        else:
            sorted_profiles_list.append(profile_item)
    
    recommended_profiles = random.sample(sorted_profiles_list, 4)

    return render(request, 'search/search.html', {'recommended_profiles': recommended_profiles, 'form': form})
