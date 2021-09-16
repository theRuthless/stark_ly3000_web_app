#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from django.urls import path, include
from .views import IssueDetailAPIView, IssueListCreateAPIView

app_name = 'issues'

urlpatterns = [
    path('comment/', include('issues.comments.urls')),
    path('', IssueListCreateAPIView.as_view(), name="list"),
    path('<uuid:pk>/', IssueDetailAPIView.as_view(), name="detail"),
]
