from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# from myproject.apps.core.models import Account
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import Token
from .api import serializers
from . import models


class StreamPlatform(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="pass@1234") # create the user
        self.token = Token.objects.get(user__username=self.user) # access his token
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key) # send credentials    
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 Streaming Platform",website="https://netflix.com")

        
    def test_streamplatform_create(self): # send req in the form of normal user
        data = {
            "name": "Netflix",
            "About": "#1 Streaming Platform",
            "website": "https://netflix.com",
        }
        response = self.client.post(reverse("streamplatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """ Normal user can send get req for individual elements of for lists"""
    
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_ind(self): # Get individual element
        response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
"""WatchList testcase"""
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="nandan", password="nandu1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 Streaming Platform",website="https://netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Bahubali 2", storyline= "King Story",active= True) # Create a movie
        
        
    def test_watchlist_create(self): # we have created a movie manually
        data = {
            "title": "3 idiots",
            "storyline": "Life story",
            "platform":self.stream,
            "active":True,
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list')) # Get entire movie
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,))) # Get single movie
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.get().title, "Bahubali 2") # match the title
        self.assertEqual(models.WatchList.objects.count(), 1) # match count
        
    
class ReviewTestCase(APITestCase):
    # in doc u'll find a force authentication where u can login and logout as a random user
    def setUp(self):
        self.user = User.objects.create_user(username="nandan", password="nandu1234")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        """ creating stream and movie"""
        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 Streaming Platform",website="https://netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Bahubali 2", storyline= "King Story",active= True) # Create a movie
        # creating 2nd watchlist cuz we're not allowed to send 2 reviews to same watchlist
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="Bahubali 1", storyline= "King Story",active= True) # Create a movie
        self.review = models.Review.objects.create(review_user = self.user, rating=5, description='Great Movie', whatslist=self.watchlist2, active=True)

    def test_review_create(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"Great Movie!",
            "whatslist":self.watchlist,
            "active":True
        }
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # self.assertEqual(models.Review.objects.get().rating, 5) # match the rating
        self.assertEqual(models.Review.objects.count(), 2) # match count
        
    """ add review as un-authenticated user"""
    def test_review_create_unauthenticated(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"Great Movie!",
            "whatslist":self.watchlist,
            "active":True
        }
        
        self.client.force_authenticate(user=None) # Not logged in
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    """update a review"""
    def test_review_update(self):
        data = {
            "review_user":self.user,
            "rating":4,
            "description":"Great Movie! - updated",
            "whatslist":self.watchlist,
            "active":False
        }
        
        
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)