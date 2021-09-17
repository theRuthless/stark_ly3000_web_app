#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 2021
@author: sagrana
"""
from rest_framework import serializers
from .models import Watcher


class WatcherSerializer(serializers.ModelSerializer):
    """WatcherSerializer
    """
    class Meta:
        """Meta
        """
        model = Watcher
        fields = ("id", "name", "issue")
        read_only_fields = ("id",)

