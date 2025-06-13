from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verification_email(user):
    """Send verification email with OTP to user"""
    subject = 'Verify your MenuGenie account'
    html_message = render_to_string('accounts/email/verification_email.html', {
        'user': user,
        'otp': user.email_verification_token,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    ) 