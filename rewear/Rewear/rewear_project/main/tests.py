from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from registry.models import UserProfileInfo
from .models import market, submission
from .views import *


class Test(TestCase):

    # this one is okay
    def test_home(self):
        response = self.client.get('//')
        self.assertEqual(response.status_code, 200)

    #this one is okay
    def test_about(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    # def test_areyousure(self):
    #    response = self.client.get('/areyousure/')
    #    self.assertEqual(response.status_code, 200)

    # def test_messagetouser(self):
    #     response = self.client.get('/messagetouser/')
    #     self.assertEqual(response.status_code, 200)

    # def test_sendmessage(self):
    #     response = self.client.get('/sendmessage/')
    #     self.assertEqual(response.status_code, 200)

    # def test_editabout(self):
    #     response = self.client.get('/editabout/')
    #     self.assertEqual(response.status_code, 200)
    #
    def test_saveabout(self):
        response = self.client.get('/saveabout/')
        self.assertEqual(response.status_code, 200)

    # this one is okay
    def test_search(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    # this one is  okay
    def test_search_page(self):
        response = self.client.get('/search_page/')
        self.assertEqual(response.status_code, 200)

    # def test_market_page(self):
    #     response = self.client.get('/market_page/')
    #     self.assertEqual(response.status_code, 200)

    # def test_update_market(self):
    #     response = self.client.get('/update_market/')
    #     self.assertEqual(response.status_code, 200)
    #
    # this one is okay
    def test_submissions(self):
        response = self.client.get('/submissions/')
        self.assertEqual(response.status_code, 200)

    def test_submit_request(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.market = Market.objects.create(name='testmarket', address='testaddress')
        self.user.save()
        self.market.save()
        url = reverse('submit_request', args=[self.user.id, self.market.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submit_request.html')
        self.assertContains(response, 'Submit Request')
        self.user.delete()
        self.market.delete()


    def test_feedback(self):
        response = self.client.get('/feedback/')
        self.assertEqual(response.status_code, 404)

    def test_update_profilepic(self):
        response = self.client.get('/update_profilepic/')
        self.assertEqual(response.status_code, 404)

    def test_getUserProfileInfo(self):
        response = self.client.get('/getUserProfileInfo/')
        self.assertEqual(response.status_code, 404)

    def test_toggle_active(self):
        response = self.client.get('/toggle_active/')
        self.assertEqual(response.status_code, 404)