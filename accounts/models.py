from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import json

# Create your models here.

class RegistrationData(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_restaurant_owner = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=6)
    email_verification_token_created_at = models.DateTimeField(auto_now_add=True)
    
    def is_token_expired(self):
        """Check if verification token is expired (10 minutes)"""
        return (timezone.now() - self.email_verification_token_created_at).total_seconds() > 600

    def generate_verification_token(self):
        """Generate a 6-digit verification token"""
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def set_verification_token(self):
        """Set verification token and timestamp"""
        self.email_verification_token = self.generate_verification_token()
        self.email_verification_token_created_at = timezone.now()
        self.save()

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_restaurant_owner = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=6, null=True, blank=True)
    email_verification_token_created_at = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    
    def set_verification_token(self):
        """Generate and set a new verification token"""
        self.email_verification_token = ''.join(random.choices('0123456789', k=6))
        self.email_verification_token_created_at = timezone.now()
        self.save()
    
    def is_verification_token_expired(self):
        """Check if the verification token has expired (10 minutes)"""
        if not self.email_verification_token_created_at:
            return True
        return timezone.now() - self.email_verification_token_created_at > timezone.timedelta(minutes=10)