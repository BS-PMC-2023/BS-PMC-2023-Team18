from django.contrib.auth.models import User
from django.db import models
from django import forms
from registry.models import UserProfileInfo

class MessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)
