from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class MenuLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='menu_links')
    restaurant_name = models.CharField(max_length=200, null=True, blank=True)
    website_link = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'
        unique_together = ['user', 'restaurant_name']

    def __str__(self):
        return f"{self.restaurant_name or 'Unnamed Restaurant'} - {self.user.username}"

class MenuItem(models.Model):
    menu = models.ForeignKey(MenuLink, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        unique_together = ['menu', 'name']

    def __str__(self):
        return f"{self.name} - {self.menu.restaurant_name}"

    def save(self, *args, **kwargs):
        # Ensure the photo path includes the restaurant name for better organization
        if self.photo and not self.photo.name.startswith(f'menu_items/{self.menu.restaurant_name}/'):
            self.photo.name = f'menu_items/{self.menu.restaurant_name}/{self.photo.name}'
        super().save(*args, **kwargs)
