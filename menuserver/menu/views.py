from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import MenuLink, MenuItem, MenuSection, Restaurant
from .forms import MenuItemForm, MenuSectionForm, MenuUploadForm
from .utils import extract_menu_data
import os
from django.conf import settings
import json
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

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
        restaurant_tagline = request.POST.get('restaurant_tagline')
        restaurant_image = request.FILES.get('restaurant_image')
        
        if not restaurant_name:
            messages.error(request, 'Restaurant name is required.')
            return render(request, 'menu/create_restaurant.html', {
                'restaurant_name': restaurant_name,
                'restaurant_tagline': restaurant_tagline
            })
        
        # Check if restaurant name already exists
        if Restaurant.objects.filter(name=restaurant_name).exists():
            messages.error(request, 'A restaurant with this name already exists.')
            return render(request, 'menu/create_restaurant.html', {
                'restaurant_name': restaurant_name,
                'restaurant_tagline': restaurant_tagline
            })
        
        # Create restaurant
        restaurant = Restaurant.objects.create(
            name=restaurant_name,
            tagline=restaurant_tagline,
            image=restaurant_image
        )
        
        # Create menu link
        menu_link = MenuLink.objects.create(
            user=request.user,
            restaurant=restaurant
        )
        
        return redirect('menu:select_template', menu_id=menu_link.id)
    
    return render(request, 'menu/create_restaurant.html')

@login_required
def import_restaurant(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        if restaurant_name:
            try:
                # Create restaurant first
                restaurant = Restaurant.objects.create(
                    user=request.user,
                    name=restaurant_name
                )
                
                # Create menu link
                MenuLink.objects.create(
                    user=request.user,
                    restaurant=restaurant
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
    
    # Get all sections for this menu
    sections = MenuSection.objects.filter(menu=menu_link).order_by('name')
    
    # Get all menu items
    menu_items = MenuItem.objects.filter(menu=menu_link).order_by('section__name', 'name')
    
    # Get unsectioned items
    unsectioned_items = menu_items.filter(section__isnull=True)
    
    # Handle menu upload
    if request.method == 'POST' and 'menu_image' in request.FILES:
        upload_form = MenuUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            menu_image = request.FILES['menu_image']
            print(f"Processing uploaded image: {menu_image.name}")
            
            # Save the uploaded image temporarily
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', menu_image.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            print(f"Saving image to: {temp_path}")
            
            with open(temp_path, 'wb+') as destination:
                for chunk in menu_image.chunks():
                    destination.write(chunk)
            
            print("Image saved successfully, extracting menu data...")
            # Extract menu data
            menu_data = extract_menu_data(temp_path)
            
            if menu_data:
                print(f"Successfully extracted menu data: {json.dumps(menu_data, indent=2)}")
                try:
                    # Process each section and its items
                    for section_data in menu_data:
                        print(f"Processing section: {section_data['section']}")
                        # Create or get section
                        section, created = MenuSection.objects.get_or_create(
                            menu=menu_link,
                            name=section_data['section']
                        )
                        print(f"Section {'created' if created else 'already exists'}")
                        
                        # Create items for this section
                        for item_data in section_data['items']:
                            print(f"Processing item: {item_data['item']}")
                            # Extract price (remove currency symbols and convert to float)
                            price_str = item_data['price'].replace('₹', '').replace('$', '').strip()
                            try:
                                price = float(price_str)
                                print(f"Parsed price: {price}")
                            except ValueError:
                                print(f"Could not parse price: {item_data['price']}")
                                price = 0.0
                            
                            # Create menu item
                            MenuItem.objects.create(
                                menu=menu_link,
                                section=section,
                                name=item_data['item'],
                                price=price,
                                quantity=1,  # Set default quantity to 1
                                is_available=True
                            )
                            print(f"Created menu item: {item_data['item']}")
                    
                    messages.success(request, 'Menu items extracted and added successfully!')
                except Exception as e:
                    print(f"Error processing menu data: {str(e)}")
                    messages.error(request, f'Error processing menu data: {str(e)}')
            else:
                print("Failed to extract menu data from image")
                messages.error(request, 'Failed to extract menu data from the image.')
            
            # Clean up temporary file
            try:
                os.remove(temp_path)
                print("Temporary file cleaned up")
            except Exception as e:
                print(f"Error cleaning up temporary file: {str(e)}")
            
            return redirect('menu:manage_menu', menu_id=menu_id)
    else:
        upload_form = MenuUploadForm()
    
    # Handle regular menu item form
    if request.method == 'POST' and 'name' in request.POST:
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.menu = menu_link
            menu_item.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Menu item added successfully!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Error adding menu item.',
                'errors': form.errors.as_json()
            }, status=400)
    else:
        form = MenuItemForm()
    
    # Add section form
    section_form = MenuSectionForm()
    
    return render(request, 'menu/manage_menu.html', {
        'menu_link': menu_link,
        'form': form,
        'section_form': section_form,
        'upload_form': upload_form,
        'sections': sections,
        'menu_items': menu_items,
        'unsectioned_items': unsectioned_items,
    })

