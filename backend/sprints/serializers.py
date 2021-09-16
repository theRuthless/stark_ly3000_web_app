#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import serializers, fields
from .models import Sprint


class SprintSerializer(serializers.ModelSerializer):
    """SprintSerializer
    """
    start_date = fields.DateField(input_formats=['%Y-%m-%d'])
    end_date = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        """Meta
        """
        model = Sprint
        fields = ("id", "name", "project", "start_date", "end_date", "sprint_issues")
        read_only_fields = ("id", "sprint_issues", "start_date", "end_date")
