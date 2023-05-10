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
from .models import market, submission, myEvent
from django import forms
from registry.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm


# Create your views here.

def getUserProfileInfo(usr):
    upi = UserProfileInfo.objects.get(user=usr)
    return upi


def home(response):
    subs = len(submission.objects.all())
    # return render(response, "main/home.html", {'markets': markets, 'search': markets})
    new_mail = new_messages(response.user.username)
    return render(response, "main/home.html", {'subs': subs, 'new_mail': new_mail})


def search_page(response):
    markets = market.objects.all()
    new_mail = new_messages(response.user.username)
    return render(response, "main/search.html", {'markets': markets, 'search': markets, 'new_mail': new_mail})


def myprofile(response):
    profileinfo = UserProfileInfo.objects.get(user=response.user)
    picture = UserProfileInfo.objects.get(user=response.user).picture
    group = response.user.groups.get(user=response.user)
    if group.name == 'buyer':
        pass

    if group.name == 'eventManager':
        pass

    new_mail = new_messages(response.user.username)
    return render(response, "main/myprofile.html", {
        'profileinfo': profileinfo,
        'profile_pic': picture,
        'new_mail': new_mail,
    })


def editabout(response):
    profileinfo = UserProfileInfo.objects.get(user=response.user)
    about = profileinfo.about
    new_mail = new_messages(response.user.username)
    return render(response, "main/editabout.html", {'about': about, 'new_mail': new_mail})


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
        send_mail('Rewear: A new message from ' + str(response.user.username),
                  message,
                  settings.EMAIL_HOST_USER,
                  [str(User.objects.get(username=username).email)],
                  fail_silently=False)
    new_mail = new_messages(response.user.username)
    return render(response, 'main/thankyou2.html', {'new_mail': new_mail})


def about(response):
    new_mail = new_messages(response.user.username)
    return render(response, "main/about.html", {'new_mail': new_mail})


# def contact(response):
#     new_mail = new_messages(response.user.username)
#     return render(response, "main/contact.html", {'new_mail': new_mail})


def profile(response, username):
    user = User.objects.get(username=username)
    try:
        profileinfo = (UserProfileInfo.objects.filter(user=user))[0]
        picture = profileinfo.picture
    except:
        profileinfo = None
        picture = None
    if picture: picture = picture.path

    new_mail = new_messages(response.user.username)
    return render(response, "main/profile.html", {
        'profileinfo': profileinfo,
        'cur_user': user,
        'profile_pic': picture,
        'new_mail': new_mail,
    })


def areyousure(response):
    new_mail = new_messages(response.user.username)
    return render(response, "main/areyousure.html", {'new_mail': new_mail})


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
        new_mail = new_messages(response.user.username)
        return render(response, "main/search.html",
                      {'markets': market.objects.all(), 'search': markets, 'new_mail': new_mail})
    else:
        new_mail = new_messages(response.user.username)
        return render(response, "main/search.html", {'new_mail': new_mail})


def insert_market(response):
    new_mail = new_messages(response.user.username)
    my_dict = {'inserted': False, 'new_mail': new_mail}
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

        market.objects.create(name=name, city=city, address=address, facebook=facebook, description=description,
                              picture=picture, market_manager=market_manager, date=date, capacity=capacity,
                              status=status, rating=rating, google_location=google_location)
        my_dict = {'inserted': True}
    return render(response, "main/insert_market.html", context=my_dict)


def market_page(response, id):
    cur_market = market.objects.get(id=id)
    # get all market with specific id
    myevents = myEvent.objects.filter(user_id=response.user.id, market_id=id)
    # serch in the database if the user is in the event
    new_mail = new_messages(response.user.username)
    if myevents:
        return render(response, "main/market_page.html",
                      {'market': cur_market, 'sign_event': True, 'new_mail': new_mail})
    else:
        return render(response, "main/market_page.html",
                      {'market': cur_market, 'sign_event': False, 'new_mail': new_mail})


def update_market(response, id):
    cur_market = market.objects.get(id=id)
    if response.method == 'POST':
        shirt = int(response.POST['shirt'])
        pants = int(response.POST['pants'])
        shoes = int(response.POST['shoes'])
        hat = int(response.POST['hat'])
        gloves = int(response.POST['gloves'])
        scarf = int(response.POST['scarf'])
        jacket = int(response.POST['jacket'])
        # add to the database
        cur_market.shirt += shirt
        cur_market.pants += pants
        cur_market.shoes += shoes
        cur_market.hat += hat
        cur_market.gloves += gloves
        cur_market.scarf += scarf
        cur_market.jacket += jacket
        cur_market.save()
        return market_page(response, id)
    return render(response, "main/market_page.html",
                  {'market': cur_market, 'new_mail': new_messages(response.user.username)})


def set_market_value(response, id):
    cur_market = market.objects.get(id=id)
    if response.method == 'POST':
        shirt = int(response.POST['shirt'])
        pants = int(response.POST['pants'])
        shoes = int(response.POST['shoes'])
        hat = int(response.POST['hat'])
        gloves = int(response.POST['gloves'])
        scarf = int(response.POST['scarf'])
        jacket = int(response.POST['jacket'])
        # add to the database
        cur_market.shirt = shirt
        cur_market.pants = pants
        cur_market.shoes = shoes
        cur_market.hat = hat
        cur_market.gloves = gloves
        cur_market.scarf = scarf
        cur_market.jacket = jacket
        cur_market.save()
        return market_page(response, id)
    return render(response, "main/market_page.html",
                  {'market': cur_market, 'new_mail': new_messages(response.user.username)})


