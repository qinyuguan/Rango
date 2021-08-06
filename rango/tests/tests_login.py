from django.urls import reverse

from rango import forms
from django.test import TestCase
from django.contrib.auth.models import User
from django.forms import fields as django_fields


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user


class RangoLoginTests(TestCase):
    """
    Tests the configuration of the Django project
    """

    def test_user_form(self):
        """
        Tests the functionality of user form
        """
        self.assertTrue('UserForm' in dir(forms), 'no user form in the directory')

        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, 'form doesn\'t match the model')

        fields = user_form.fields

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(),
                            f"The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification, and try again.")
            self.assertEqual(expected_field, type(fields[expected_field_name]),
                             f"The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}")

    """
    Check if the login url exists 
    """

    def test_login_url_exists(self):
        """
        Checks if the new login view exists
        """
        url = ''

        try:
            url = reverse('rango:login')
        except:
            pass

        self.assertEqual(url, '/rango/login/', "login url missing.")

    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in, and should be redirected to the Rango homepage.
        """
        user_object = create_user_object()

        response = self.client.post(reverse('rango:login'), {'username': 'testuser', 'password': 'testabc123'})
        self.assertEqual(response.status_code, 302)