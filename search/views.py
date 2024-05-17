from django.shortcuts import render
import random

from user.models import UserProfile
from .forms import SearchForm


def search(request):

    form = SearchForm(request.POST or None)
    profile = UserProfile.objects.get(user=request.user)

    #recommended profiles
    all_profiles = UserProfile.objects.all()

    sorted_profiles_list = []

    # get all users except the one who is logged in
    for profile_item in all_profiles:
        if profile_item == profile:
            pass
        else:
            sorted_profiles_list.append(profile_item)
    
    

    if request.method == "GET":
        searched = False

        recommended_profiles = random.sample(sorted_profiles_list, 4)

        return render(request, 'search/search.html', {'recommended_profiles': recommended_profiles, 'sorted_profiles_list': sorted_profiles_list,'form': form, 'searched': searched})

    elif request.method == "POST" and form.is_valid():
        searched = True

        key = str(form.cleaned_data['search']).lower()
        location = form.cleaned_data['city']
        gender = form.cleaned_data['gender']
        age_more_than = form.cleaned_data['age_more_than']
        age_less_than = form.cleaned_data['age_less_than']

        search_res = []

        for item in sorted_profiles_list:
            if not key:
                search_res.append(item)
            else:
                if key in str(item.user.first_name).lower() or key in str(item.user.last_name).lower():
                    search_res.append(item)
        
        if location:
            search_res = [item for item in search_res if item.location == location]

        if gender:
            search_res = [item for item in search_res if item.gender == gender]

        if age_more_than:
            search_res = [item for item in search_res if int(item.age()) > age_more_than]

        if age_less_than:
            search_res = [item for item in search_res if int(item.age()) < age_less_than]

        quantity = len(search_res)

        return render(request, 'search/search.html', {'search_res': search_res, 'form': form, 'searched': searched})
