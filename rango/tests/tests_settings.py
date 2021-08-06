from django.test import TestCase
from django.conf import settings


class RangoSettingsTests(TestCase):
    """
    Tests the configuration of the Django project
    """

    def test_databases_variable_exists(self):
        """
        check database settings in settings.py
        """
        self.assertTrue(settings.DATABASES, "no database in settings")

    def test_google_oauth_dependence(self):
        print("RangoSettingsTests")
        """
        Tests to see if the installed apps are present in the project configuration.
        """
        self.assertTrue('allauth' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.account' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.socialaccount' in settings.INSTALLED_APPS)
        self.assertTrue('allauth.socialaccount.providers.google' in settings.INSTALLED_APPS)
        self.assertTrue('google' in settings.SOCIALACCOUNT_PROVIDERS)

    def test_host_settings(self):
        """
        check hosts in host settings
        """
        self.assertTrue('rango.iamwz.online' in settings.ALLOWED_HOSTS)
        self.assertTrue('127.0.0.1' in settings.ALLOWED_HOSTS)
