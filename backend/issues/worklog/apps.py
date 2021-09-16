#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
from django.apps import AppConfig


class WorklogConfig(AppConfig):
    """WorklogConfig
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'worklog'
