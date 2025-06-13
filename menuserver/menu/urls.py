from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Example: path('', views.menu_list, name='menu_list'),
    path('my-restaurants/', views.my_restaurants, name='my_restaurants'),
    path('create-restaurant/', views.create_restaurant, name='create_restaurant'),
    path('import-restaurant/', views.import_restaurant, name='import_restaurant'),
    path('manage-menu/<int:menu_id>/', views.manage_menu, name='manage_menu'),
    path('manage-menu/<int:menu_id>/delete-item/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('manage-menu/<int:menu_id>/toggle-availability/<int:item_id>/', views.toggle_availability, name='toggle_availability'),
] 