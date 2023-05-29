from django.test import TestCase, Client
from registry.models import UserProfileInfo
# Create your tests here.
from django.contrib.auth.models import User, Group
from registry import views

class Test(TestCase):

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 404)

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_signup_page(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        self.method = 'POST'
        self.POST = {'userType': 'buyer', 'phone': '050', 'username': 'testuser', 'email': 'testemail@gmail.com', 'password': 'testtest', 'password_confirm': 'testtest'}
        self.META = dict()
        self.FILES = dict()


        self.user = User.objects.create_user(username='admin', password='12345')
        login = self.client.login(username='admin', password='12345')
        users = User.objects.filter(username='admin')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='admin')
        groups = Group.objects.filter(name='admin')
        users[0].groups.add(groups[0])


        users = User.objects.filter(username='testuser')
        self.assertEqual(len(users), 0)
        response = views.signup(self)
        users = User.objects.filter(username='testuser')
        self.assertEqual(len(users), 1)