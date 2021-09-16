# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 2021
@author: sagrana
"""
import uuid
from django.db import models


# Create your models here.
class Sprint(models.Model):
    """Sprint model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="sprints")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        """Meta
        """
        db_table = "sprint"

