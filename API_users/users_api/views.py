from .models import ApiUser, ApiUserProfile
from rest_framework import generics
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated


# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate


# Create your views here
#------ user API part. --------------
class ApiUserCreate(generics.CreateAPIView):
    '''Create new single user instance through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BulkCreateUsers(generics.CreateAPIView):
    ''' Create many users instances through the API'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ApiUserGet(generics.RetrieveAPIView):
    '''get a user instance from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


class ApiUserDelete(generics.RetrieveDestroyAPIView):
    '''Delete a user from api'''
    queryset = ApiUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


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
    permission_classes = [IsAuthenticated]




# -------   User_profile API part. --------------
class ApiUserProfileCreate(generics.CreateAPIView):
    '''Create new user through the API'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class BulkCreateUserProfile(generics.CreateAPIView):
    '''Create several users instance at once'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class ApiUserProfileGet(generics.RetrieveAPIView):
    '''get a user profile from api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


class ApiUserProfileDelete(generics.RetrieveDestroyAPIView):
    '''Delete a user profile fron api'''
    queryset = ApiUserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]



# if this part is ever needed for some views  to add below the view:  otherwise delete this comment if unnecessary

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data, many=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)