from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')

    def __str__(self):
        name1 = self.participants.all().first()
        name2 = self.participants.all().last()
        return f"Chat between {name1.first_name} and {name2.first_name}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}..."


class ThreadUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')