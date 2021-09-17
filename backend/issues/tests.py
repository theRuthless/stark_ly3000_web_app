#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 2021
@author: sagrana
"""
import uuid

from django.test import Client
import json
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Issue

# Create your tests here.


class IssueTest(APITestCase):
    """ Test module for Issue """

    def setUp(self):
        """setUp
        """
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
        self.issue = Issue.objects.create(type=1, status=1, reporter=self.user1,
                                          title="Issue 1",
                                          description="Test description"
                                          )
        self.issue2 = Issue.objects.create(type=1, status=1, reporter=self.user1,
                                           title="Issue 2",
                                           description="Test description"
                                           )
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.token = response_data['token']
        self.client = Client(enforce_csrf_checks=True)

    def test_issues_list(self):
        """ Test if a user can list issues and with JWT response token """
        resp = self.client.get('/api/issues/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_issues_list_fail(self):
        """ Test if a user can list issues and without JWT response token """
        resp = self.client.get('/api/issues/', HTTP_AUTHORIZATION=f'Bearer incorrect token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_issues_detail(self):
        """test_issues_detail

        """
        resp = self.client.get(f'/api/issues/{self.issue.id}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_issues_detail_fail_unauthenticated(self):
        """test_issues_detail_fail

        """
        resp = self.client.get(f'/api/issues/{self.issue.id}/', HTTP_AUTHORIZATION=f'Bearer incorrect_token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_issues_detail_fail_incorrect_pk(self):
        """test_issues_detail_fail_url
        """
        resp = self.client.get(f'/api/issues/{uuid.uuid4()}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_issue_create(self):
        """test_issues_detail_fail_url
        """
        data = {"type": 1, "description": "Test description", "title": "Issue 3", "reporter": self.user1}
        resp = self.client.post(f'/api/issues/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_issue_create_fail_unauthenticated(self):
        """test_issue_create_fail_unauthenticated
        """
        data = {"type": 1, "description": "Test description", "title": "Issue 3", "reporter": self.user1}
        resp = self.client.post(f'/api/issues/', data=data, HTTP_AUTHORIZATION=f'Bearer incorrect')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_issue_create_fail_incorrect_project(self):
        """test_issue_create_fail_incorrect_project
        """
        data = {"type": 1, "description": "Test description", "title": "Issue 3",
                "reporter": self.user1,
                "project": 1}
        resp = self.client.post(f'/api/issues/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_issue_create_fail_bad_request(self):
        """test_issue_create_fail_bad_request
        """
        data = {"description": "Test description",
                "reporter": self.user1,
                }
        resp = self.client.post(f'/api/issues/', data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_issue_update(self):
        """test_issue_update
        """
        data = dict(title="Update Title 1")
        resp = self.client.patch(f'/api/issues/{self.issue.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.token}', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_issue_update_fail_incorrect_pk(self):
        """test_issue_update
        """
        data = dict(title="Update Title 1")
        resp = self.client.patch(f'/api/issues/{uuid.uuid4()}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_issue_update_fail_unauthenticated(self):
        """test_issue_update_fail_unauthenticated
        """
        data = dict(title="Update Title 1")
        resp = self.client.patch(f'/api/issues/{self.issue.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_issue_delete(self):
        """test_issue_delete

        """
        resp = self.client.delete(f'/api/issues/{self.issue.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_issue_delete_fail_unauthenticated(self):
        """test_issue_delete_fail_unauthenticated

        """
        resp = self.client.delete(f'/api/issues/{self.issue.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_issue_delete_incorrect_pk(self):
        """test_issue_delete_fail_unauthenticated
        """
        resp = self.client.delete(f'/api/issues/{uuid.uuid4()}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