@login_required
def add_section(request, menu_id):
    menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
    
    if request.method == 'POST':
        form = MenuSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.menu = menu_link
            # Capitalize the section name
            section.name = section.name.upper()
            section.save()
            messages.success(request, 'Section added successfully!')
        else:
            messages.error(request, 'Error adding section. Please try again.')
    
    return redirect('menu:manage_menu', menu_id=menu_id)

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
            updated_item = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Menu item updated successfully!',
                'item': {
                    'id': updated_item.id,
                    'name': updated_item.name,
                    'description': updated_item.description,
                    'price': str(updated_item.price), # Convert Decimal to string for JSON
                    'quantity': updated_item.quantity,
                    'is_available': updated_item.is_available,
                    'photo_url': updated_item.photo.url if updated_item.photo else None,
                    'section_id': updated_item.section.id if updated_item.section else None,
                }
            })
        else:
            # Return form errors as JSON
            return JsonResponse({
                'status': 'error',
                'message': 'Error updating menu item.',
                'errors': form.errors.as_json()
            }, status=400)
    else:
        # This part will no longer be directly used for rendering the modal content,
        # but it's good to keep it consistent if it's still used elsewhere.
        form = MenuItemForm(instance=menu_item)
    
    return render(request, 'menu/edit_menu_item.html', {
        'form': form,
        'menu_link': menu_link,
        'menu_item': menu_item
    })

def public_menu(request, user_id, restaurant_name):
    """Public view of a restaurant's menu"""
    # Convert the restaurant name from slug to title case for comparison
    restaurant_name_title = restaurant_name.replace('-', ' ').title()
    
    # Try to find the restaurant with case-insensitive name comparison
    menu_link = get_object_or_404(
        MenuLink,
        user_id=user_id,
        restaurant__name__iexact=restaurant_name_title
    )
    
    # Get all sections ordered by name
    sections = menu_link.sections.all().order_by('name')
    
    # Get all items that belong to sections
    sectioned_items = menu_link.items.filter(section__isnull=False).order_by('section__name', 'name')
    
    # Get all items that don't belong to any section
    unsectioned_items = menu_link.items.filter(section__isnull=True).order_by('name')
    
    context = {
        'menu_link': menu_link,
        'sections': sections,
        'sectioned_items': sectioned_items,
        'unsectioned_items': unsectioned_items,
    }
    
    return render(request, f'menu/templates/public_menu_{menu_link.template}.html', context)

@login_required
def delete_section(request, menu_id, section_id):
    if request.method == 'POST':
        menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
        section = get_object_or_404(MenuSection, id=section_id, menu=menu_link)
        
        # Get all items in this section
        items = MenuItem.objects.filter(section=section)
        
        # Delete all items in the section
        items.delete()
        
        # Delete the section
        section.delete()
        
        messages.success(request, 'Section and all its items deleted successfully!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def toggle_section_availability(request, menu_id, section_id):
    if request.method == 'POST':
        menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
        section = get_object_or_404(MenuSection, id=section_id, menu=menu_link)
        action = request.POST.get('action', 'available')
        
        # Update all items in the section
        MenuItem.objects.filter(menu=menu_link, section=section).update(
            is_available=(action == 'available')
        )
        
        status = 'available' if action == 'available' else 'unavailable'
        messages.success(request, f'All items in section "{section.name}" are now {status}!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_restaurant(request, menu_id):
    menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the restaurant image if it exists
        if menu_link.restaurant and menu_link.restaurant.image:
            # Delete the image file from storage
            if os.path.isfile(menu_link.restaurant.image.path):
                os.remove(menu_link.restaurant.image.path)
        
        # Delete the menu link and related objects
        menu_link.delete()
        messages.success(request, 'Restaurant deleted successfully.')
        return redirect('menu:my_restaurants')
    
    return render(request, 'menu/delete_restaurant.html', {'menu_link': menu_link})

@login_required
def edit_restaurant(request, menu_id):
    menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
    
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_tagline = request.POST.get('restaurant_tagline')
        restaurant_image = request.FILES.get('restaurant_image')
        
        if not restaurant_name:
            messages.error(request, 'Restaurant name is required.')
            return render(request, 'menu/edit_restaurant.html', {'menu_link': menu_link})
        
        # Check if restaurant name already exists (excluding current restaurant)
        if Restaurant.objects.filter(name=restaurant_name).exclude(id=menu_link.restaurant.id).exists():
            messages.error(request, 'A restaurant with this name already exists.')
            return render(request, 'menu/edit_restaurant.html', {'menu_link': menu_link})
        
        # Update restaurant
        menu_link.restaurant.name = restaurant_name
        menu_link.restaurant.tagline = restaurant_tagline
        if restaurant_image:
            menu_link.restaurant.image = restaurant_image
        menu_link.restaurant.save()
        
        messages.success(request, 'Restaurant updated successfully!')
        return redirect('menu:my_restaurants')
    
    return render(request, 'menu/edit_restaurant.html', {'menu_link': menu_link})

@login_required
def change_template(request, menu_id):
    menu_link = get_object_or_404(MenuLink, id=menu_id, user=request.user)
    
    if request.method == 'POST':
        template = request.POST.get('template')
        if template in dict(MenuLink.TEMPLATE_CHOICES):
            menu_link.template = template
            menu_link.save()
            messages.success(request, 'Menu template updated successfully!')
        else:
            messages.error(request, 'Invalid template selected.')
    
    return redirect('menu:my_restaurants')
