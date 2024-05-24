from rest_framework import serializers

from .models import ApiUser, ApiUserProfile




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUserProfile
        fields = '__all__'

