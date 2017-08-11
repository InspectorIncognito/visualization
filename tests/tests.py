from django.test import TestCase, Client

import json


class URLStatusTestCase(TestCase):
    """ """
    URL_PREFIX = '/timePerStreet/'
    GET_URLS = [
        ''
    ]
    POST_URLS = [
        ''
    ]

    def makeGetRequest(self, url, params={}):

        c = Client()
        response = c.get(url, params)
        self.assertEqual(response.status_code, 200)

        return response

    def makePostRequest(self, url, params={}):

        c = Client()
        response = c.post(url, params)
        self.assertEqual(response.status_code, 200)

        return response

    def printJson(self, jsonResponse):

        print(json.dumps(jsonResponse,
                         sort_keys=True,
                         indent=4,
                         separators=(',', ': ')))

    def setUp(self):
        ''' '''
        pass

    def test_askGETRequests(self):
        '''  '''
        for url in self.GET_URLS:
            self.makeGetRequest(url, {})

    def test_askPOSTRequests(self):
        '''  '''
        for url in self.POST_URLS:
            self.makePostRequest(url, {})
