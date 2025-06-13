from django.urls import path
from . import views

app_name = 'menu'

# Admin URLs (prefixed with 'menu/')
admin_urlpatterns = [
    path('my-restaurants/', views.my_restaurants, name='my_restaurants'),
    path('create-restaurant/', views.create_restaurant, name='create_restaurant'),
    path('import-restaurant/', views.import_restaurant, name='import_restaurant'),
    path('manage-menu/<int:menu_id>/', views.manage_menu, name='manage_menu'),
    path('manage-menu/<int:menu_id>/delete-item/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('manage-menu/<int:menu_id>/toggle-availability/<int:item_id>/', views.toggle_availability, name='toggle_availability'),
]

# Public URLs (no prefix)
public_urlpatterns = [
    path('<int:user_id>/<slug:restaurant_name>/', views.public_menu, name='public_menu'),
]

urlpatterns = admin_urlpatterns + public_urlpatterns 