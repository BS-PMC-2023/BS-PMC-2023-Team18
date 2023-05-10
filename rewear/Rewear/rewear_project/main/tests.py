from django.test import TestCase, Client
# from django.urls import reverse
from django.contrib.auth.models import User, Group
from registry.models import UserProfileInfo
# from .models import market, submission
# from .views import *
from main import views

class Test(TestCase):

    # this one is okay
    def test_home(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)

    # this one is okay
    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    # this one is okay
    def test_search(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    # this one is  okay
    def test_search_page(self):
        response = self.client.get('/search_page/')
        self.assertEqual(response.status_code, 200)

    # this one is okay
    def test_submissions(self):
        response = self.client.get('/submissions/')
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        response = self.client.get('/send_message/')
        self.assertEqual(response.status_code, 302)

    def test_inbox(self):
        response = self.client.get('/inbox/')
        self.assertEqual(response.status_code, 302)

    def test_submit_request(self):
        response = self.client.get('/submit_request/2/2/')
        self.assertEqual(response.status_code, 200)

    def test_message_detail(self):
        response = self.client.get('/message_detail/0/')
        self.assertEqual(response.status_code, 404)

    def test_market_page(self):
        response = self.client.get('/market_page/')
        self.assertEqual(response.status_code, 404)

    def test_update_market(self):
        response = self.client.get('/update_market/')
        self.assertEqual(response.status_code, 404)

    def test_getUserProfileInfo(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        self.assertEqual(temp.user.username, users[0].username)

    def test_myprofile(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

        

