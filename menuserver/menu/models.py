from django.db import models
from django.conf import settings

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
