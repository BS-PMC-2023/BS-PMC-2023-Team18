from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import os
from django.contrib.auth.models import Group
from registry.models import UserProfileInfo
import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import market
# Create your views here.

def getUserProfileInfo(usr):
        upi = UserProfileInfo.objects.get(user=usr)
        return upi

def home(response):
    markets = market.objects.all()
    # return render(response, "main/home.html", {'markets': markets, 'search': markets})
    return render(response, "main/home.html", {})

def search_page(response):
    markets = market.objects.all()
    return render(response, "main/search.html", {'markets': markets, 'search': markets})

def myprofile(response):
    profileinfo = UserProfileInfo.objects.get(user=response.user)
    picture = UserProfileInfo.objects.get(user=response.user).picture
    group = response.user.groups.get(user=response.user)
    if group.name == 'buyer':
        pass

    if group.name == 'eventManager':
        pass

    return render(response, "main/myprofile.html", {
        'profileinfo': profileinfo,
        'profile_pic': picture,
        })

def editabout(response):
    profileinfo = UserProfileInfo.objects.get(user=response.user)
    about = profileinfo.about
    return render(response, "main/editabout.html", {'about': about})

def saveabout(response):
    if response.method == 'POST':
        message = response.POST['message']
        profileinfo = UserProfileInfo.objects.get(user=response.user)
        profileinfo.about = message[0:1000:]
        profileinfo.save()
    return myprofile(response)

def toggle_active(response):
    user = User.objects.get(pk=response.user.id)
    user.is_active = not user.is_active
    user.save()
    return home(response)

def sendmessage(response, username):
    if response.method == 'POST':
        message = response.POST['message']
        message = message + "\n\nMy email: " + User.objects.get(username=response.user.username).email
        send_mail('Rewear: A new message from '+str(response.user.username),
         message,
         settings.EMAIL_HOST_USER,
         [str(User.objects.get(username = username).email)],
         fail_silently=False)
    return render(response, 'main/thankyou2.html')

def messagetouser(response, username):
    return render(response, 'main/messagetouser.html', {'username': username})

def about(response):
    return render(response, "main/about.html", {})

def contact(response):
    return render(response, "main/contact.html", {})

def profile(response, username):
    user = User.objects.get(username = username)
    profileinfo = (UserProfileInfo.objects.filter(user = user))[0]
    picture = profileinfo.picture
    if picture: picture = picture.path

    return render(response, "main/profile.html", {
        'profileinfo': profileinfo,
        'user': user,
        'profile_pic': picture,
        })

def areyousure(response):
    return render(response, "main/areyousure.html", {})

def search(response):
    if response.method == 'POST':
        city = response.POST['city']
        address = response.POST['address']
        if address == "All" and city == "All":
            markets = market.objects.all()
        elif address == "All":
            markets = market.objects.filter(city=city)
        elif city == "All":
            markets = market.objects.filter(address=address)
        else:
            markets = market.objects.filter(city=city, address=address)
        return render(response, "main/search.html", {'markets': market.objects.all(), 'search': markets})
    else:
        return render(response, "main/search.html", {})

def insert_market(response):
    my_dict = {'inserted': False}
    if response.method == 'POST':
        name = response.POST['name']
        city = response.POST['city']
        address = response.POST['address']
        facebook = response.POST['facebook']
        description = response.POST['description']
        picture = response.POST['picture']
        market_manager = response.POST['market_manager']
        date = response.POST['date']
        capacity = response.POST['capacity']
        status = response.POST['status']
        rating = response.POST['rating']
        google_location = response.POST['google_location']

        market.objects.create(name=name, city=city, address=address, facebook=facebook, description=description, picture=picture, market_manager=market_manager, date=date, capacity=capacity, status=status, rating=rating, google_location=google_location)
        my_dict = {'inserted': True}
    return render(response, "main/insert_market.html", context=my_dict)

def market_page(response, id):
    cur_market = market.objects.get(id=id)
    return render(response, "main/market_page.html", {'market': cur_market})
def update_market(response, id):
    if response.method == 'POST':
        shirt = int(response.POST['shirt'])
        pants = int(response.POST['pants'])
        shoes = int(response.POST['shoes'])
        hat = int(response.POST['hat'])
        gloves = int(response.POST['gloves'])
        scarf = int(response.POST['scarf'])
        jacket = int(response.POST['jacket'])
        # add to the data base
        cur_market = market.objects.get(id=id)
        cur_market.shirt += shirt
        cur_market.pants += pants
        cur_market.shoes += shoes
        cur_market.hat += hat
        cur_market.gloves += gloves
        cur_market.scarf += scarf
        cur_market.jacket += jacket
        cur_market.save()
        return market_page(response, id)
    return render(response, "main/edit_market.html", {'market': cur_market})
