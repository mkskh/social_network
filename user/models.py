from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    date_of_modified = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateTimeField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    description = models.CharField(max_length=300)
    
    def __str__(self):
        return self.user.username
