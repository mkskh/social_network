from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

from .forms import RegistrationForm
from .models import ApiUser, ApiUserProfile

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser
from .serializers import UserSerializer, UserProfileSerializer

# Create your views here.
def home(request):

    return render(request, 'users_api/home_api.html')


def registration(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, 'users_api/registration_api.html', {"form": form})
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('/login/')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, 'users_api/registration_api.html', {"form": form})


def user_login(request):

    if request.method == "GET":
        return render(request, 'users_api/login_api.html', {})
    
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
            return render(request, 'users_api/login_api.html', {})


def user_logout(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('/')





# user API part.
class ApiUserCreate(generics.CreateAPIView):
    '''Create new single user instance through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class BulkCreateUsers(generics.CreateAPIView):
    ''' Create many users instances through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.request.query_params.get('id', None)
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=id)
        self.check_object_permissions(self.request, obj)
        return obj


class ApiUserDelete(generics.RetrieveDestroyAPIView):
    '''Delete a user from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        id = self.request.query_params.get('id', None)
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=id)
        self.check_object_permissions(self.request, obj)
        return obj


class ApiUserList(generics.ListAPIView):
    '''list of users from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ApiUserUpdate(generics.UpdateAPIView):
    '''Update the UserProfile through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        id = self.request.query_params.get('id', None)
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=id)
        self.check_object_permissions(self.request, obj)
        return obj


# User_profile API part.
class ApiUserProfileCreate(generics.CreateAPIView):
    '''Create new user through the API'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class BulkCreateUserProfile(generics.CreateAPIView):
    '''Create several users instance at once'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        id = self.request.query_params.get('id', None)
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=id)
        self.check_object_permissions(self.request, obj)
        return obj



class ApiUserProfileDelete(generics.RetrieveDestroyAPIView):
    '''Delete a user profile fron api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        id = self.request.query_params.get('id', None)
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=id)
        self.check_object_permissions(self.request, obj)
        return obj


class ApiUserProfileList(generics.ListAPIView):
    '''list of users profile from api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    
class ApiUserProfileUpdate(generics.UpdateAPIView):
    '''Update the UserProfile through the API'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        id = self.request.query_params.get('id', None)
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=id)
        self.check_object_permissions(self.request, obj)
        return obj