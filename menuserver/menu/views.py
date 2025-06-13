from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import MenuLink, MenuItem
from .forms import MenuItemForm

# Create your views here.

@login_required
def my_restaurants(request):
    if not request.user.is_restaurant_owner:
        messages.error(request, 'You must be a restaurant owner to access this page.')
        return redirect('home')
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

@login_required
def manage_menu(request, menu_id):
    menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
    menu_items = MenuItem.objects.filter(menu=menu_link).order_by('-created_at')
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.menu = menu_link
            menu_item.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('menu:manage_menu', menu_id=menu_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MenuItemForm()
    
    context = {
        'menu_link': menu_link,
        'menu_items': menu_items,
        'form': form
    }
    return render(request, 'menu/manage_menu.html', context)

@login_required
def delete_menu_item(request, menu_id, item_id):
    if request.method == 'POST':
        menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
        menu_item = get_object_or_404(MenuItem, id=item_id, menu=menu_link)
        menu_item.delete()
        messages.success(request, 'Menu item deleted successfully!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def toggle_availability(request, menu_id, item_id):
    if request.method == 'POST':
        menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
        menu_item = get_object_or_404(MenuItem, id=item_id, menu=menu_link)
        menu_item.is_available = not menu_item.is_available
        menu_item.save()
        status = 'available' if menu_item.is_available else 'unavailable'
        messages.success(request, f'Menu item is now {status}!')
        return JsonResponse({
            'status': 'success',
            'is_available': menu_item.is_available
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_menu_item(request, menu_id, item_id):
    menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
    menu_item = get_object_or_404(MenuItem, id=item_id, menu=menu_link)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menu:manage_menu', menu_id=menu_id)
    else:
        form = MenuItemForm(instance=menu_item)
    
    return render(request, 'menu/edit_menu_item.html', {
        'form': form,
        'menu_link': menu_link,
        'menu_item': menu_item
    })

def public_menu(request, user_id, restaurant_name):
    menu_link = get_object_or_404(MenuLink, user_id=user_id, restaurant_name=restaurant_name)
    menu_items = MenuItem.objects.filter(menu=menu_link, is_available=True).order_by('name')
    
    context = {
        'menu_link': menu_link,
        'menu_items': menu_items,
    }
    return render(request, 'menu/public_menu.html', context)
