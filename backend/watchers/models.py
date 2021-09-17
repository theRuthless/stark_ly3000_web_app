# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 2021
@author: sagrana
"""
import uuid
from django.db import models

from .utils import notify_user


class WatcherManager(models.Manager):
    pass


# Create your models here.
class Watcher(models.Model):
    """Watcher model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.ForeignKey("users.User", on_delete=models.CASCADE)
    issue = models.ForeignKey("issues.Issue", on_delete=models.CASCADE, related_name="watchers")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="watcher_owner")

    objects = WatcherManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Watcher, self).save(force_insert=False, force_update=False, using=None,
                                  update_fields=None)
        notify_user(getattr(self, "id"))

    class Meta:
        db_table = "watchers"
        unique_together = ("name", "issue")

