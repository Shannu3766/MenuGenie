from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import MenuLink, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ('name', 'price', 'quantity', 'is_available', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True

@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ('restaurant_name', 'user', 'menu_items_count', 'created_at', 'view_menu_items', 'view_public_menu')
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('restaurant_name', 'user__username', 'user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'public_menu_url')
    inlines = [MenuItemInline]
    list_per_page = 20

    fieldsets = (
        ('Restaurant Information', {
            'fields': ('user', 'restaurant_name')
        }),
        ('Menu Information', {
            'fields': ('public_menu_url',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def menu_items_count(self, obj):
        count = obj.menu_items.count()
        return format_html('<span style="color: #666;">{}</span>', count)
    menu_items_count.short_description = 'Menu Items'

    def view_menu_items(self, obj):
        url = reverse('admin:menu_menuitem_changelist') + f'?menu__id__exact={obj.id}'
        return format_html('<a class="button" href="{}">View Items</a>', url)
    view_menu_items.short_description = 'Menu Items'
    view_menu_items.allow_tags = True

    def view_public_menu(self, obj):
        url = f'/{obj.user.id}/{obj.restaurant_name}/'
        return format_html('<a class="button" href="{}" target="_blank">View Public Menu</a>', url)
    view_public_menu.short_description = 'Public Menu'
    view_public_menu.allow_tags = True

    def public_menu_url(self, obj):
        url = f'/{obj.user.id}/{obj.restaurant_name}/'
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)
    public_menu_url.short_description = 'Public Menu URL'

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_link', 'price', 'quantity', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at', 'menu__restaurant_name', 'menu__user')
    search_fields = ('name', 'description', 'menu__restaurant_name', 'menu__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('price', 'quantity', 'is_available')
    list_per_page = 20

    fieldsets = (
        ('Item Information', {
            'fields': ('menu', 'name', 'description', 'price', 'quantity', 'photo')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def menu_link(self, obj):
        url = reverse('admin:menu_menulink_change', args=[obj.menu.id])
        return format_html('<a href="{}">{}</a>', url, obj.menu.restaurant_name)
    menu_link.short_description = 'Restaurant'
    menu_link.allow_tags = True
