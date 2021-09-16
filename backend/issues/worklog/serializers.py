#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from rest_framework import serializers
from .models import WorkLog


class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = ("id", "time_spent", "description", "issue", "logged_at")
        read_only_fields = ("logged_at", "id",)
