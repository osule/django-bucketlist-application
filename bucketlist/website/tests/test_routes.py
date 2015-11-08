# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from faker import Faker


fakerInst = Faker()


class SetUpMixin(object):
    """Mixes the setUp for TestCases
    """
    def setUp(self):
        User.objects.create(username="basil", password="12345")
        self.login_data = {
            'username': 'basil',
            'password': '12345'
        }
        self.client = Client()


class UserAuthTestCase(SetUpMixin, TestCase):
    """Test that the user can login to access the service
    """

    def test_that_user_can_login(self):
        """tests that the user can login to his/her account
        """
        response = self.client.post(
            reverse('app.login'),
            data=self.login_data
        )
        self.assertEqual(response.status_code, 302)

    def test_that_user_can_logout(self):
        """tests that user can logout from his/her account
        """
        response = self.client.get(
            reverse('app.logout')
        )
        self.assertEqual(response.status_code, 302)

    def test_that_user_can_signup(self):
        """tests that user can signup for a new account
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


class BucketlistTestCase(SetUpMixin, TestCase):
    """Test that the user can login and make a bucketlist
    """
    def test_that_user_can_post_to_bucketlist_route(self):
        response = self.client.post(
                reverse('app.login'),
                data=self.login_data
            )
        self.assertEqual(response.status_code, 302)

        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('app.bucketlist'),
                data=bucketlist_data
            )
        self.assertEqual(response.status_code == 302)
        self.assertIn(bucketlist_data['name'], response.body)
