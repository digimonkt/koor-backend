from .local import Local

class Development(Local):
    """
    Devserver settings for KOOR project.

    You can modify and add variables for as per your needs.
    Check the detail documentation for the variable @ https://docs.djangoproject.com/en/4.1/ref/settings
    """

    ALLOWED_HOSTS = ["*",]


    # A list of all the people who get code error notifications.
    # Django emails these people the details of exceptions raised in the request/response cycle.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-ADMINS

    ADMINS = [
        ('Developer', 'keval.rajpal@digimonk.in'),
        ('QA', 'saral.shrivastava@digimonk.in'),
        ('DevOps', 'vishnu.gahlot@digimonk.in'),
    ]


    # A list in the same format as ADMINS that specifies who should get broken link notifications.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-MANAGERS

    MANAGERS = [
        ('Developer', 'keval.rajpal@digimonk.in'),
    ]


    # Server Email
    # The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
    # https://docs.djangoproject.com/en/4.1/ref/settings/#server-email

    SERVER_EMAIL = "support.koor@digimonk.co"