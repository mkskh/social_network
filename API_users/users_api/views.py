from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserProfileSerializer
from .models import ApiUser, ApiUserProfile


# user API part.
class ApiUserCreate(generics.CreateAPIView):
    '''Create new single user instance through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer


class BulkCreateUsers(generics.CreateAPIView):
    ''' Create many users instances through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApiUserGet(generics.RetrieveAPIView):
    '''get a user instance from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class ApiUserDelete(generics.RetrieveDestroyAPIView):
    '''Delete a user from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer


class ApiUserList(generics.ListAPIView):
    '''list of users from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer


class ApiUserUpdate(generics.UpdateAPIView):
    '''Update the UserProfile through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer


# User_profile API part.
class ApiUserProfileCreate(generics.CreateAPIView):
    '''Create new user through the API'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer


class BulkCreateUserProfile(generics.CreateAPIView):
    '''Create several users instance at once'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApiUserProfileGet(generics.RetrieveAPIView):
    '''get a user profile from api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'


class ApiUserProfileDelete(generics.RetrieveDestroyAPIView):
    '''Delete a user profile fron api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'


class ApiUserProfileList(generics.ListAPIView):
    '''list of users profile from api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ApiUserProfileUpdate(generics.UpdateAPIView):
    '''Update the UserProfile through the API'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer