import logging

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import get_template

from conf.models import SMTPSetting


def get_email_object(subject, email_template_name, context, to_email, content_subtype="html", **kwargs):
    """
    Generic Mail Template: If mail send successfully return's True else return None.
    """
    logger = logging.getLogger(__name__)
    try:
        smtp_setting_instance = SMTPSetting.objects.last()
        host = smtp_setting_instance.smtp_host
        host_user = smtp_setting_instance.smtp_user
        host_password = smtp_setting_instance.smtp_password
        host_port = smtp_setting_instance.smtp_port
        mail_obj = EmailBackend(host=host, port=host_port, password=host_password, username=host_user, use_tls=True,
                                timeout=10)

        email_template = get_template(email_template_name).render(context)

        if 'type' in kwargs.keys():
            email_msg = mail.EmailMessage(
                subject=subject,
                body=email_template,
                from_email=host_user,
                to=[to_email]
            )
            email_msg.attach(kwargs['filename'], kwargs['file'].read(), 'application/pdf')
        else:
            email_msg = mail.EmailMessage(
                subject=subject,
                body=email_template,
                from_email=host_user,
                to=[to_email],
            )
        email_msg.content_subtype = content_subtype
        mail_obj.send_messages([email_msg])
        mail_obj.close()
        return True
    except Exception as e:
        logger.exception("Exception occurred", exc_info=True)
        return None
