#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
import uuid
from django.db import models


# Create your models here.
class Project(models.Model):
    """Project ORM model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=300)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = "projects"
