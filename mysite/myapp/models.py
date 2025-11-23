from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    level=models.IntegerField()
    email=models.EmailField(unique=True)
    otp=models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    participants=models.ManyToManyField(User, related_name='conversations')
    created_at =models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Converstion {self.id}"

class Message(models.Model):
    conversation=models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content=models.TextField(blank=True)
    file=models.FileField(upload_to='files/', null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return f"{self.sender} : {self.content[:20]}" 

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    def __str__(self):
        return self.user.username