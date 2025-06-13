# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_step1, name='register_step1'),
    path('register/username/', views.register_step2, name='register_step2'),
    path('register/password/', views.register_step3, name='register_step3'),
    path('register/additional-info/', views.register_step4, name='register_step4'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]