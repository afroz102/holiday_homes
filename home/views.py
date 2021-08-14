from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
# from django.core.paginator import Paginator  # To help with pagination
# from django.http import JsonResponse

# import os
# import csv
# import json
# from django.conf import settings


# from .Google import Create_Service
# import base64
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# Dashboard
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    print("user: ", user)

    # CLIENT_SECRET_FILE = 'gmail_client_secret.json'
    # API_NAME = 'gmail'
    # API_VERSION = 'v1'
    # SCOPES = ['https://mail.google.com/']

    # service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # print("service: ", service)

    # emailMsg = 'This email is for gmail api code testing. I hope this works'
    # mimeMessage = MIMEMultipart()
    # mimeMessage['to'] = 'sahilraza102@gmail.com'
    # mimeMessage['subject'] = 'Test'
    # mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    # raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    # message = service.users().messages().send(
    #     userId='me',
    #     body={'raw': raw_string}
    # ).execute()

    # print("message: ", message)

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
