# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.utils.decorators import classonlymethod
from django.contrib.auth.models import User


class HomeSigninUserTest(LiveServerTestCase):
    """This TestSuite tests functionality available to visitors.
    """


    @classmethod
    def setUpClass(cls):
        super(HomeSigninUserTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.login_data = {
            'username': 'basil',
            'password': 'some_really_strong_password'
        }

    def setUp(self):
        User.objects.create_user(**self.login_data)
        # sign in user
        self.browser.get('%s%s' % (self.live_server_url, '/'))
        self.browser.find_element_by_id(
            "signInUsername").send_keys(self.login_data['username'])
        self.browser.find_element_by_id(
            "signInPassword").send_keys('some_really_strong_password')
        self.browser.find_element_by_id(
            "signInBtn"
            ).click()
        super(HomeSigninUserTest, self).setUp()
        self.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(HomeSigninUserTest, cls).tearDownClass()

    def _get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)  # pragma: no cover

    def test_dashboard(self):
        """Test that Bucketlist link is present in Dashboard.
        """
        self.assertIn(
            'Dashboard',
            self.browser.find_element_by_tag_name('body').text)

        self.assertIn(
            'Bucketlists',
            self.browser.find_element_by_css_selector('section ul li a').text)

    def test_can_navigate_to_bucketlist_details(self):
        """Test that Bucketlist detail page can be navigated.
        """
        self.browser.find_element_by_css_selector('section ul li a').click()
        self.assertEquals(
            'No bucketlists added yet.',
            self.browser.find_element_by_css_selector('section div p').text)
