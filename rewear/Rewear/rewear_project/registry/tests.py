from django.test import TestCase
from registry.models import UserProfileInfo
# Create your tests here.
from django.contrib.auth.models import User
def test_profile(self):
    self.user = User.objects.create_user(username='testuser', password='testpass')
    self.user.save()
    self.userprofileinfo = UserProfileInfo.objects.create(user=self.user, userType='Buyer', phone='1234567890',
                                                          picture='static\\media\\profile_pics\\default.jpg',
                                                          about='testabout')
    self.userprofileinfo.save()
    response = self.client.get('/profile/')
    self.assertEqual(response.status_code, 200)
    self.userprofileinfo.delete()
    self.user.delete()

def test_profile_update(self):
    self.user = User.objects.create_user(username='testuser', password='testpass')
    self.user.save()
    self.userprofileinfo = UserProfileInfo.objects.create(user=self.user, userType='Buyer', phone='1234567890',
                                                          picture='static\\media\\profile_pics\\default.jpg',
                                                          about='testabout')
    self.userprofileinfo.save()
    response = self.client.get('/profile_update/')
    self.assertEqual(response.status_code, 200)
    self.userprofileinfo.delete()
    self.user.delete()

def test_profile_update_save(self):
    self.user = User.objects.create_user(username='testuser', password='testpass')
    self.user.save()
    self.userprofileinfo = UserProfileInfo.objects.create(user=self.user, userType='Buyer', phone='1234567890',
                                                          picture='static\\media\\profile_pics\\default.jpg',
                                                          about='testabout')
    self.userprofileinfo.save()
    response = self.client.get('/profile_update_save/')
    self.assertEqual(response.status_code, 200)
    self.userprofileinfo.delete()
    self.user.delete()

def test_register(self):
    response = self.client.get('/register/')
    self.assertEqual(response.status_code, 200)

def test_login(self):
    response = self.client.get('/login/')
    self.assertEqual(response.status_code, 200)

def test_logout(self):
    response = self.client.get('/logout/')
    self.assertEqual(response.status_code, 302)

