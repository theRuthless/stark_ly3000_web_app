#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
import uuid
from django.utils.translation import gettext as _
from django.db import models


# Create your models here.
class WorkLog(models.Model):
    """WorkLog model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_spent = models.PositiveIntegerField()
    description = models.CharField(max_length=300, blank=False)
    logged_at = models.DateTimeField(_("Date Created"), auto_now_add=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    issue = models.ForeignKey("issues.Issue", on_delete=models.CASCADE, related_name="worklogs", null=True)
    objects = models.Manager()

    class Meta:
        """Meta
        """
        db_table = "work_log"


