from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import MenuLink, MenuItem, MenuSection, Restaurant

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    show_change_link = True

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user', 'template', 'created_at')
    list_filter = ('user', 'template', 'created_at')
    search_fields = ('restaurant__name', 'user__username')
    inlines = [MenuItemInline]

@admin.register(MenuSection)
class MenuSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'created_at')
    list_filter = ('menu__restaurant', 'created_at')
    search_fields = ('name', 'menu__restaurant__name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'section', 'menu', 'is_available')
    list_filter = ('is_available', 'section', 'menu__restaurant')
    search_fields = ('name', 'menu__restaurant__name') 