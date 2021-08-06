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


class PermissionTests(TestCase):
    """
    Tests the permission
    """

    """
    Tests to check the if a anonymous user can get into the cart page
    """

    def test_permission_cart(self):
        response = self.client.get(reverse('rango:cart'))
        self.assertTrue(response.status_code == 302)

    def test_permission_admin(self):
        """
            Tests to see if the admin user can access admin pages
        """
        User.objects.create_superuser('testAdmin', '123@email.com', 'adminPassword123')
        self.client.login(username="testAdmin", password='adminPassword123')
        response = self.client.get(reverse('rango:admin_orders'))
        expect = """<div class="keyword"><h3>Manage Orders</h3></div>"""
        self.assertTrue(expect in response.content.decode())

    def test_permission_user(self):
        """
        Tests to see if the common user can access admin pages
        """
        User.objects.create_user('testUser', '123@email.com', 'userPassword123')
        self.client.login(username="testUser", password='userPassword123')
        response = self.client.get(reverse('rango:admin_orders'))
        self.assertTrue(response.status_code == 302)

