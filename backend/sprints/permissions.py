#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""


def has_admin_manager_permission(request):
    return request.user.role == 1 or request.user.is_superuser or request.user.role == 2