def assign_manager(response, mid, username):
    cur_market = market.objects.get(id=mid)
    print(cur_market.market_manager)
    cur_market.market_manager = username
    print(cur_market.market_manager)
    market.save(cur_market)
    return delete_sub(response, mid, username)


def delete_sub(response, mid, username):
    cur_user = User.objects.get(username=username)
    cur_sub = submission.objects.get(user_id=cur_user.id, market_id=mid)
    cur_sub.delete()
    return submissions(response)


def submissions(response):
    submissions = submission.objects.all()
    users = User.objects.all()
    res = []
    for sub in submissions:
        flag = 0
        cur = []
        cur.append(sub.market_id)
        try:
            cur.append(users.get(id=sub.user_id))
            flag = 1
        except:
            pass
        if flag: res.append(cur)
    new_mail = new_messages(response.user.username)
    return render(response, "main/submissions.html", {'subs': res, 'new_mail': new_mail})


def submit_request(response, uid, mid):
    subs = submission.objects.all()
    if not subs.filter(user_id=uid, market_id=mid).exists():
        submission.objects.create(user_id=uid, market_id=mid)
        print("Created submission with uid: " + str(uid) + ", mid: " + str(mid))  # create submission
    else:
        print("Submission already exists with uid: " + str(uid) + ", mid: " + str(mid))
    new_mail = new_messages(response.user.username)
    return render(response, "main/submissions.html", {'submissions': submissions, 'new_mail': new_mail})


# user story 14 - Market FeedBack
def feedback(response, id):
    if response.method == 'POST':
        message = response.POST['message']
        send_mail('Contact Form',
                  message,
                  settings.EMAIL_HOST_USER,
                  ['Rewear100@gmail.com'],
                  fail_silently=True)
    cur_market = market.objects.get(id=id)
    new_mail = new_messages(response.user.username)
    return render(response, "main/market_page.html", {'market': cur_market, 'feedback': True, 'new_mail': new_mail})


def update_profilepic(response):
    if response.method == 'POST':
        form = UserProfileInfo(response.POST, response.FILES)
        if form.is_valid():
            form.save()
            return render(response, 'main/profile.html', {})
    else:
        form = UserProfileInfoForm()
    new_mail = new_messages(response.user.username)
    return render(response, 'main/update_profilepic.html', {'form': form, 'new_mail': new_mail})


def update_profilepic(response):
    new_mail = new_messages(response.user.username)
    if response.method == 'POST':
        picture = response.FILES['picture']
        user = User.objects.get(username=response.user.username)
        profileinfo = UserProfileInfo.objects.get(user=user)
        profileinfo.picture = picture
        profileinfo.save()
        return render(response, "main/myprofile.html", {'profile_pic': picture, 'new_mail': new_mail})
    else:
        return render(response, 'main/myprofile.html', {'new_mail': new_mail})


def sign_event(response, uid, mid):
    cur_market = market.objects.get(id=mid)
    if response.method == 'POST':
        print("Signing up for event with uid: " + str(uid) + ", mid: " + str(mid))
        currevent = myEvent.objects.create(user_id=uid, market_id=mid)
        currevent.save()
    new_mail = new_messages(response.user.username)
    return render(response, "main/market_page.html", {'market': cur_market, 'sign_event': True, 'new_mail': new_mail})


def my_events(response, uid):
    myevents = myEvent.objects.filter(user_id=uid)
    markets = []
    for event in myevents:
        markets.append(market.objects.get(id=event.market_id))
    new_mail = new_messages(response.user.username)
    return render(response, "main/my_events.html", {'markets': markets, 'new_mail': new_mail})


@login_required
def send_message(request, username=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            message = Message.objects.create(sender=request.user, recipient=recipient, subject=subject, body=body)
            return inbox(request)
    else:
        form = MessageForm()
        if username:
            user = User.objects.filter(username=username)[0]
            form.fields['recipient'] = forms.ModelChoiceField(queryset=User.objects.all(), initial=user)
    new_mail = new_messages(request.user.username)
    return render(request, 'main/send_message.html', {'form': form, 'new_mail': new_mail})


@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user)
    new_mail = new_messages(request.user.username)
    return render(request, 'main/inbox.html', {'messages': messages, 'new_mail': new_mail})


@login_required
def message_detail(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.user == message.recipient:
        message.is_read = True
        message.save()
    new_mail = new_messages(request.user.username)
    return render(request, 'main/message_detail.html', {'message': message, 'new_mail': new_mail})


def new_messages(username):
    try:
        messages = Message.objects.filter(recipient=User.objects.filter(username=username)[0])
        for m in messages:
            if not m.is_read:
                return True
        return False
    except:
        return False


# NEW MESSAGES:
# Add the following to every render request:
# 'new_mail': new_messages(response.user.username)
# so that "base.html" will be able to get whether user has new mail

def delete_market(response, id):

    if response.method == 'POST':
        if response.user.username == market.objects.get(id=id).market_manager:

            cur_market = market.objects.get(id=id)
            cur_market.delete()
            for sub in submission.objects.filter(market_id=id):
                sub.delete()

            for event in myEvent.objects.filter(market_id=id):
                event.delete()
    return search_page(response)