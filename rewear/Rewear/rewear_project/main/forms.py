from django.contrib.auth.models import User
from django.db import models
from django import forms
from registry.models import UserProfileInfo

class MessageForm(forms.Form):
    # recipient = forms.ModelChoiceField(queryset=User.objects.all(), initial="admin")
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)

    def __init__(self, username=None):
        super().__init__()
        if username:
            user = User.objects.filter(username=username)[0]
            self.fields['recipient'] = forms.ModelChoiceField(queryset=User.objects.all(), initial=user)