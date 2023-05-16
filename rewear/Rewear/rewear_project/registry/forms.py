from django.contrib.auth.models import User
from .models import UserProfileInfo
from django.db import models
from django import forms


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Making fields required:
        self.fields['email'].required = True

    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")

        return cleaned_data

    class Meta:
        model = User
        fields=('username', 'first_name', 'last_name', 'email', 'password', 'password_confirm')

class UserProfileInfoForm(forms.ModelForm):

    USER_TYPES = [('buyer', 'Buyer'),
    #('eventManager', 'Event Manager'),
                  ]
    userType = forms.CharField(label='User type', widget=forms.Select(choices=USER_TYPES))
    phone = models.CharField(max_length=10, default=None,)
    picture = models.ImageField(upload_to='picture', blank=True)


    class Meta:
        model = UserProfileInfo
        fields=('userType', 'phone', 'picture')