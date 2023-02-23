from django.contrib.auth.models import BaseUserManager

# Create Auth User according to Developer Code
class UserManager(BaseUserManager):
    """
    class UserManager is called by the django auth.
    Whenever we create authenticate superuser with email and password, username is not needed for superuser.
    - We create authenticate user with `email` or `mobile` and `password`. 
    - `username` is not required.
    """
    use_in_migrations = True

    # function for create user or superuser
    def _create_user(
            self,
            email=None,
            mobile_number=None,
            password=None,
            role=None,
            **extra_fields
    ):
        if not (email or mobile_number):
            raise ValueError('Email or Mobile Number one must be set')
        else:
            if email:
                email = self.normalize_email(email)
                user = self.model(email__iexact=email, role=role, **extra_fields)
            elif mobile_number:
                user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # function for add normal user's other field
    def create_user(
        self,
        name=None,
        email=None,
        mobile_number=None,
        password=None,
        role=None,
        **extra_fields
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            name=name,
            mobile_number=mobile_number,
            password=password,
            role=role,
            **extra_fields
        )

    # function for add superusers other field
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', "admin")
        # display error message if is_staff and is_superuser is false for superuser.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')
        return self._create_user(email=email, password=password, **extra_fields)
