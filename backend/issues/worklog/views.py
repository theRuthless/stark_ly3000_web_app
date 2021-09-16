#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import WorkLogSerializer
from .models import WorkLog


class WorkLogViewSet(viewsets.ModelViewSet):
    """CommentViewSet
    """
    serializer_class = WorkLogSerializer
    queryset = WorkLog.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
