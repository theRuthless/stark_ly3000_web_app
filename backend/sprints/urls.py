#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
from django.urls import path
from .views import SprintListCreateAPIView, SprintDetailAPIView

app_name = 'sprints'

urlpatterns = [
    path('', SprintListCreateAPIView.as_view(), name="list"),
    path('<uuid:pk>/', SprintDetailAPIView.as_view(), name="detail"),
]
