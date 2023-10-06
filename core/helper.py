import os

from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv


load_dotenv(os.environ.get('ENV_PATH'))


def send_email(contact_subject, msg_content):

    subject, from_email, to = contact_subject, os.environ.get(
                'MAIL_USERNAME'), os.environ.get('MAIL_RECIPIENTS')

    msg = EmailMultiAlternatives(
                subject, msg_content, from_email, [to]
            )
    msg.attach_alternative(msg_content, "text/html")
    msg.send()