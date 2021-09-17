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
from issues.models import Issue

# Create your tests here.
from .models import Comment


class CommentsTest(APITestCase):
    """ Test module for Comment """

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
        self.comment = Comment.objects.create(value="test comment", issue=self.issue, owner=self.user1)
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.token = response_data['token']
        self.client = Client(enforce_csrf_checks=True)
        self.base_url = "/api/issues/comment/"

    def test_comment_list(self):
        """ Test if a user can list comments and with JWT response token """
        resp = self.client.get(self.base_url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_comment_list_fail(self):
        """ Test if a user can list comments and without JWT response token """
        resp = self.client.get(self.base_url, HTTP_AUTHORIZATION=f'Bearer incorrect token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_detail(self):
        """test_comment_detail

        """
        resp = self.client.get(f'{self.base_url}{self.comment.id}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_comment_detail_fail_unauthenticated(self):
        """test_comment_detail_fail

        """
        resp = self.client.get(f'{self.base_url}{self.comment.id}/', HTTP_AUTHORIZATION=f'Bearer incorrect_token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_detail_fail_incorrect_pk(self):
        """test_comment_detail_fail_incorrect_pk
        """
        resp = self.client.get(f'{self.base_url}{uuid.uuid4()}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_create(self):
        """test_comment_create
        """
        data = {"value": "test comment 2", "issue": self.issue.id}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_comment_create_fail_unauthenticated(self):
        """test_comment_create_fail_unauthenticated
        """
        data = {"value": "test comment 2", "issue": self.issue.id}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer incorrect')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_issue_create_fail_incorrect_issue(self):
        """test_issue_create_fail_incorrect_project
        """
        data = {"value": "test comment 2", "issue": uuid.uuid4()}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_create_fail_bad_request(self):
        """test_comment_create_fail_bad_request
        """
        data = {"issue": self.issue.id}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update(self):
        """test_comment_update
        """
        data = dict(value="Update Comment 1")
        resp = self.client.patch(f'{self.base_url}{self.comment.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.token}', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_comment_update_fail_incorrect_pk(self):
        """test_comment_update_fail_incorrect_pk
        """
        data = dict(value="Update Title 1")
        resp = self.client.patch(f'{self.base_url}{uuid.uuid4()}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_update_fail_unauthenticated(self):
        """test_comment_update_fail_unauthenticated
        """
        data = dict(value="Update value")
        resp = self.client.patch(f'{self.base_url}{self.comment.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_delete(self):
        """test_comment_delete

        """
        resp = self.client.delete(f'{self.base_url}{self.comment.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_delete_fail_unauthenticated(self):
        """test_comment_delete_fail_unauthenticated

        """
        resp = self.client.delete(f'{self.base_url}{self.comment.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_delete_incorrect_pk(self):
        """test_comment_delete_incorrect_pk
        """
        resp = self.client.delete(f'{self.base_url}{uuid.uuid4()}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
