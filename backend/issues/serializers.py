#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import serializers
from .comments.serializers import CommentSerializer
from .models import Issue
from .worklog.serializers import WorkLogSerializer


class IssueUserSerializer(serializers.ModelSerializer):
    """IssueUserSerializer
    """
    class Meta:
        """Meta
        """
        model = "users.User"
        fields = "email"


class IssueSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    worklogs = WorkLogSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = ("id", "title", "type", "status", "description", "reporter", "assignee", "comments", "worklogs",
                  "watchers",
                  "project",
                  "sprint")
        read_only_fields = ("id", "reporter", "watchers")
