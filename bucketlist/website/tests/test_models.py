# -*- coding: utf-8 -*-

from django.test import TestCase
from website.models import Bucketlist, BucketlistItem
from django.contrib.auth.models import User


class BucketListTestCase(TestCase):

    def setUp(self):
        self.title = "Before I turn 80"
        user = User.objects.create_user(
            username="john_doe",
            first_name="John",
            last_name="Doe",
            email="john.doe@anon.ms")
        user.save()
        self.user = user

        bucketlist = Bucketlist(
            title=self.title,
            user_id=self.user.id)
        bucketlist.save()

    def test_that_bucket_list_can_be_created(self):
        """Tests that bucketlists can be created.
        """
        bucketlist = Bucketlist.objects.get(
            title=self.title)

        self.assertEqual(type(bucketlist.id), int)

    def test_that_bucket_list_item_can_be_created(self):
        """Tests that bucketlist items can be created.
        """
        bucketlist = Bucketlist.objects.get(
            title=self.title)
        bucketlist_item = BucketlistItem(
            title="Visit India",
            done=False,
            bucketlist_id=bucketlist.id,
            user_id=self.user.id)
        bucketlist_item.save()

        bucketlist_item = BucketlistItem.objects.get(
            title="Visit India")

        self.assertEqual(bucketlist_item.done, False)
        self.assertEqual(
            bucketlist_item.bucketlist_id,
            bucketlist.id)
