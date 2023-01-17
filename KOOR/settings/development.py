from .local import Local, config


class Development(Local):
    """
    Devserver settings for KOOR project.

    You can modify and add variables for as per your needs.
    Check the detail documentation for the variable @ https://docs.djangoproject.com/en/4.1/ref/settings
    """

    ALLOWED_HOSTS = ["*", ]

    # A list of all the people who get code error notifications.
    # Django emails these people the details of exceptions raised in the request/response cycle.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-ADMINS

    ADMINS = [
        ('Organization', config('ORGANIZATION')),
        ('DevOps', config('DEVOPS')),
        ('TeamLeader', config('QA')),
        ('Developer', config('DEVELOPER')),
    ]

    # A list in the same format as ADMINS that specifies who should get broken link notifications.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-MANAGERS

    MANAGERS = [
        ('Developer', config('DEVELOPER')),
    ]

    # Server Email
    # The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#server-email

    SERVER_EMAIL = config("SERVER_EMAIL")
