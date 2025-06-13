from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Example: path('', views.menu_list, name='menu_list'),
    path('my-restaurants/', views.my_restaurants, name='my_restaurants'),
    path('create-restaurant/', views.create_restaurant, name='create_restaurant'),
    path('import-restaurant/', views.import_restaurant, name='import_restaurant'),
] 