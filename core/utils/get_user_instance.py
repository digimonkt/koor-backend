import jwt
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status

from KOOR.settings import DJANGO_CONFIGURATION
from users.models import User


def get_user_instance(request):
    access_token = request.headers['Authorization'].replace('Bearer ', '')
    decoded = jwt.decode(access_token, DJANGO_CONFIGURATION.SECRET_KEY, algorithms=['HS256'])
    user_id = decoded.get('user_id')
    return get_object_or_404(User, id=user_id)
