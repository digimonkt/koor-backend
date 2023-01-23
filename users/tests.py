# IMPORT PYTHON PACKAGE.
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class CreateUserTestCase(APITestCase):
    """
    Created a test case for create user module with all possible test requirements.
    """

    def test_register_with_email(self):
        """
        This is first test function here we use email and password without mobile number.
        """
        data = {
            "email": "testcase@example.com",
            "mobile_number": "",
            "password": "test@password1",
            "profile_role": "",
            "country_code": ""
        }
        response = self.client.post(reverse('user_app_link:create_user_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_with_mobile(self):
        """
        This is second test function here we use mobile number and password without email.
        """
        data = {
            "email": "",
            "mobile_number": "1234567890",
            "password": "test@password2",
            "profile_role": "",
            "country_code": ""
        }
        response = self.client.post(reverse('user_app_link:create_user_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateSessionTestCase(APITestCase):
    """
       Created a test case for create session module with all possible test requirements.
    """

    def setUp(self):
        """
           Created a test user with email and mobile number for create session.
        """
        self.user = User.objects.create_user(email='example@email.com',
                                             password='NewPassword@123'
                                             )
        self.user = User.objects.create_user(mobile_number='1234567890',
                                             password='NewMobPassword@123'
                                             )

    def test_login_with_email(self):
        """
            This is first test function here we use email and password as login credential.
        """
        data = {
            "email": "example@email.com",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('users_app_link:create_session_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_mobile(self):
        """
            This is second test function here we use mobile number and password as login credential.
        """
        data = {
            "mobile_number": "1234567890",
            "password": "NewMobPassword@123"
        }
        response = self.client.post(reverse('users_app_link:create_session_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
