#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from typing import Any
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .permissions import has_admin_permission
from .serializers import ProjectSerializer
from .models import Project


class ProjectListCreateAPIView(ListCreateAPIView):
    """ProjectListCreateAPIView
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ProjectSerializer

    def get_queryset(self) -> Any:
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
        return Project.objects.all()

    def post(self, request, *args, **kwargs):
        """post

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if has_admin_permission(request):
            return self.create(request, *args, **kwargs)
        else:
            return Response({"message": "Permission Denied! Only Admin can create the project"},
                            status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer) -> None:
        """perform_create
        :param serializer:
        :return:
        """
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        """create
        :param request:
        :param args:
        :param kwargs:
        :return: Response instance
        :rtype: Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    """ProjectDetailAPIView
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def patch(self, request, *args, **kwargs):
        """patch
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if has_admin_permission(request):
            return self.partial_update(request, *args, **kwargs)
        else:
            return Response({"message": "Permission Denied! Only Admin can update the project"},
                            status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        """delete
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if has_admin_permission(request):
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"message": "Permission Denied! Only Admin can delete the project"},
                            status.HTTP_401_UNAUTHORIZED)
