from django.shortcuts import render, redirect
from .forms import UserProfileInfoForm, UserForm
from django.contrib.auth.models import Group
from main.models import Message
from django.contrib.auth.models import User

# Create your views here.

def signup(response):
    registered = False

    if response.method == "POST":
        user_form = UserForm(data=response.POST)
        profile_form = UserProfileInfoForm(data=response.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            Group.objects.get_or_create(name=profile_form.cleaned_data['userType'])
            cur_group = Group.objects.get(name=profile_form.cleaned_data['userType'])
            cur_group.user_set.add(user)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.phone = profile_form.cleaned_data['phone']
            profile.save()
        
            if 'picture' in response.FILES:
                profile.picture = response.FILES['picture']

            profile.save()

            admin = User.objects.get(username="admin")
            recipient = User.objects.get(username=user.username)

            welcome_msg = "Welcome to Rewear! We’re thrilled to have you here. Our mission is to make sustainable fashion accessible to everyone.\n"  \
            +"We believe that every small step counts and we’re excited that you’re taking one with us. We hope you enjoy our platform and find everything you’re looking for. If you have any questions or feedback, please don’t hesitate to reach out to us.\n"

            try:
                message = Message.objects.create(sender=admin, recipient=user, subject="Welcome to Rewear!", body=welcome_msg)
            except:
                pass

            registered = True
            return redirect("/login/")

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(response, "registry/signup.html",
        {'user_form':user_form,
        'profile_form':profile_form, 'registered':registered})