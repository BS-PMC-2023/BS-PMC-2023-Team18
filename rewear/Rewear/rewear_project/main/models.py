from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

#  name , city , address , facebook , description , picture , market_manager , date , capacity , status , rating
class market(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    facebook = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    google_location = models.CharField(max_length=1000, default='')
    market_manager = models.CharField(max_length=200, default='')
    date = models.CharField(max_length=200, default='')
    status = models.CharField(max_length=200, default='')
    rating = models.CharField(max_length=200, default='')
    # wear items
    shirt = models.IntegerField(default=0)
    pants = models.IntegerField(default=0)
    shoes = models.IntegerField(default=0)
    hat = models.IntegerField(default=0)
    gloves = models.IntegerField(default=0)
    scarf = models.IntegerField(default=0)
    jacket = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    class Meta:
        app_label = 'main'

    def __str__(self):
        return self.name
        
class submission(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=10, default='')
    market_id = models.CharField(max_length=10, default='')
    def __str__(self):
        return str(self.id)

class myEvent(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=10, default='')
    market_id = models.CharField(max_length=10, default='')
    def __str__(self):
        return str(self.id)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)