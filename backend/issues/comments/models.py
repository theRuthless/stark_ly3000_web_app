#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
import uuid
from django.utils.translation import gettext as _
from django.db import models
from django.db.models import Manager


class Comment(models.Model):
    """Comment Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.CharField(max_length=300)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    issue = models.ForeignKey("issues.Issue", on_delete=models.CASCADE, related_name="comments", null=True)
    created_at = models.DateTimeField(_("Date Created"), auto_now_add=True, null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return self.value

    class Meta:
        """
        to set table name in database
        """
        db_table = "comment"
