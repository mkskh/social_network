from django.db import models
from user.models import UserProfile


class Post(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, blank=True) 
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    text = models.CharField(max_length=1000)


class Like(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


    def __str__(self):
        return self.headline