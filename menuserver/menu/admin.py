from django.contrib import admin
from .models import MenuLink

@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'website_link', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'website_link')
    ordering = ('-created_at',)
