from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_verification_email(user_or_registration):
    """Send verification email with OTP to user or registration data"""
    try:
        subject = 'Verify your MenuGenie account'
        
        # Get email and token based on the type of object
        if hasattr(user_or_registration, 'email_verification_token'):
            # It's a CustomUser
            email = user_or_registration.email
            otp = user_or_registration.email_verification_token
        else:
            # It's a RegistrationData
            email = user_or_registration.email
            otp = user_or_registration.email_verification_token
        
        # Render the email template
        html_message = render_to_string('accounts/email/verification_email.html', {
            'user': user_or_registration,
            'otp': otp,
        })
        plain_message = strip_tags(html_message)
        
        # Create EmailMessage instance
        email_message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        
        # Set content type to HTML
        email_message.content_subtype = "html"
        
        # Add headers for better deliverability
        email_message.extra_headers = {
            'X-Entity-Ref-ID': str(getattr(user_or_registration, 'id', '')),
            'X-Entity-Type': 'verification',
        }
        
        # Log the attempt to send email
        logger.info(f"Attempting to send verification email to {email}")
        
        # Send the email
        email_message.send(fail_silently=False)
        
        # Log successful email send
        logger.info(f"Successfully sent verification email to {email}")
        
    except Exception as e:
        # Log the error
        logger.error(f"Failed to send verification email to {email}: {str(e)}")
        raise  # Re-raise the exception to be handled by the view 