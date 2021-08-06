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


class RangoSettingsTests(TestCase):
    """
    Tests the configuration of the Django project
    """

    def test_google_oauth_dependence(self):
        print("RangoSettingsTests")
        """
        Tests to see if the SessionMiddleware is present in the project configuration.
        """
        self.assertTrue('allauth' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.account' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.socialaccount' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.socialaccount.providers.google' in settings.INSTALLED_APPS)
        self.assertTrue('google' in settings.SOCIALACCOUNT_PROVIDERS)


    def test_host_settings(self):
        """
        Tests to see if the sessions app is present.
        """
        self.assertTrue('rango.iamwz.online' in settings.ALLOWED_HOSTS)
        self.assertTrue('127.0.0.1' in settings.ALLOWED_HOSTS)



