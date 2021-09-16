#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import IssueSerializer
from .models import Issue


class IssueListCreateAPIView(ListCreateAPIView):
    """IssueListCreateAPIView
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = IssueSerializer

    def get_queryset(self):
        """
                Get the list of items for this view.
                This must be an iterable, and may be a queryset.
                Defaults to using `self.queryset`.

                This method should always be used rather than accessing `self.queryset`
                directly, as `self.queryset` gets evaluated only once, and those results
                are cached for all subsequent requests.

                You may want to override this if you need to provide different
                querysets depending on the incoming request.

                (Eg. return a list of items that is specific to the user)
        """

        return Issue.objects.all()

    def perform_create(self, serializer):
        """perform_create
        :param serializer:
        :return:
        """
        serializer.save(reporter=self.request.user)

    def create(self, request, *args, **kwargs):
        """create
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IssueDetailAPIView(RetrieveUpdateDestroyAPIView):
    """IssueDetailAPIView
    """
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def patch(self, request, *args, **kwargs):
        """patch
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass
