from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Restaurant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

class MenuLink(models.Model):
    TEMPLATE_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('minimal', 'Minimal'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant.name}'s Menu" if self.restaurant else "Menu"

class MenuSection(models.Model):
    menu = models.ForeignKey(MenuLink, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['menu', 'name']

    def __str__(self):
        return f"{self.menu.restaurant.name} - {self.name}" if self.menu.restaurant else self.name

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
        return f"{self.menu.restaurant.name} - {self.name}" if self.menu.restaurant else self.name

    def save(self, *args, **kwargs):
        if self.photo and self.menu.restaurant and not self.photo.name.startswith(f'menu_items/{self.menu.restaurant.name}/'):
            self.photo.name = f'menu_items/{self.menu.restaurant.name}/{self.photo.name}'
        super().save(*args, **kwargs)
