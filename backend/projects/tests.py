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
from .models import Project
# Create your tests here.


class ProjectLogTest(APITestCase):
    """ Test module for Project """

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

        self.standard_user = User.objects.create_user(
            email='test2@test.com',
            password='test',
            role="3"
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
        self.project = Project.objects.create(title="Project 1", description="Project decription", owner=self.admin)
        response = self.client.post(url, data)
        response_data = json.loads(response.content)
        self.admin_token = response_data['token']
        data = {
            'email': 'test1@test.com',
            'password': 'test'
        }
        user_response = self.client.post(url, data)
        user_response_data = json.loads(user_response.content)
        self.manager_token = user_response_data['token']
        data = {
            'email': 'test2@test.com',
            'password': 'test'
        }
        standard_user_response = self.client.post(url, data)
        standard_user_response_data = json.loads(standard_user_response.content)
        self.standard_user_token = standard_user_response_data['token']
        self.client = Client(enforce_csrf_checks=True)
        self.base_url = "/api/projects/"

    def test_project_list(self):
        """ Test if a user can list projects and with JWT response token """
        resp = self.client.get(self.base_url, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_project_list_fail(self):
        """ Test if a user can list projects and without JWT response token """
        resp = self.client.get(self.base_url, HTTP_AUTHORIZATION=f'Bearer incorrect token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_detail(self):
        """test_project_detail

        """
        resp = self.client.get(f'{self.base_url}{self.project.id}/', HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_project_detail_fail_unauthenticated(self):
        """test_project_detail_fail_unauthenticated

        """
        resp = self.client.get(f'{self.base_url}{self.project.id}/', HTTP_AUTHORIZATION=f'Bearer incorrect_token')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_detail_fail_incorrect_pk(self):
        """test_project_detail_fail_incorrect_pk
        """
        resp = self.client.get(f'{self.base_url}{uuid.uuid4()}/', HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_create(self):
        """test_project_create
        """
        data = {"title": "Project 2", "description": "Project 2 Description"}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_project_create_fail_no_permission_non_admin_user(self):
        """test_project_create_fail_no_permission_non_admin_user
        """
        data = {"title": "Project 3", "description": "Project 2 Description"}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_create_fail_no_permission_standard_user(self):
        """test_project_create_fail_no_permission_standard_user
        """
        data = {"title": "Project 3", "description": "Project 2 Description"}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.standard_user_token}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_create_fail_unauthenticated(self):
        """test_project_create_fail_unauthenticated
        """
        data = {"title": "Project 3", "description": "Project 2 Description"}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer incorrect')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_create_fail_bad_request(self):
        """test_work_log_create_fail_bad_request
        """
        data = {"description": "Project 2 Description"}
        resp = self.client.post(self.base_url, data=data, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_update(self):
        """test_project_update
        """
        data = dict(description="Update Project Description")
        resp = self.client.patch(f'{self.base_url}{self.project.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.admin_token}', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_project_update_no_permission_non_admin_user(self):
        """test_project_update_no_permission_non_admin_user
        """
        data = dict(description="Update Project Description")
        resp = self.client.patch(f'{self.base_url}{self.project.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.standard_user_token}',
                                 content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_update_fail_incorrect_pk(self):
        """test_project_update_fail_incorrect_pk
        """
        data = dict(description="Update description")
        resp = self.client.patch(f'{self.base_url}{uuid.uuid4()}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_update_fail_unauthenticated(self):
        """test_project_update_fail_unauthenticated
        """
        data = dict(description="Update description")
        resp = self.client.patch(f'{self.base_url}{self.project.id}/', data=data,
                                 HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_delete_no_permission_non_admin(self):
        """test_project_delete_no_permission_non_admin

        """
        resp = self.client.delete(f'{self.base_url}{self.project.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.standard_user_token}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_delete(self):
        """test_project_delete

        """
        resp = self.client.delete(f'{self.base_url}{self.project.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_project_delete_fail_unauthenticated(self):
        """test_project_delete_fail_unauthenticated

        """
        resp = self.client.delete(f'{self.base_url}{self.project.id}/',
                                  HTTP_AUTHORIZATION=f'Bearer {uuid.uuid4()}')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_delete_incorrect_pk(self):
        """test_project_delete_incorrect_pk
        """
        resp = self.client.delete(f'{self.base_url}{uuid.uuid4()}/',
                                  HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
