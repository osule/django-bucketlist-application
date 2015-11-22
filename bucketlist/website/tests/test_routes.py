# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from faker import Faker


fakerInst = Faker()


class SetUpMixin(object):
    """Mixes the setUp for TestCases
    """
    @classmethod
    def setUpClass(cls):
        super(SetUpMixin, cls).setUpClass()
        cls.login_data = {
            'username': 'basil',
            'password': 'some_really_strong_password'
        }
        User.objects.create_user(**cls.login_data)
        cls.client = Client()


class UserAuthTestCase(SetUpMixin, TestCase):
    """Test that the user can login to access the service
    """

    def test_that_user_can_login(self):
        """Ensures that the user can login to his/her account
        """
        response = self.client.post(
            reverse('app.login'),
            data=self.login_data
        )
        self.assertEqual(response.status_code, 302)

    def test_that_user_can_logout(self):
        """Ensures that user can logout from his/her account
        """
        response = self.client.get(
            reverse('app.logout')
        )
        self.assertEqual(response.status_code, 302)

    def test_that_user_can_signup(self):
        """Ensures that user can signup for a new account
        """
        response = self.client.post(
            reverse('app.signup'),
            data={
                'username': fakerInst.user_name(),
                'first_name': fakerInst.first_name(),
                'last_name': fakerInst.last_name(),
                'email': fakerInst.email(),
                'password': fakerInst.password()
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_that_user_cannot_signup_with_a_registered_username(self):
        """Ensures that user cannot sign up with a registered username
        """
        response = self.client.post(
            reverse('app.signup'),
            {
                'username': 'basil',
                'password': 'do_not_know_what_goes_here'
            },
            follow=True
        )
        self.assertContains(response, 'already taken', status_code=200)


class BucketlistTestCase(SetUpMixin, TestCase):
    """Test that the user can carry out actions on bucketlist
    """
    def test_that_user_can_post_to_bucketlist_route(self):
        """Ensures that user can make new bucketlist
        """
        response = self.client.login(**self.login_data)

        self.assertEqual(response, True)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response, bucketlist_data['name'], status_code=200
        )
        self.client.logout()

    def test_that_user_can_delete_bucketlist(self):
        """Ensures that user can delete bucketlist
        """
        response = self.client.post(
                reverse('app.login'),
                self.login_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
                    reverse('app.bucketlist.delete', kwargs={'pk': 1}),
                    bucketlist_data, follow=True
            )
        self.assertNotContains(response,
                               bucketlist_data['name'],
                               status_code=200)

    def test_that_user_can_update_bucketlist(self):
        """Ensures that user can update bucketlist
        """
        response = self.client.post(
                reverse('app.login'),
                self.login_data
            )
        self.assertEqual(response.status_code, 302)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data
            )
        self.assertEqual(response.status_code, 302)

        bucketlist_data['name'] = 'Before I kick the bucket'
        response = self.client.post(
                reverse('app.bucketlist.update',
                        kwargs={'pk': 1}
                        ),
                bucketlist_data,
                follow=True
            )
        self.assertContains(
            response,
            bucketlist_data['name'],
            status_code=200
        )

    def test_that_user_can_read_bucketlist(self):
        """Ensures that user can read lists of bucketlists
        """
        response = self.client.post(
                 reverse('app.login'),
                 self.login_data,
                 follow=True
            )
        self.assertEqual(response.status_code, 200)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('app.bucketlists'))

        self.assertContains(response,
                            bucketlist_data['name'],
                            status_code=200)

    def test_that_the_user_can_retrieve_paginated_bucketlist(self):
        """Ensures that user can retrieve paginated bucketlist
        """
        response = self.client.post(
                 reverse('app.login'),
                 self.login_data,
                 follow=True
            )
        self.assertEqual(response.status_code, 200)

        for i in xrange(50):
            response = self.client.post(
                reverse('app.bucketlist.create'),
                {'name': fakerInst.name()},
                follow=True
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('app.bucketlists'))

        self.assertContains(response,
                            'Next',
                            status_code=200)


class BucketlistItemTestCase(SetUpMixin, TestCase):
    """Test that user can carry out actions on bucketlist items.
    """
    def test_that_user_can_create_new_bucketlistitem(self):
        """Ensures that user can make new bucketlist item
        """
        response = self.client.login(**self.login_data)

        self.assertEqual(response, True)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )

        self.assertContains(
            response, bucketlist_data['name'], status_code=200
        )

        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('app.bucketlist.item.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                follow=True
            )

        self.assertContains(
                response, bucketlistitem_data['name'], status_code=200
            )
        self.client.logout()

    def test_that_user_can_delete_bucketlistitem(self):
        """Ensures that user can delete bucketlist item
        """
        response = self.client.post(
                reverse('app.login'),
                self.login_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )
        self.assertContains(
            response, bucketlist_data['name'], status_code=200
        )

        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('app.bucketlist.item.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                follow=True
            )

        self.assertContains(
                response, bucketlistitem_data['name'], status_code=200
            )

        response = self.client.post(
                    reverse('app.bucketlist.item.delete',
                            kwargs={'pk': 1, 'pk_item': 1}),
                    bucketlist_data, follow=True
            )
        self.assertNotContains(response,
                               bucketlistitem_data['name'],
                               status_code=200)

    def test_that_user_can_update_bucketlistitem(self):
        """Ensures that user can update bucketlist item
        """
        response = self.client.post(
                reverse('app.login'),
                self.login_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )
        self.assertContains(
            response, bucketlist_data['name'], status_code=200
        )

        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('app.bucketlist.item.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                follow=True
            )

        self.assertContains(
                response, bucketlistitem_data['name'], status_code=200
            )

        bucketlistitem_data['name'] = 'Get a cat'
        response = self.client.post(
                reverse('app.bucketlist.item.update',
                        kwargs={'pk': 1, 'pk_item': 1}
                        ),
                bucketlistitem_data,
                follow=True
            )
        self.assertContains(
            response,
            bucketlistitem_data['name'],
            status_code=200
        )

    def test_that_user_can_mark_task_as_done(self):
        """Ensures that user can mark bucketlist item as done
        """
        response = self.client.post(
                reverse('app.login'),
                self.login_data,
                follow=True
            )
        self.assertEqual(response.status_code, 200)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist.create'),
                bucketlist_data,
                follow=True
            )
        self.assertContains(
            response, bucketlist_data['name'], status_code=200
        )

        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('app.bucketlist.item.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                follow=True
            )

        self.assertContains(
                response, bucketlistitem_data['name'], status_code=200
            )

        response = self.client.get(
                reverse('app.bucketlist.item.finish',
                        kwargs={'pk': 1, 'pk_item': 1}
                        ),
                follow=True
            )

        self.assertContains(
            response,
            'marked as done',
            status_code=200
        )


class UserProfileTestCase(SetUpMixin, TestCase):
    """Test that user can edit his profile.
    """
    def test_that_user_can_edit_profile(self):
        response = self.client.login(**self.login_data)

        self.assertEqual(response, True)

        profile_data = {
                        'bio': 'User is a native of Metro City. \
                                Since 2008, he has been District Executive\
                                for Hispanic Outreach',
                        'age': 24,
                    }
        response = self.client.post(
                reverse('app.user_profile.edit'),
                profile_data,
                follow=True
            )

        self.assertContains(
            response, profile_data['bio'], status_code=200
        )
        self.client.logout()
