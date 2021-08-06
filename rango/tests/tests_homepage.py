import os
import re
import rango.models
from rango import forms
from datetime import datetime, timedelta
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

class HomePageTests(TestCase):
    """
    Tests the homepage
    """

    """
    Tests to check the homepage
    """
    def test_homepage(self):
        response = self.client.get(reverse('rango:index'))
        home_page_check = '<h3>Rango: Get What You Want</h3>'
        self.assertTrue(home_page_check in response.content.decode())


    def test_homepage_login_button(self):
        """
        Tests to see if the login button appear.
        """
        response = self.client.get(reverse('rango:index'))
        expect = """<div class="popup-item"><a href="/rango/login/">Login</a></div>"""
        self.assertTrue(expect in response.content.decode())