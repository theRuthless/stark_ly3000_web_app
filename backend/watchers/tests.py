#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 2021
@author: sagrana
"""
import datetime
import uuid

from django.test import Client
import json
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from issues.models import Issue
from .models import Watcher
# Create your tests here.


class WatcherTest(APITestCase):
    """ Test module for Watcher """

    def setUp(self):
        """setUp
        """
        # creating user instance with manager role
        self.user1 = User.objects.create_user(
            email='test1@test.com',
            password='test',
            role="2"
        )

        # creating user instance with admin
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin',
        )

        # creating user instance with standard role
        self.standard_user = User.objects.create_user(
            email='test2@test.com',
            password='test',
            role="3"
        )

        # creating issue instance
        self.issue = Issue.objects.create(type=1, status=1, reporter=self.user1,
                                          title="Issue 1",
                                          description="Test description"
                                          )
        self.issue2 = Issue.objects.create(type=2, status=2, reporter=self.user1,
                                           title="Issue 2",
                                           description="Test description"
                                           )

        # create watcher instance
        self.watcher = Watcher.objects.create(issue=self.issue, name=self.user1, owner=self.user1)

        # fetching JWT token for admin user
        url = "/api/auth/signin"
        data = {
            'email': 'admin@test.com',
            'password': 'admin'
        }
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.admin_token = response_data['token']

        # fetching JWT token for manager role user
        data = {
            'email': 'test1@test.com',
            'password': 'test'
        }
        user_response = self.client.post(url, data)
        user_response_data = json.loads(user_response.content)
        self.manager_token = user_response_data['token']

        # fetching JWT token for standard role user
        data = {
            'email': 'test2@test.com',
            'password': 'test'
        }
        standard_user_response = self.client.post(url, data)
        standard_user_response_data = json.loads(standard_user_response.content)
        self.standard_user_token = standard_user_response_data['token']

        # Initializing Client instance for api calls
        self.client = Client(enforce_csrf_checks=True)

        # Initialized base url for watcher
        self.base_url = "/api/watchers/"

    def test_watcher_list(self):
        """ Test if a user can list watcher and with JWT response token """
        resp = self.client.get(self.base_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_watcher_list_fail(self):
        """ Test if a user can list watcher and without JWT response token """
        resp = self.client.get(self.base_url, HTTP_AUTHORIZATION=f'Bearer incorrect token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_watcher_detail(self):
        """test_watcher_detail

        """
        resp = self.client.get(f'{self.base_url}{self.watcher.id}/', HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_watcher_detail_fail_unauthenticated(self):
        """test_watcher_detail_fail_unauthenticated

        """
        resp = self.client.get(f'{self.base_url}{self.watcher.id}/', HTTP_AUTHORIZATION=f'Bearer incorrect_token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_watcher_detail_fail_incorrect_pk(self):
        """test_watcher_detail_fail_incorrect_pk
        """
        resp = self.client.get(f'{self.base_url}{uuid.uuid4()}/', HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_watcher_create(self):
        """test_watcher_create
        """
        data = {"name": self.admin.id, "issue": self.issue2.id}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_watcher_create_fail_unauthenticated(self):
        """test_watcher_create_fail_unauthenticated
        """
        data = {"name": self.admin.id, "issue": self.issue2.id}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer incorrect')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_watcher_create_fail_bad_request(self):
        """test_watcher_create_fail_bad_request
        """
        data = {"issue": self.issue2.id}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_watcher_delete(self):
        """test_watcher_delete

        """
        resp = self.client.delete(f'{self.base_url}{self.watcher.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_watcher_delete_fail_unauthenticated(self):
        """test_watcher_delete_fail_unauthenticated
        """
        resp = self.client.delete(f'{self.base_url}{self.watcher.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_watcher_delete_incorrect_pk(self):
        """test_watcher_delete_incorrect_pk
        """
        resp = self.client.delete(f'{self.base_url}{uuid.uuid4()}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
