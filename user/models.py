from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    date_of_modified = models.DateTimeField(auto_now=True, blank=True) 
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, default='user_images/dummy-profile-picture.png')
    description = models.CharField(max_length=300, blank=True, null=True)
    background_image = models.ImageField(upload_to='background_images/', blank=True, null=True, default='background_images/dummy_background_img.jpg')
    
    def __str__(self):
        return self.user.username
    
    def age(self):
        if self.date_of_birth:
            today = datetime.today().date()
            dob = self.date_of_birth
            age = today.year - dob.year
            return age
        else:
            return None
    
    def capitalized_gender(self):
        if self.gender:
            return (self.gender).capitalize()
        else:
            return None
    
    def dob_another_format(self):
        if self.date_of_birth:
            input_date_string = str(self.date_of_birth)
            parsed_date = datetime.strptime(input_date_string, "%Y-%m-%d")
            formatted_date = parsed_date.strftime("%d %B %Y")
            return (formatted_date)
        else:
            return None
    
    def count_subscribers(self):
        return self.subscribers.count()
    
    def count_subscribed_to(self):
        return self.subscriptions.count()



class Album(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.profile.user.username}"


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='album_photos/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id} in {self.album.title} by {self.album.profile.user.username}"


class Subscription(models.Model):
    subscriber = models.ForeignKey(UserProfile, related_name="subscriptions", on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(UserProfile, related_name="subscribers", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subscriber} subscribed to {self.subscribed_to}"