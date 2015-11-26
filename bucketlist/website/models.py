# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from .utils import normalize


class BaseModel(models.Model):
    """ An abstract model that has common information for
    `Bucketlist` and `BucketlistItem`
    """
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def search(cls, query_string):
        """Searches the model table for occurences of words
        in the query string"""
        query = None
        query_terms = normalize(query_string)
        for term in query_terms:
            or_query = None  # Query to search for a given term in each field
            query_obj = models.Q(**{"name__icontains": term})
            if or_query is None:
                or_query = query_obj
            else:
                or_query = or_query | query_obj
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return cls.objects.filter(query).order_by('date_created')

    def __str__(self):
        return self.name


class Bucketlist(BaseModel):
    """A model representation of the Bucketlist table"""
    user = models.ForeignKey(User)

    def num_items_done(self):
        """Returns number of bucketlist items completed"""
        return self.bucketlistitem_set.filter(done=True).count()


class BucketlistItem(BaseModel):
    """A model representation of the Bucketlist item table"""
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    bucketlist = models.ForeignKey(Bucketlist)


class UserProfile(BaseModel):
    """A model representation of the user's profile"""
    bio = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User)
