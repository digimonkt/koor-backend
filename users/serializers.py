from django.contrib.auth import authenticate

from rest_framework import exceptions, status
from rest_framework import serializers

from .models import User


class CreateUserSerializers(serializers.ModelSerializer):
    """
    CreateUserSerializer class provides serialization for creating a User model.

    The class extends the ModelSerializer from the rest_framework.serializers module. The Meta class
    specifies the model to use (User) and the fields to include in serialization.

    The validate_mobile_number method performs a custom validation on the mobile_number field. It ensures that the
    mobile_number is not blank and contains only numbers. In case of an error, it raises a ValidationError with a
    detailed error message.

    """

    class Meta:
        model = User
        fields = ['email', 'mobile_number', 'password', 'role', 'country_code']

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                try:
                    if User.objects.get(mobile_number=mobile_number):
                        raise serializers.ValidationError('mobile_number already in use.', code='mobile_number')
                except User.DoesNotExist:
                    return mobile_number
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    def validate_email(self, email):
        if email != '':
            try:
                if User.objects.get(email=email):
                    raise serializers.ValidationError('email already in use.', code='email')
            except User.DoesNotExist:
                return email
        else:
            raise serializers.ValidationError('email can not be blank', code='email')
