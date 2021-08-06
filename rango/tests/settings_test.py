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

class Chapter10ConfigurationTests(TestCase):
    """
    Tests the configuration of the Django project
    """

    def test_google_oauth_dependence(self):
        """
        Tests to see if the SessionMiddleware is present in the project configuration.
        """
        # SOCIALACCOUNT_PROVIDERS
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)

    def test_session_app_present(self):
        """
        Tests to see if the sessions app is present.
        """
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)