# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client


class UserAuthTestCase(TestCase):
    """Test that the user can login to access our service
    """

    def setUp(self):
        User.objects.create(username="basil", password="12345")
        self.client = Client()

    def test_that_user_can_login(self):
        """tests that the user can login to his account
        """
        response = self.client.post(
            reverse('app.login'),
            {'username': 'basil',
             'password': '12345'}
        )
        self.assertEqual(response.status_code, 200)

    def test_that_user_can_logout(self):
        """tests that user can logout from his account
        """
        response = self.client.get(
            reverse('app.logout')
        )
        self.assertEqual(response.status_code, 200)
