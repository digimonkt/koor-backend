from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import User


class RegisterTestCase(APITestCase):

    def test_register_with_email(self):
        data = {
            "email": "testcase@example.com",
            "mobile": "",
            "password": "test@password1",
            "profile_role": "",
            "country_code": ""
        }
        response = self.client.post(reverse('users_app_link:user_registration_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_with_mobile(self):
        data = {
            "email": "",
            "mobile": "1234567890",
            "password": "test@password2",
            "profile_role": "",
            "country_code": ""
        }
        response = self.client.post(reverse('users_app_link:user_registration_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='example',
                                             password='NewPassword@123'
                                             )
        self.user = User.objects.create_user(mobile='1234567890',
                                             password='NewMobPassword@123'
                                             )

    def test_login_with_email(self):
        data = {
            "email": "example",
            "password": "NewPassword@123"
        }
        response = self.client.post(reverse('users_app_link:user_login_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_mobile(self):
        data = {
            "mobile": "1234567890",
            "password": "NewMobPassword@123"
        }
        response = self.client.post(reverse('users_app_link:user_login_view_link'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_logout_with_email(self):
    #     print("---------")
    #     print(self.client)
    #     self.token = Token.objects.get(user__email='example')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    #     response = self.client.delete(reverse('users_app_link:user_logout_view_link'))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    # #
    # # def test_logout_with_mobile(self):
    # #     self.token = Token.objects.get(user__mobile='1234567890')
    # #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    # #     response = self.client.delete(reverse('users_app_link:user_logout_view_link'))
    # #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
