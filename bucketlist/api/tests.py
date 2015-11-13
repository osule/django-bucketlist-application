from django.test import TestCase

# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from faker import Faker
from website.models import Bucketlist, BucketlistItem
import json

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
        cls.client = APIClient()


class UserAuthTestCase(SetUpMixin, APITestCase):
    """Test that the user can login to access the service
    """

    def test_that_user_can_login(self):
        """Ensures that the user can login to his/her account
        ENDPOINT: POST `/api/auth/login/`
        """
        response = self.client.post('/api/auth/login/',
            data=self.login_data
        )
        self.assertContains(response, 'token', status_code=200)


class BucketlistTestCase(SetUpMixin, APITestCase):
    """Test that the user can carry out actions on bucketlist
    """

    def test_that_user_can_create_bucketlist(self):
        """Ensures that user can make new bucketlist
        ENDPOINT: POST `/api/bucketlists/`
        """
        response = self.client.post('/api/auth/login/',
            data=self.login_data
        )
    
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
 
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_that_user_can_delete_bucketlist(self):
        """Ensures that user can delete bucketlist
        ENDPOINT: DELETE `/api/bucketlists/:id/`
        """
        response = self.client.post('/api/auth/login/',
            data=self.login_data
        )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
                    reverse('api.bucketlist', kwargs={'pk': bucketlist.id}),
                    {},
                    format='json',
                    follow=True
                )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
         
    def test_that_user_can_update_bucketlist(self):
        """Ensures that user can update bucketlist
        ENDPOINT: PUT `/api/bucketlists/:id/`
        """
        response = self.client.post('/api/auth/login/',
            data=self.login_data
        )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        bucketlist = Bucketlist.objects.get()
        bucketlist_data['name'] = 'Before I kick the bucket'
        response = self.client.put(
                reverse('api.bucketlist',
                kwargs={'pk':bucketlist.id}
            ),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_that_user_can_read_bucketlist(self):
        """Ensures that user can read lists of bucketlists
        ENDPOINT: GET `/api/bucketlists/:id/`
        """
        response = self.client.post('/api/auth/login/',
            data=self.login_data
        )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        bucketlist = Bucketlist.objects.get()
        
        response = self.client.get(
                    reverse('api.bucketlist',
                    kwargs={'pk':bucketlist.id}
                ),
                    format='json')
         
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
class BucketlistItemTestCase(SetUpMixin, APITestCase):
    """Test that user can carry out actions on bucketlist items.
    """

    def test_that_user_can_create_new_bucketlistitem(self):
        """Ensures that user can make new bucketlist item
        ENDPOINT: POST `/api/bucketlists/:id/items/`
        """
        response = self.client.post('/api/auth/login/',
            data=self.login_data
        )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('api.bucketlist.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                format='json'
            )
        
        self.assertEqual(
                response.status_code, status.HTTP_201_CREATED
            )
 
    def test_that_user_can_delete_bucketlistitem(self):
        """Ensures that user can delete bucketlist item
        ENDPOINT: DELETE `/api/bucketlists/:id/items/:item_id/`
        """
        response = self.client.post(
                '/api/auth/login/',
                data=self.login_data
            )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('api.bucketlist.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                format='json'
            )
        
        self.assertEqual(
                response.status_code, status.HTTP_201_CREATED
            )
         
        response = self.client.delete(
                    reverse('api.bucketlist.item',
                            kwargs={'pk': 1, 'pk_item': 1}),
                    format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
         
    def test_that_user_can_update_bucketlistitem(self):
        """Ensures that user can update bucketlist item
        ENDPOINT: PUT `/api/bucketlists/:id/items/:item_id/`
        """
        response = self.client.post(
                '/api/auth/login/',
                data=self.login_data
            )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
        bucketlistitem_data = {'name': 'Get a dog', 'done': True}
        response = self.client.post(
                reverse('api.bucketlist.create', kwargs={'pk': 1}),
                bucketlistitem_data,
                format='json'
            )
        
        self.assertEqual(
                response.status_code, status.HTTP_201_CREATED
            )
         
        bucketlistitem_data['name'] = 'Get a cat'
        response = self.client.put(
                reverse('api.bucketlist.item',
                kwargs={'pk':1, 'pk_item': 1}
            ),
                bucketlistitem_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BucketlistSearchTestCase(SetUpMixin, APITestCase):
    """Test search functionality for bucketlist
    """
    def test_that_user_can_search_bucketlist(self):
        """Ensures that user can update bucketlist item
        ENDPOINT: GET `/api/bucketlists?q=:query`
        """
        response = self.client.post(
                '/api/auth/login/',
                data=self.login_data
            )
        
        self.assertContains(response, 'token', status_code=200)
        token = json.loads(response.content)
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT {0}'.format(token.get('token'))
        )
         
        bucketlist_data = {'name': 'Before I get married'}
        response = self.client.post(
                reverse('api.bucketlists'),
                bucketlist_data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
         
        response = self.client.get(
                '{0}?q=Before'.format(reverse('api.bucketlists')),
                format='json'
            )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
