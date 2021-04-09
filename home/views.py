from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
# from django.core.paginator import Paginator  # To help with pagination
# from django.http import JsonResponse

# import os
# import csv
# import json
# from django.conf import settings


# Dashboard
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    print("user: ", user)
    context = {}
    try:
        userProfile = UserProfile.objects.get(user=user)
        context['userProfile'] = userProfile
    except UserProfile.DoesNotExist:
        print("Profile does not exists")
        pass

    return render(request, 'home/dashboard.html', context)


@login_required(login_url='login')
def getAgencyProfilePage(request):
    # user = request.user

    context = {}
    if request.method == 'POST':
        pass

    return render(request, 'home/agency_profile_page.html', context)
