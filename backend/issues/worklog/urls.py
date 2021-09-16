#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import routers
from .views import WorkLogViewSet

router = routers.SimpleRouter()

router.register('', WorkLogViewSet)
urlpatterns = router.urls
