from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rewear_app.models import UserProfileInfo
from rewear_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
def HomePage(request):
    attributes = {'key': 'value'}
    return render(request, 'rewear_app/base.html', context=attributes)

def header(request):
    attributes = {}
    return render(request, 'rewear_app/index.html', context=attributes)
def index(request):
    attributes = {}
    return render(request, 'rewear_app/index.html', context=attributes)
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    attributes = {}
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        try:
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile.save()

                registered = True
            else:
                print(user_form.errors, profile_form.errors)
                catch = user_form.errors
                expctaion = profile_form.errors
        except:
            print("error")
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'rewear_app/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    attributes = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'rewear_app/login.html', {})