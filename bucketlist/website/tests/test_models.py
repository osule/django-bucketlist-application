# -*- coding: utf-8 -*-

from django.test import TestCase
from website.models import Bucketlist, BucketlistItem, UserProfile
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
            name=self.title,
            user_id=self.user.id)
        bucketlist.save()

    def test_that_bucket_list_can_be_created(self):
        """Ensures that bucketlists can be created.
        """
        bucketlist = Bucketlist.objects.get(
            name=self.title)

        self.assertEqual(type(bucketlist.id), int)

    def test_that_bucket_list_item_can_be_created(self):
        """Ensures that bucketlist items can be created.
        """
        bucketlist = Bucketlist.objects.get(
            name=self.title)
        bucketlist_item = BucketlistItem(
            name="Visit India",
            done=False,
            bucketlist=bucketlist,
            user_id=self.user.id)
        bucketlist_item.save()

        bucketlist_item = BucketlistItem.objects.get(
            name="Visit India")

        self.assertEqual(bucketlist_item.done, False)
        self.assertEqual(
            bucketlist_item.bucketlist_id,
            bucketlist.id)

    def test_that_models_can_be_queried(self):
        """Ensures that models can be queried.
        """
        bucketlist = Bucketlist.objects.get(
            name=self.title)
        bucketlist_item = BucketlistItem(
            name="Visit India",
            done=False,
            bucketlist=bucketlist,
            user_id=self.user.id)
        bucketlist_item.save()

        query_results = BucketlistItem.search('Visit India')

        self.assertIn(bucketlist_item, query_results)

    def test_that_items_done_can_be_retrieved(self):
        """Ensure that items done can be retrieved
        """
        bucketlist = Bucketlist.objects.get(
            name=self.title)
        bucketlist_item = BucketlistItem(
            name="Visit India",
            done=False,
            bucketlist=bucketlist,
            user_id=self.user.id)
        bucketlist_item.save()

        self.assertEqual(bucketlist.num_items_done(), 0)

        bucketlist_item.done = True
        bucketlist_item.save()
        self.assertEqual(bucketlist.num_items_done(), 1)

    def test_that_user_profile_can_be_created(self):
        """Ensure that user profile can be created
        """
        user_profile = UserProfile(bio="Some bio info", age=24, user=self.user)
        user_profile.save()

        test_user_profile = UserProfile.objects.get(user=self.user)

        self.assertEqual(test_user_profile.id, user_profile.id)
