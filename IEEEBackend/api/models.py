from django.db import models

app_name = 'api'

class Conversation(models.Model):
    Title = models.CharField(max_length=100)
    
class Message(models.Model):
    SENT_BY_CHOICES = ['user','chatbot']

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')  
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    sent_by = models.CharField(max_length=7, choices=SENT_BY_CHOICES)

class Users(models.Model):
    Username = models.CharField(max_length=25)

