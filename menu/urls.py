from django.urls import path
from . import views

app_name = 'menu'

# Admin URLs (prefixed with 'menu/')
admin_urlpatterns = [
    path('my-restaurants/', views.my_restaurants, name='my_restaurants'),
    path('create-restaurant/', views.create_restaurant, name='create_restaurant'),
    path('import-restaurant/', views.import_restaurant, name='import_restaurant'),
    path('manage-menu/<int:menu_id>/', views.manage_menu, name='manage_menu'),
    path('manage-menu/<int:menu_id>/add-section/', views.add_section, name='add_section'),
    path('manage-menu/<int:menu_id>/delete-section/<int:section_id>/', views.delete_section, name='delete_section'),
    path('manage-menu/<int:menu_id>/delete-item/<int:item_id>/', views.delete_menu_item, name='delete_item'),
    path('manage-menu/<int:menu_id>/toggle-availability/<int:item_id>/', views.toggle_availability, name='toggle_availability'),
    path('manage-menu/<int:menu_id>/toggle-section-availability/<int:section_id>/', views.toggle_section_availability, name='toggle_section_availability'),
    path('manage-menu/<int:menu_id>/edit-item/<int:item_id>/', views.edit_menu_item, name='edit_item'),
    path('menu/<int:menu_id>/delete/', views.delete_restaurant, name='delete_restaurant'),
    path('menu/<int:menu_id>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('menu/<int:menu_id>/change-template/', views.change_template, name='change_template'),
    path('template/<int:template_id>/preview/', views.template_preview, name='template_preview'),
]

# Public URLs (no prefix)
public_urlpatterns = [
    path('<int:user_id>/<slug:restaurant_name>/', views.public_menu, name='public_menu'),
]

urlpatterns = admin_urlpatterns + public_urlpatterns 