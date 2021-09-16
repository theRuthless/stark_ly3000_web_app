#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from .comments.models import Comment
from .comments.serializers import CommentSerializer
from .models import Issue
from .worklog.serializers import WorkLogSerializer


class IssueUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = "users.User"
        fields = "email"


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    worklogs = WorkLogSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ("id", "title", "type", "description", "reporter", "assignee", "comments", "worklogs")
        read_only_fields = ("id",)
