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

    def getUser(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        users = User.objects.filter(username='testuser')
        temp = UserProfileInfo.objects.create(user=users[0], phone='050', about='')
        Group.objects.create(name='testgroup')
        groups = Group.objects.filter(name='testgroup')
        users[0].groups.add(groups[0])
        return users[0]

    def test_home(self):
        self.user = self.getUser()
        response = views.home(self)
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        self.user = self.getUser()
        self.META = {}
        response = views.about(self)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        self.user = self.getUser()
        self.META = {}
        response = views.about(self)
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        self.user = self.getUser()
        self.META = {}
        response = views.search_page(self)
        self.assertEqual(response.status_code, 200)

    def test_submissions(self):
        self.user = self.getUser()
        response = views.submissions(self)
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {}
        response = views.send_message(self)
        self.assertEqual(response.status_code, 200)

    def test_inbox(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {}
        response = views.inbox(self)
        self.assertEqual(response.status_code, 200)

    def test_submit_request(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {}

        m = models.market.objects.create(id=1)

        response = views.submit_request(self, self.user.id, m.id)
        self.assertEqual(response.status_code, 200)

    def test_market_page(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {}

        m = models.market.objects.create(id=1)
        
        response = views.market_page(self, m.id)
        self.assertEqual(response.status_code, 200)

    def test_update_market(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {'shirt': 0, 'pants': 1, 'shoes': 0, 'hat': 0, 'gloves': 0, 'scarf': 0, 'jacket': 0}

        models.market.objects.create(id=1)
        m = models.market.objects.filter(id=1)[0]
        e = models.myEvent.objects.create(user_id=self.user.id, market_id=m.id)
        self.assertEqual(m.pants, 0)

        response = views.update_market(self, m.id)
        m = models.market.objects.filter(id=1)[0]
        self.assertEqual(m.pants, 1)


    def test_getUserProfileInfo(self):
        self.user = self.getUser()
        profile = views.getUserProfileInfo(self.user)
        self.assertEqual(profile.user, self.user)

    def test_myprofile(self):
        self.user = self.getUser()
        self.META = {}
        response = views.myprofile(self)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        self.user = self.getUser()
        self.META = {}
        response = views.profile(self, self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_editabout(self):
        self.user = self.getUser()
        self.META = {}
        response = views.editabout(self)
        self.assertEqual(response.status_code, 200)

    def test_saveabout(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {'message': 'test'}
        response = views.saveabout(self)
        self.assertEqual(response.status_code, 200)

    def test_toggle_active(self):
        self.user = self.getUser()
        user = User.objects.filter(username=self.user.username)[0]
        self.assertEqual(user.is_active, True)
        views.toggle_active(self)
        user = User.objects.filter(username=self.user.username)[0]
        self.assertEqual(user.is_active, False)

    def test_areyousure(self):
        self.user = self.getUser()
        self.META = {}
        response = views.areyousure(self)
        self.assertEqual(response.status_code, 200)

    def test_assign_manager(self):
        self.user = self.getUser()

        m = models.market.objects.create(id=1)
        self.client.get('/submit_request/' + str(self.user.id) + '/1/')

        self.assertEqual(m.market_manager, '')
        response = views.assign_manager(self, m.id, self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_delete_sub(self):
        self.user = self.getUser()

        m = models.market.objects.create(id=1)
        self.client.get('/submit_request/' + str(self.user.id) + '/1/')

        response = views.delete_sub(self, m.id, self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_sign_event(self):
        self.user = self.getUser()

        m = models.market.objects.create(id=1)
        self.method = 'POST'
        self.META = {}
        self.POST = {}

        self.assertEqual(len(models.myEvent.objects.filter(user_id=self.user.id, market_id=m.id)), 0)
        response = views.sign_event(self, self.user.id, m.id)
        self.assertEqual(len(models.myEvent.objects.filter(user_id=self.user.id, market_id=m.id)), 1)

    def test_my_events(self):
        self.user = self.getUser()
        self.META = {}
        response = views.my_events(self, self.user.id)
        self.assertEqual(response.status_code, 200)

    def test_message_detail(self):
        self.user = self.getUser()

        m = models.Message.objects.create(
            sender=self.user,
            recipient=self.user,
            subject='test subject',
            body='this is a test',
            is_read=False,
        )

        m = models.Message.objects.get(id=m.id)
        self.assertEqual(m.is_read, False)
        response = views.message_detail(self, m.id)
        m = models.Message.objects.get(id=m.id)
        self.assertEqual(m.is_read, True)

    def test_new_messages(self):
        self.user = self.getUser()

        self.assertEqual(views.new_messages(self.user.username), False)

        m = models.Message.objects.create(
            sender=self.user,
            recipient=self.user,
            subject='test subject',
            body='this is a test',
            is_read=False
        )

        self.assertEqual(views.new_messages(self.user.username), True)

    def test_send_message(self):
        self.user = self.getUser()

        self.method = 'POST'
        self.POST = {'recipient': self.user, 'subject': 'test subject', 'body': 'this is a test'}
        self.META = dict()

        self.assertEqual(len(models.Message.objects.filter(sender=self.user)), 0)
        views.send_message(self)
        self.assertEqual(len(models.Message.objects.filter(sender=self.user)), 1)

    def test_edit_items_market(self):
        self.user = self.getUser()

        market = models.market.objects.create(id=1, name='test market', city='test city', address='test address')
        event = models.myEvent.objects.create(user_id=self.user.id, market_id=market.id)

        self.method = 'POST'
        self.POST = {'shirt': 0, 'pants': 1, 'shoes': 0, 'hat': 0, 'gloves': 0, 'scarf': 0, 'jacket': 0}
        self.META = {}

        self.assertEqual(market.pants, 0)
        views.edit_items_market(self, market.id)
        market = models.market.objects.get(id=1)
        self.assertEqual(market.pants, 1)

    def test_set_market_value(self):
        self.user = self.getUser()

        market = models.market.objects.create(id=1, name='test market', city='test city', address='test address')
        event = models.myEvent.objects.create(user_id=self.user.id, market_id=market.id)

        self.method = 'POST'
        self.POST = {'shirt': 0, 'pants': 1, 'shoes': 0, 'hat': 0, 'gloves': 0, 'scarf': 0, 'jacket': 0}
        self.META = {}

        self.assertEqual(market.pants, 0)
        views.set_market_value(self, market.id)
        market = models.market.objects.get(id=1)
        self.assertEqual(market.pants, 1)

    def test_feedback(self):
        self.user = self.getUser()

        admin_password = '123'
        my_admin = User.objects.create_superuser('adminuser', 'myemail@test.com', admin_password)

        self.method = 'POST'
        self.POST = {'message': 'test message'}
        
        admin = User.objects.filter(username=my_admin.username)[0]

        self.assertEqual(len(models.Message.objects.filter(recipient = admin)), 0)
        views.feedback(self, '"')
        self.assertEqual(len(models.Message.objects.filter(recipient = admin)), 1)

    def test_update_profilepic(self):
        self.user = self.getUser()
        
        profile = UserProfileInfo.objects.filter(user=self.user)[0]

        import tempfile
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        self.assertEqual(profile.picture, "")

        self.method = 'POST'
        self.POST = {}
        self.FILES = {'picture': image}
        self.META = {}

        views.update_profilepic(self)
        profile = UserProfileInfo.objects.filter(user=self.user)[0]
        self.assertEqual(profile.picture, image)

    def test_managed_events(self):
        self.user = self.getUser()
        self.META = {}
        response = views.managed_events(self, self.user.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_market(self):
        self.user = self.getUser()

        market = models.market.objects.create(id=1, name='test market', city='test city', address='test address', market_manager=self.user.username)

        self.method = 'POST'
        self.POST = {}
        self.META = {}
        
        m = models.market.objects.filter(id=1)
        self.assertEqual(len(m), 1)
        views.delete_market(self, market.id)
        m = models.market.objects.filter(id=1)
        self.assertEqual(len(m), 0)

    def test_edit_profile(self):
        self.user = self.getUser()
        self.META = {}
        response = views.edit_profile(self)
        self.assertEqual(response.status_code, 200)

    def test_update_profile_info(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        old_phone = self.user.userprofileinfo.phone
        new_phone = '123'
        self.POST = {'first_name': 'test', 'last_name': 'test', 'email': 'test@mytest.com', 'phone': new_phone}

        profile = UserProfileInfo.objects.filter(user=self.user)[0]
        self.assertEqual(profile.phone, old_phone)
        self.assertNotEqual(profile.phone, new_phone)
        views.update_profile_info(self)
        profile = UserProfileInfo.objects.filter(user=self.user)[0]
        self.assertEqual(profile.phone, new_phone)
        self.assertNotEqual(profile.phone, old_phone)

    def test_remove_manager(self):
        self.user = self.getUser()

        m = models.market.objects.create(id=1)
        self.client.get('/submit_request/' + str(self.user.id) + '/1/')

        views.assign_manager(self, m.id, self.user.username)

        m = models.market.objects.filter(id=1)[0]
        self.assertEqual(m.market_manager, self.user.username)

        self.META = {}
        self.method = 'POST'
        self.POST = {}

        admin_password = '123'
        my_admin = User.objects.create_superuser('adminuser', 'myemail@test.com', admin_password)
        c = Client()
        c.login(username=my_admin.username, password=admin_password)
        self.client = c
        self.user = my_admin

        views.remove_manager(self, m.id)

        m = models.market.objects.filter(id=1)[0]
        self.assertEqual(m.market_manager, '')

    def test_attending_users(self):
        
        self.user = self.getUser()

        market = models.market.objects.create(id=1, name='test market', city='test city', address='test address', market_manager=self.user.username)
        event = models.myEvent.objects.create(user_id=self.user.id, market_id=market.id)
        self.META = {}

        response = views.attending_users(self, 1)
        self.assertEqual(response.status_code, 200)

    def test_report_user(self):
        self.user = self.getUser()
        self.META = {}
        response = views.report_user(self, self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_send_report(self):
        self.user = self.getUser()
        self.META = {}
        self.method = 'POST'
        self.POST = {'message': 'test message'}
        
        admin_password = '123'
        my_admin = User.objects.create_superuser('adminuser', 'myemail@test.com', admin_password)

        m = models.Message.objects.all()
        self.assertEqual(len(m), 0)
        
        views.send_report(self, self.user.username)
        
        m = models.Message.objects.all()
        self.assertEqual(len(m), 1)

    def test_facebook_page(self):
        self.user = self.getUser()

        market = models.market.objects.create(id=1, name='test market', city='test city', address='test address', market_manager=self.user.username)
        self.META = {}

        response = views.facebook_page(self, 1)
        self.assertEqual(response.status_code, 200)

    # def test_post_to_facebook(self):  # needs to be fixed
        # self.assertEqual(True, True)