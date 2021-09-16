from django.test import TestCase, Client
import json
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

# Create your tests here.


class UserTest(APITestCase):
    """ Test module for User """

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='test1@test.com',
            password='test',
            role="2"
        )

        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin',
        )
        url = "/api/auth/signin"
        data = {
            'email': 'admin@test.com',
            'password': 'admin'
        }
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.token = response_data['token']

    def test_issues_list(self):
        """ Test if a user can login and get a JWT response token """
        self.client = Client(enforce_csrf_checks=True)
        resp = self.client.get('/api/issues/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_issues_list_fail(self):
        """ Test if a user can login and get a JWT response token """
        self.client = Client(enforce_csrf_checks=True)
        resp = self.client.get('/api/issues/', HTTP_AUTHORIZATION=f'Bearer incorrect token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
