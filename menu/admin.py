from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import MenuLink, MenuItem, MenuSection, Restaurant, MenuTemplate

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    show_change_link = True

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('restaurant__name',)

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'created_at')
    list_filter = ('menu',)
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'section', 'price', 'is_available')
    list_filter = ('menu', 'section', 'is_available')
    search_fields = ('name', 'description')

@admin.register(MenuTemplate)
class MenuTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_file', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'template_file')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'template_file', 'description', 'thumbnail', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 