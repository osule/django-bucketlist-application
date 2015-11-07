# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Bucketlist(models.Model):
    """A model representation of the Bucketlist table
    """
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class BucketlistItem(models.Model):
    """A model representation of the Bucketlist item table
    """
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    user_id = models.ForeignKey(User)
    bucketlist_id = models.ForeignKey(Bucketlist)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
