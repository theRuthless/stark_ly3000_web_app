#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """ProjectSerializer
    """

    class Meta:
        """Meta class
        """
        model = Project
        fields = ("id", "title", "description", "owner", "issues", "sprints")
        read_only_fields = ("id", "owner", "issues")
