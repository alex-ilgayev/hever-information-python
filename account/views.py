from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.contrib.auth.models import Group
from oauth2client.crypt import AppIdentityError
from oauth2client.client import verify_id_token
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from report.serializers import *
from report.models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from datetime import date
from datetime import datetime
from django.db import *
from django.shortcuts import redirect
import json
import re


# permission system:
# 1. client will send each request his google token id (in header).
# 2. each request the backend will do the following:
#     2.1. check if the user is logged in.
#     2.2. if not logged:
#         2.2.1 validates the google token id against google servers.
#         2.2.2 retrieves the user according to google email. (creates new user if not exist)
#         2.2.3 logs in to the user for the rest of the requests.
#     2.3. check user permission for the action:
#         2.3.2 if its reports / report entries
#             2.3.2.1 only if user belongs to the group for the unit of the group


CONSTANT_PASSWORD = 'Aa123456'

@api_view(['GET'])
def create_user(request):
    user_name = request.GET.get('user_name')
    if user_name is None:
        return Response('please include a user name', status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(user_name, password=CONSTANT_PASSWORD)
        user.save()
    except IntegrityError:
        return Response('user name already exist', status=status.HTTP_409_CONFLICT)
    return Response('user created successfully', status=status.HTTP_201_CREATED)


@api_view(['GET'])
def create_group(request):
    group_name = request.GET.get('group_name')
    if group_name is None:
        return Response('please include a group name', status=status.HTTP_400_BAD_REQUEST)

    new_group, created = Group.objects.get_or_create(name='new_group')
    if not created:
        return Response('group is has not been created (already exists with the same name ?)')

    return Response('group created successfully', status=status.HTTP_201_CREATED)

# checks the integrity of the google token id (passed via 'google-token-id' parameter.
# if valid then logs when email is the username, and password is constant.

@api_view(['GET'])
def signin(request):
    next_path = request.GET.get('next')
    google_token_id = request.GET.get('google-token-id')
    if google_token_id is None:
        return Response('no token is provided', status=status.HTTP_403_FORBIDDEN)

    # Update client_secrets.json with your Google API project information.
    # Do not change this assignment.
    CLIENT_ID = json.loads(
        open('client_secret.json', 'r').read())['web']['client_id']

    try:
        # Client library can verify the ID token.
        jwt = verify_id_token(google_token_id, CLIENT_ID)
        gid = jwt['sub']
        email = jwt['email']

        # checks if user exists. if not, then creates.
        exists = User.objects.all().filter(username=email).exists()
        if not exists:
            if next_path is not None:
                return redirect('/account/signup/?user_name=' + email + '&next=/account/signin/?next=' + next_path)
            else:
                return redirect('/account/signup/?user_name=' + email)
        # up to now validated google token id. now logs in using django auth system.
        user = authenticate(username=email, password=CONSTANT_PASSWORD)

        # shouldn't happen
        if user is None:
            return Response('login error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        login(request, user=user)
        return Response('successful login to ' + str(user), status=status.HTTP_200_OK)

    except AppIdentityError:
        return Response('google token id provided is invalid', status=status.HTTP_403_FORBIDDEN)

    if next_path is None:
        return Response(status=status.HTTP_200_OK)
    return redirect(next_path)

