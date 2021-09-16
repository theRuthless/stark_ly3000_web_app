#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from django.urls import path
from .views import ProjectDetailAPIView, ProjectListCreateAPIView

app_name = 'projects'

urlpatterns = [
    path('', ProjectListCreateAPIView.as_view(), name="list"),
    path('<uuid:pk>/', ProjectDetailAPIView.as_view(), name="detail"),
]
