from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# from myproject.apps.core.models import Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token



class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "test@gmail.com",
            "password": "testpass123",
            "password2": "testpass123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # match whether 2 status codes are same
        
        
class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="testpass123") # this will run before test_Login and test_Logout
        
    def test_Login(self):
        data = {
            "username":"test",
            "password":"testpass123",
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # match whether 2 status codes are same

    def test_logout(self): # We need to send token to logout 
        self.token = Token.objects.get(user__username="test")# get token of the particular user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # pass this token to get the credentials or to log in, now wr're logged in
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK) # match whether 2 status codes are same                  