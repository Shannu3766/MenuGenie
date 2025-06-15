from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class MenuLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.user.username}"

    @property
    def sections(self):
        return self.menusection_set.all()

    @property
    def items(self):
        return self.menuitem_set.all()

class MenuSection(models.Model):
    menu = models.ForeignKey(MenuLink, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.menu.restaurant.name}"

class MenuItem(models.Model):
    menu = models.ForeignKey(MenuLink, on_delete=models.CASCADE)
    section = models.ForeignKey(MenuSection, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.menu.restaurant.name}"

    def save(self, *args, **kwargs):
        if self.photo and self.menu.restaurant and not self.photo.name.startswith(f'menu_items/{self.menu.restaurant.name}/'):
            self.photo.name = f'menu_items/{self.menu.restaurant.name}/{self.photo.name}'
        super().save(*args, **kwargs)
