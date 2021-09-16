#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """CommentsConfig
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
