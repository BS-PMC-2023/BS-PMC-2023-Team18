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
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
# facebook meta graph api import 
import facebook

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
    try:
        picture = UserProfileInfo.objects.get(user=response.user).picture
    except:
        picture = None
    try:
        pic_path = picture.path.split("static")[-1]
    except:
        pic_path = None
    new_mail = new_messages(response.user.username)
    return render(response, "main/myprofile.html", {
        'profileinfo': profileinfo,
        'profile_pic': picture,
        'pic_path': pic_path,
        'cur_user': response.user,
        'new_mail': new_mail,
    })

# Here we edit the profile of the user and update the about him.
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


# def sendmessage(response, username):
#     if response.method == 'POST':
#         message = response.POST['message']
#         message = message + "\n\nMy email: " + User.objects.get(username=response.user.username).email
#         send_mail('Rewear: A new message from ' + str(response.user.username),
#                   message,
#                   settings.EMAIL_HOST_USER,
#                   [str(User.objects.get(username=username).email)],
#                   fail_silently=False)
#     new_mail = new_messages(response.user.username)
#     return render(response, 'main/thankyou2.html', {'new_mail': new_mail})


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

    pic_path = None
    try:
        pic_path = picture.split("static")[-1]
    except:
        pic_path = None
    new_mail = new_messages(response.user.username)
    return render(response, "main/profile.html", {
        'profileinfo': profileinfo,
        'cur_user': user,
        'profile_pic': picture,
        'pic_path': pic_path,
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

def market_page(response, id):
    cur_market = market.objects.get(id=id)
    new_mail = new_messages(response.user.username)

    try:
        my_event = myEvent.objects.get(user_id=response.user.id, market_id=id)

        if my_event:
            return render(response, "main/market_page.html",
                          {'market': cur_market, 'sign_event': True, 'new_mail': new_mail, 'my_event': my_event})
        else:
            return render(response, "main/market_page.html",
                          {'market': cur_market, 'sign_event': False, 'new_mail': new_mail, 'my_event': my_event})
    except ObjectDoesNotExist:
        # Handle the case when the myEvent object does not exist
        return render(response, "main/market_page.html",
                      {'market': cur_market, 'sign_event': False, 'new_mail': new_mail})


def update_market(response, id):
    new_mail = new_messages(response.user.username)
    cur_market = market.objects.get(id=id)
    if response.method == 'POST':
        shirt = int(response.POST.get('shirt', 0))  # Default value of 0 if empty
        pants = int(response.POST.get('pants', 0))  # Default value of 0 if empty
        shoes = int(response.POST.get('shoes', 0))  # Default value of 0 if empty
        hat = int(response.POST.get('hat', 0))  # Default value of 0 if empty
        gloves = int(response.POST.get('gloves', 0))  # Default value of 0 if empty
        scarf = int(response.POST.get('scarf', 0))  # Default value of 0 if empty
        jacket = int(response.POST.get('jacket', 0))  # Default value of 0 if empty
        # add to the database
        cur_market.shirt += shirt
        cur_market.pants += pants
        cur_market.shoes += shoes
        cur_market.hat += hat
        cur_market.gloves += gloves
        cur_market.scarf += scarf
        cur_market.jacket += jacket
        cur_market.save()
        my_event = myEvent.objects.get(user_id=response.user.id, market_id=id)
        if my_event:
            my_event.shirt += shirt
            my_event.pants += pants
            my_event.shoes += shoes
            my_event.hat += hat
            my_event.gloves += gloves
            my_event.scarf += scarf
            my_event.jacket += jacket
            my_event.save()

        return market_page(response, id)
    return render(response, "main/market_page.html",
                  {'market': cur_market, 'new_mail': new_messages(response.user.username)})

# user story 33 key BSPMC2318-33 edit items in market
def edit_items_market(response, id):
    new_mail = new_messages(response.user.username)
    cur_market = market.objects.get(id=id)
    my_event = myEvent.objects.get(user_id=response.user.id, market_id=id)
    if response.method == 'POST':
        shirt = response.POST.get('shirt')
        pants = response.POST.get('pants')
        shoes = response.POST.get('shoes')
        hat = response.POST.get('hat')
        gloves = response.POST.get('gloves')
        scarf = response.POST.get('scarf')
        jacket = response.POST.get('jacket')

        # Convert empty strings to 0
        shirt = int(shirt) if shirt else 0
        pants = int(pants) if pants else 0
        shoes = int(shoes) if shoes else 0
        hat = int(hat) if hat else 0
        gloves = int(gloves) if gloves else 0
        scarf = int(scarf) if scarf else 0
        jacket = int(jacket) if jacket else 0
        # add to the database
        cur_market.shirt += shirt - my_event.shirt
        cur_market.pants += pants - my_event.pants
        cur_market.shoes += shoes - my_event.shoes
        cur_market.hat += hat - my_event.hat
        cur_market.gloves += gloves - my_event.gloves
        cur_market.scarf += scarf - my_event.scarf
        cur_market.jacket += jacket - my_event.jacket
        cur_market.save()
        if my_event:
            my_event.shirt += shirt - my_event.shirt
            my_event.pants += pants - my_event.pants
            my_event.shoes += shoes - my_event.shoes
            my_event.hat += hat - my_event.hat
            my_event.gloves += gloves - my_event.gloves
            my_event.scarf += scarf - my_event.scarf
            my_event.jacket += jacket - my_event.jacket
            my_event.save()

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
    user = User.objects.get(username=username)
    Group.objects.get_or_create(name="eventManager")
    managerGroup = Group.objects.get(name="eventManager")
    user.groups.add(managerGroup)
    user.save()
    cur_market = market.objects.get(id=mid)
    cur_market.market_manager = username
    market.save(cur_market)

    current_market = market.objects.get(id=mid)
    sign_user = User.objects.get(username=username)
    try:
        message_body = 'Your submission for "' + current_market.name + '" has been accepted by the admin you can now manage your market.'
        Message.objects.create(sender=response.user, recipient=sign_user, subject='Submission Accepted',
                               body=message_body)
    except:
        pass

    return delete_sub(response, mid, username, False)

def delete_sub(response, mid, username, msg=True):
    current_market = market.objects.get(id=mid)
    sign_user = User.objects.get(username=username)
    if msg:
        try:
            message_body = 'Your submission for ' + current_market.name + ' has been declined by the Admin.'
            Message.objects.create(sender=response.user, recipient=sign_user, subject='Submission Declined',
                                   body=message_body)
        except:
            pass
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

# User story 19,20 - market feedback and general feedback
def feedback(response, market_name):
    cur_market = None
    if response.method == 'POST':
        form = MessageForm(response.POST)
        body = response.POST['message']
        if market_name != '"':
            cur_market = market.objects.get(name=market_name)
            recipient = User.objects.get(username=cur_market.market_manager)
            subject = "Market {0} Feedback".format(market_name)
            new_message = Message.objects.create(sender=response.user, recipient=recipient, subject=subject, body=body)
            new_mail = new_messages(response.user.username)
            return render(response, "main/market_page.html",
                          {'market': cur_market, 'feedback': True, 'new_mail': new_mail})
        else:
            subject = "Feedback from {0}".format(response.user.username)
            for user in User.objects.all():
                if user.is_superuser:
                    recipient = User.objects.get(username=user.username)
                    new_message = Message.objects.create(sender=response.user, recipient=recipient, subject=subject, body=body)
        # new_message = Message.objects.create(sender=response.user, recipient=recipient, subject=subject, body=body)
    return home(response)

    # new_mail = new_messages(response.user.username)
    # return render(response, "main/market_page.html", {'market': cur_market, 'feedback': True, 'new_mail': new_mail})

def submit_request(response, uid, mid):
    new_mail = new_messages(response.user.username)
    subs = submission.objects.all()
    if not subs.filter(user_id=uid, market_id=mid).exists():
        submission.objects.create(user_id=uid, market_id=mid)
    #     print("\nCreated submission with uid: " + str(uid) + ", mid: " + str(mid) + "\n")  # create submission
    # else:
    #     print("\nSubmission already exists with uid: " + str(uid) + ", mid: " + str(mid) + "\n")
    return render(response, "main/submissions.html", {'submissions': submissions, 'new_mail': new_mail})

# def update_profilepic(response):
#     new_mail = new_messages(response.user.username)
#     if response.method == 'POST':
#         form = UserProfileInfo(response.POST, response.FILES)
#         if form.is_valid():
#             form.save()
#             # return myprofile(response)
#             return render(response, "main/home.html", {'new_mail': new_mail})
#     else:
#         form = UserProfileInfoForm()
#     # return render(response, 'main/update_profilepic.html', {'form': form, 'new_mail': new_mail})
#     return render(response, "main/home.html", {'new_mail': new_mail})

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
        # print("\nSigning up for event with uid: " + str(uid) + ", mid: " + str(mid) + "\n")
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

def managed_events(response, uid):
    curUser = User.objects.get(id=uid)
    markets = market.objects.filter(market_manager=curUser.username)
    new_mail = new_messages(response.user.username)
    return render(response, "main/managed_events.html", {'markets': markets, 'new_mail': new_mail})

# User story 27 - send message to user
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


# User story 27 - send message to user
@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user)
    new_mail = new_messages(request.user.username)
    return render(request, 'main/inbox.html', {'messages': messages, 'new_mail': new_mail})


# User story 27 - send message to user
@login_required
def message_detail(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.user == message.recipient:
        message.is_read = True
        message.save()
    new_mail = new_messages(request.user.username)
    return render(request, 'main/message_detail.html', {'message': message, 'new_mail': new_mail})


# User story 27 - send message to user
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
    user_events = myEvent.objects.filter(market_id=id)
    current_market = market.objects.get(id=id)
    try:
        for event in user_events:
            sign_user = User.objects.get(id=event.user_id)
            message_body = 'The market ' + current_market.name + ' which located in '+ current_market.city + ' you signed up for has been cancelled.'
            Message.objects.create(sender=response.user, recipient=sign_user, subject='Market Canceled', body=message_body)
    except:
        pass

    if response.method == 'POST':
        if response.user.username == market.objects.get(id=id).market_manager:

            cur_market = market.objects.get(id=id)
            cur_market.delete()
            for sub in submission.objects.filter(market_id=id):
                sub.delete()

            for event in myEvent.objects.filter(market_id=id):
                event.delete()
    return search_page(response)


def facebook_page(response, market_id):
    new_mail = new_messages(response.user.username)
    current_market = market.objects.get(id=market_id)
    success_message = None
    return render(response, "main/facebook_page.html", {'new_mail': new_mail, 'current_market': current_market,'success_message': success_message})


def post_to_facebook(request):
    if request.method == 'POST':
        message = request.POST.get('message')  # Get the message from the form

        # Create a Facebook Graph API instance
        # graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
        access_token = 'EAAb6g8eihJsBAFMZAjXwFy7EEdVqrpEdlGXZAmGZALazYe1hIDlY46tMgwcwUY77OZAZBIKfKDaANl6wWyQZCsOHwGHoiSLLMkEThB4BNKYrXjMqZBYOzbT9ZAbr3UDjHJLDneziYPJOdNn1oaDSQ2FXSnVfStLZAhcevV5zQ6QqQZBrkwmT1eTV9001GHq7CCWp051MPUMZBoHO6VOHZAjiZBr2LMxVnuvOhhO0ZD'
        graph = facebook.GraphAPI(access_token=access_token)

        # try:
        # Make the API call to post on Facebook
        graph.put_object(parent_object='me', connection_name='feed', message='Hello, world')
        # graph.put_wall_post(message=message)
        success_message = "Post successfully posted on Facebook."
        print(success_message)
        # except facebook.GraphAPIError as e:
        #     print("not success")
        #     error_message = f"Failed to post on Facebook: {str(e)}"

    return home(request)

def edit_profile(response):
    new_mail = new_messages(response.user.username)
    profileinfo = UserProfileInfo.objects.get(user=response.user)
    try:
        picture = UserProfileInfo.objects.get(user=response.user).picture
    except:
        picture = None
    try:
        pic_path = picture.path.split("static")[-1]
    except:
        pic_path = None

    return render(response, "main/edit_profile.html", {
        'profileinfo': profileinfo,
        'profile_pic': picture,
        'pic_path': pic_path,
        'cur_user': response.user,
        'new_mail': new_mail,
    })

# User story 23 - edit profile key BSPMC2318-23
def update_profile_info(request):
    if request.method == 'POST':
        profileinfo = UserProfileInfo.objects.get(user=request.user)

        profileinfo.user.email = request.POST.get('email')
        profileinfo.user.first_name = request.POST.get('first_name')
        profileinfo.user.last_name = request.POST.get('last_name')
        profileinfo.phone = request.POST.get('phone')

        profileinfo.user.save()
        profileinfo.save()
        return home(request)
    else:
        return myprofile(request)

def remove_manager(response, market_id):
    if response.method == 'POST' and response.user.is_superuser:
        cur_market = market.objects.get(id=market_id)
        temp_manager = cur_market.market_manager
        cur_market.market_manager = ''
        cur_market.save()

        cnt = 0
        for m in market.objects.all():
            if m.market_manager == temp_manager:
                cnt += 1
                break
        if cnt == 0:
            user = UserProfileInfo.objects.get(user = User.objects.get(username = temp_manager))
            managerGroup = Group.objects.get(name="eventManager")
            User.objects.get(username = temp_manager).groups.remove(managerGroup)

    return market_page(response, market_id)


def attending_users(response, market_id):
    cur_market = market.objects.get(id=market_id)

    events = myEvent.objects.filter(market_id = market_id)
    attending_users = []
    for event in events:
        try:
            attending_users.append(User.objects.get(id = event.user_id))
        except:
            continue

    new_mail = new_messages(response.user.username)
    return render(response, 'main/attending_users.html', {'new_mail': new_mail, 'market': cur_market, 'attending_users': attending_users})


def report_user(response, username):
    user = User.objects.get(username=username)

    new_mail = new_messages(response.user.username)
    return render(response, 'main/report_user.html', {'new_mail': new_mail, 'user': user})


def send_report(response, username):
    if response.method == 'POST':
        form = MessageForm(response.POST)
        body = response.POST['message']

        start_body = "This is a report on: " + str(username) + ", from an event manager: " + str(response.user.username) + ".\n\n"

        subject = "Reporting on {0}".format(username)
        for user in User.objects.all():
            if user.is_superuser:
                recipient = User.objects.get(username=user.username)
                new_message = Message.objects.create(sender=response.user, recipient=recipient, subject=subject, body=start_body+body)
    # return home(response)

    new_mail = new_messages(response.user.username)
    return render(response, 'main/thankyou2.html', {'new_mail': new_mail})



