#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
from rest_framework import routers
from .views import CommentViewSet

router = routers.SimpleRouter()

router.register('', CommentViewSet)
urlpatterns = router.urls
