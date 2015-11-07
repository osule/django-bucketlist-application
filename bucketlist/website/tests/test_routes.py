# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from faker import Faker


fakerInst = Faker()


class UserAuthTestCase(TestCase):
    """Test that the user can login to access the service
    """

    def setUp(self):
        User.objects.create(username="basil", password="12345")
        self.client = Client()

    def test_that_user_can_login(self):
        """tests that the user can login to his/her account
        """
        response = self.client.post(
            reverse('app.login'),
            data={
                'username': 'basil',
                'password': '12345'
                }
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
