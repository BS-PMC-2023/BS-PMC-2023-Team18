from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

#  name , city , address , facebook , description , picture , market_manager , date , capacity , status , rating
class market(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, default='', blank=True)
    description = models.CharField(max_length=200, default='', blank=True)
    google_location = models.CharField(max_length=1000, default='', blank=True)
    market_manager = models.CharField(max_length=200, default='', blank=True)
    date = models.CharField(max_length=200, default='', blank=True)
    status = models.CharField(max_length=200, default='', blank=True)
    rating = models.CharField(max_length=200, default='', blank=True)
    # wear items
    shirt = models.IntegerField(default=0, blank=True)
    pants = models.IntegerField(default=0, blank=True)
    shoes = models.IntegerField(default=0, blank=True)
    hat = models.IntegerField(default=0, blank=True)
    gloves = models.IntegerField(default=0, blank=True)
    scarf = models.IntegerField(default=0, blank=True)
    jacket = models.IntegerField(default=0, blank=True)
    other = models.IntegerField(default=0, blank=True)
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
    #created_at = models.DateTimeField(auto_now_add=True)
    from django.utils import timezone
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)