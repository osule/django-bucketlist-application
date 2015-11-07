# -*- coding: utf-8 -*-

from django.test import TestCase
from bucketlist.models import Bucketlist, BucketlistItem
from django.contrib.auth.models import User
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'
    admin = False


class BucketListTestCase(TestCase):

    def setUp(self):
        self.title = "Before I turn 80"
        self.user = UserFactory.build()

        Bucketlist.objects.create(
            title=self.title,
            user_id=self.user.id)

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
        BucketlistItem.objects.create(
            title="Visit India",
            done=False,
            bucketlist_id=bucketlist.id,
            user_id=self.user.id)

        bucketlist_item = BucketlistItem.objects.get(
            title="Visit India")

        self.assertEqual(bucketlist_item.done, False)
        self.assertEqual(
            bucketlist_item.bucketlist_id,
            bucketlist.id)
