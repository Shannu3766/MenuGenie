from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import MenuLink

# Create your views here.

@login_required
def my_restaurants(request):
    menu_links = MenuLink.objects.filter(user=request.user)
    return render(request, 'menu/my_restaurants.html', {
        'menu_links': menu_links
    })

@login_required
def create_restaurant(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        if restaurant_name:
            try:
                MenuLink.objects.create(
                    user=request.user,
                    restaurant_name=restaurant_name
                )
                messages.success(request, 'Restaurant created successfully!')
                return redirect('menu:my_restaurants')
            except IntegrityError:
                messages.error(request, f'A restaurant named "{restaurant_name}" already exists. Please choose a different name.')
                return render(request, 'menu/create_restaurant.html', {'restaurant_name': restaurant_name})
    return render(request, 'menu/create_restaurant.html')

@login_required
def import_restaurant(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        if restaurant_name:
            try:
                MenuLink.objects.create(
                    user=request.user,
                    restaurant_name=restaurant_name
                )
                messages.success(request, 'Restaurant imported successfully!')
                return redirect('menu:my_restaurants')
            except IntegrityError:
                messages.error(request, f'A restaurant named "{restaurant_name}" already exists. Please choose a different name.')
                return render(request, 'menu/import_restaurant.html', {'restaurant_name': restaurant_name})
    return render(request, 'menu/import_restaurant.html')
