# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Bucketlist(models.Model):
    """A model representation of the Bucketlist table
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def bucketlistitem_count_done(self):
        """Gets the count of bucketlist items done
        """
        return BucketlistItem.objects.filter(
            bucketlist=self, done=True).count()

    def bucketlistitem_count_undone(self):
        """Gets the count of bucketlist items undone
        """
        return BucketlistItem.objects.filter(
            bucketlist=self, done=False).count()


class BucketlistItem(models.Model):
    """A model representation of the Bucketlist item table
    """
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    bucketlist = models.ForeignKey(Bucketlist)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
