from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import TransantiagoUser
import json


class URLStatusTestCase(TestCase):
    """ """
    URL_PREFIX = '/timePerStreet/'
    GET_URLS = [
        reverse("getCount"),
        reverse("driversTable"),
        reverse("getDriversTable"),
    ]
    POST_URLS = [
    ]

    def setUp(self):
        ''' '''
        # log in inputs
        username = "Felipinbombin"
        password = "Felipinbombin"
        email = "a@b.cl"

        # create user on django contrib user model
        superUser = User.objects.create_superuser(username=username, email=email, password=password)
        TransantiagoUser.objects.create(user=superUser)

        self.client = Client()
        response = self.client.login(username=username, password=password)
        self.assertTrue(response)


    def makeGetRequest(self, url, params={}):

        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)

        return response

    def makePostRequest(self, url, params={}):

        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 200)

        return response

    def printJson(self, jsonResponse):

        print(json.dumps(jsonResponse,
                         sort_keys=True,
                         indent=4,
                         separators=(',', ': ')))

    def test_askGETRequests(self):
        '''  '''
        for url in self.GET_URLS:
            self.makeGetRequest(url, {})

    def test_askPOSTRequests(self):
        '''  '''
        for url in self.POST_URLS:
            self.makePostRequest(url, {})
