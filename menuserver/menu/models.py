from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class MenuLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    restaurant_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant_name} - {self.name}"

class MenuSection(models.Model):
    menu = models.ForeignKey(MenuLink, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['menu', 'name']

    def __str__(self):
        return f"{self.menu.restaurant_name} - {self.name}"

class MenuItem(models.Model):
    menu = models.ForeignKey(MenuLink, on_delete=models.CASCADE, related_name='items')
    section = models.ForeignKey(MenuSection, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section__name', 'name']

    def __str__(self):
        return f"{self.menu.restaurant_name} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure the photo path includes the restaurant name for better organization
        if self.photo and not self.photo.name.startswith(f'menu_items/{self.menu.restaurant_name}/'):
            self.photo.name = f'menu_items/{self.menu.restaurant_name}/{self.photo.name}'
        super().save(*args, **kwargs)
