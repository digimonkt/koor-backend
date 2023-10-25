import logging

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import get_template

from koor.config.common import Common

from superadmin.models import SMTPSetting


def get_email_object(subject, email_template_name, context, to_email, content_subtype="html", **kwargs):
    """
    Sends an email message using `SMTP settings` from the latest `SMTPSetting object` in the database.

    Args:
        - `subject (str)`: The subject of the email message.
        - `email_template_name (str)`: The name of the email template to be used.
        - `context (dict)`: A dictionary containing variables to be used in the email template.
        - `to_email (list)`: A list of email addresses to send the email to.
        - `content_subtype (str, optional)`: The content subtype of the email message. `Defaults to` `"html"`.
        - `base_url (str, optional)`: The base URL of the website. Defaults to None.
        - `**kwargs`: Additional keyword arguments. Currently only supports a `"filename"` and "`file`" parameter if
            the "`type`" key is in the dictionary.

    Returns:
        - `bool`: True if the email was successfully sent, None otherwise.

    Raises:
        - `Exception`: If an exception occurs during the sending of the email message.

    """

    logger = logging.getLogger(__name__)

    try:
        smtp_setting = SMTPSetting.objects.last()
        host = smtp_setting.smtp_host
        host_user = smtp_setting.smtp_user
        host_password = smtp_setting.smtp_password
        host_port = smtp_setting.smtp_port
        context.update({
            'FOOTER': 'Koor Admin, Thanks',
            'FOOTER_TEXT': 'Unsubscribe from the newsletter',
            'BASE_URL': Common.BASE_URL,
            'LOGO': Common.BASE_URL + smtp_setting.logo.url
        })
        mail_obj = EmailBackend(host=host, port=host_port, password=host_password, username=host_user, use_tls=True,
                                timeout=10)

        email_template = get_template(email_template_name).render(context)

        if 'type' in kwargs.keys():
            email_msg = mail.EmailMessage(
                subject=subject,
                body=email_template,
                from_email=host_user,
                to=to_email
            )
            email_msg.attach(kwargs['filename'], kwargs['file'], 'application/pdf')
        else:
            email_msg = mail.EmailMessage(
                subject=subject,
                body=email_template,
                from_email=host_user,
                to=to_email,
            )
        email_msg.content_subtype = content_subtype
        mail_obj.send_messages([email_msg])
        mail_obj.close()
        return True

    except Exception as e:
        logger.exception("Exception occurred", exc_info=True)
        return None
