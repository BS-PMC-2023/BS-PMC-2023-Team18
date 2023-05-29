from django.test import TestCase, Client
# from django.urls import reverse
from django.contrib.auth.models import User, Group
from registry.models import UserProfileInfo
# from .models import market, submission
# from .views import *
from main import views
from main import models
from django.db import models as djmodels

class Test(TestCase):

    def test_home(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        response = self.client.get('/search_page/')
        self.assertEqual(response.status_code, 200)

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
        self.assertEqual(response.status_code, 302)

    def test_market_page(self):
        models.market.objects.create(id=1)
        response = self.client.get('/market_page/1')
        self.assertEqual(response.status_code, 301)

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

    def test_profile(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
        response = self.client.get('/profile/'+str(users[0].username))
        self.assertEqual(response.status_code, 301)

    def test_editabout(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
        response = self.client.get('/editabout/')
        self.assertEqual(response.status_code, 200)

    def test_saveabout(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
        response = self.client.get('/saveabout/')
        self.assertEqual(response.status_code, 200)

    # def test_toggle_active(self):
    #     self.user = User.objects.create_user(username='testuser', password='12345')
    #     login = self.client.login(username='testuser', password='12345')
    #     users = User.objects.filter(username='testuser')
    #     temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
    #     Group.objects.create(name='testgroup')
    #     groups = Group.objects.filter(name='testgroup')
    #     users[0].groups.add(groups[0])
    #     self.assertEqual(users[0].is_active, True)
    #     # views.toggle_active(self)
    #     # self.assertEqual(users[0].is_active, False)

    def test_areyousure(self):
        response = self.client.get('/areyousure/')
        self.assertEqual(response.status_code, 200)

    def test_assign_manager(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
    
        m = models.market.objects.create(id=1)
        self.client.get('/submit_request/' + str(users[0].id) + '/1/')
    
        self.assertEqual(m.market_manager, '')
        response = views.assign_manager(self, m.id, users[0].username)
        self.assertEqual(response.status_code, 200)

    def test_delete_sub(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])

        m = models.market.objects.create(id=1)
        self.client.get('/submit_request/' + str(users[0].id) + '/1/')

        response = views.delete_sub(self, m.id, users[0].username)
        self.assertEqual(response.status_code, 200)

    def test_sign_event(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])

        m = models.market.objects.create(id=1)

        self.assertEqual(len(models.myEvent.objects.filter(user_id=users[0].id, market_id=m.id)), 0)
        e = models.myEvent.objects.create(user_id=users[0].id, market_id=m.id)
        self.assertEqual(len(models.myEvent.objects.filter(user_id=users[0].id, market_id=m.id)), 1)

    def test_my_events(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])

        response = self.client.get('/my_events/' + str(users[0].id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_message_detail(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
    
        m = models.Message.objects.create(
            sender=self.user,
            recipient=self.user,
            subject='test subject',
            body='this is a test',
            is_read=False,
        )
    
        self.assertEqual(m.is_read, False)
        response = views.message_detail(self, m.id)
        # self.assertEqual(m.is_read, True)

    def test_new_messages(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
    
        self.assertEqual(views.new_messages(self.user.username), False)
    
        m = models.Message.objects.create(
            sender=self.user,
            recipient=self.user,
            subject='test subject',
            body='this is a test',
            is_read=False
        )
    
        self.assertEqual(views.new_messages(self.user.username), True)
