# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.decorators import classonlymethod


class HomeNewVisitorTest(StaticLiveServerTestCase):
    """This TestSuite tests functionality available to visitors.
    """

    @classonlymethod
    def setUpClass(cls):
        super(StaticLiveServerTestCase, cls).setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.implicitly_wait(3)

    @classonlymethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(StaticLiveServerTestCase, cls).tearDownClass()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        """Test that `Bucketlist Tracker` is present in browser window title.
        """
        self.browser.get(self.get_full_url("app.index"))
        self.assertIn("Bucketlist Tracker", self.browser.title)

    def test_home_files(self):
        """Test that `robots.txt` and `humans.txt` files are available publicly.
        """
        self.browser.get(self.live_server_url + "/robots.txt")
        self.assertNotIn("Not Found", self.browser.title)
        self.browser.get(self.live_server_url + "/humans.txt")
        self.assertNotIn("Not Found", self.browser.title)
