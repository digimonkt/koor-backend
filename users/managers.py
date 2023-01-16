from django.contrib.auth.models import BaseUserManager
from typing import Any


# Create Auth User according to Developer Code
class UserManager(BaseUserManager):
    use_in_migrations = True

    # function for create user or superuser
    def _create_user(
            self,
            email: str | None = None,
            mobile: str | None = None,
            password: str | None = None,
            profile_role: str | None = None,
            **extra_fields: dict[str, Any]
    ) -> Any:
        if not (email or mobile):
            raise ValueError('Email or Mobile Number one must be set')
        else:
            if email:
                email = self.normalize_email(email)
                user = self.model(email=email, profile_role=profile_role, **extra_fields)
            elif mobile:
                user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # function for add normal user's other field
    def create_user(
            self,
            display_name: str | None = None,
            email: str | None = None,
            mobile: str | None = None,
            password: str | None = None,
            profile_role: str | None = None,
            **extra_fields: dict[str, Any]
    ) -> Any:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            display_name=display_name,
            email=email,
            mobile=mobile,
            password=password,
            profile_role=profile_role,
            **extra_fields
        )

    # function for add super user's other field
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('profile_role', "admin")
        # display error message if is_staff and is_superuser is false for superuser.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')
        return self._create_user(email=email, password=password, **extra_fields)