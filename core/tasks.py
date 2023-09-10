import os

from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task()
def send_registration_email_task(first_name, last_name, username, email):
    """Sends an email when the registration form has been submitted."""
    subject, from_email, to = (
        'New User Registered for core App',
        os.environ.get('MAIL_USERNAME'),
        os.environ.get('MAIL_RECIPIENTS')
    )
    text_content = f'''
    New User ...

    First Name: {first_name}\n
    Last Name: {last_name}\n
    Username: {username}\n
    Email: {email}\n
    '''
    html_content = f'''
    <p>Greetings!</p>
    <p>The following user registered:</p>
    <ul>
    <li><strong>First Name:</strong> {first_name}</li>
    <li><strong>Last Name:</strong> {last_name}</li>
    <li><strong>Username:</strong> {username}</li>
    <li><strong>Email:</strong> {email}</li>
    </ul>
    '''
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
