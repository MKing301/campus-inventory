from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from django.contrib import messages


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    messages.success(request, "You have successfully logged out!")
