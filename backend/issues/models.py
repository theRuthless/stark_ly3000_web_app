#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 2021
@author: sagrana
"""
import uuid
from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext as _
from .constants import ROLE_CHOICES, STATUS_CHOICES

# Create your models here.


class Issue(models.Model):
    """Issue model
    """
    # Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=True, default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=False, null=True, default=1)
    reporter = models.ForeignKey("users.User", on_delete=models.CASCADE)
    assignee = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="owner", null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="issues", null=True)
    sprint = models.ForeignKey("sprints.Sprint", on_delete=models.CASCADE, related_name="sprint_issues", null=True)
    objects = Manager()

    def __str__(self):
        """__str__
        :return:
        """
        return self.title

    class Meta:
        """
        to set table name in database
        """
        db_table = "issue"
        unique_together = ('type', 'title')
