from django.db import models

# Create your models here.
class ApiUser(models.Model):
    '''Fields for user instance'''
    username = models.CharField(max_length=150, blank=False, null=False)
    last_login = models.DateTimeField()
    first_name = models.CharField(max_length=70, blank=False, null=False)
    last_name = models.CharField(max_length=70, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.username



class ApiUserProfile(models.Model):
    '''fields for user profile instance'''

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(ApiUser, on_delete=models.CASCADE, related_name='userprofile')
    date_of_modified = models.DateTimeField(auto_now=True, blank=True) 
    date_of_birth = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.user.username
