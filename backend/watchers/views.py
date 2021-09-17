#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 2021
@author: sagrana
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import WatcherSerializer
from .models import Watcher


class WatcherViewSet(viewsets.ModelViewSet):
    """WatcherViewSet
    """
    serializer_class = WatcherSerializer
    queryset = Watcher.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def perform_create(self, serializer) -> None:
        """perform_create
        :param serializer:
        :return:
        """
        serializer.save(owner=self.request.user)
