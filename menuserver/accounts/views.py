# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

def register_step1(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
            # Check if email already exists
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return render(request, 'accounts/register_step1.html')
            # Store email in session for next step
            request.session['registration_email'] = email
            return redirect('accounts:register_step2')
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
    return render(request, 'accounts/register_step1.html')

def register_step2(request):
    if 'registration_email' not in request.session:
        return redirect('accounts:register_step1')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        # Check if username is valid
        if not username or len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long.')
            return render(request, 'accounts/register_step2.html', {'email': request.session['registration_email']})
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            return render(request, 'accounts/register_step2.html', {'email': request.session['registration_email']})
        
        # Store username in session for next step
        request.session['registration_username'] = username
        return redirect('accounts:register_step3')
    
    return render(request, 'accounts/register_step2.html', {'email': request.session['registration_email']})

def register_step3(request):
    if 'registration_email' not in request.session or 'registration_username' not in request.session:
        return redirect('accounts:register_step1')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register_step3.html', {
                'email': request.session['registration_email'],
                'username': request.session['registration_username']
            })
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/register_step3.html', {
                'email': request.session['registration_email'],
                'username': request.session['registration_username']
            })
        
        # Store password in session for next step
        request.session['registration_password'] = password1
        return redirect('accounts:register_step4')
    
    return render(request, 'accounts/register_step3.html', {
        'email': request.session['registration_email'],
        'username': request.session['registration_username']
    })

def register_step4(request):
    # Check if all required previous steps are completed
    required_session_keys = ['registration_email', 'registration_username', 'registration_password']
    if not all(key in request.session for key in required_session_keys):
        messages.error(request, 'Please complete all registration steps.')
        return redirect('accounts:register_step1')
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        is_restaurant_owner = request.POST.get('is_restaurant_owner') == 'on'
        
        # Validate phone number if provided
        if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
            messages.error(request, 'Please enter a valid 10-digit phone number.')
            return render(request, 'accounts/register_step4.html', {
                'email': request.session['registration_email'],
                'username': request.session['registration_username'],
                'password1': request.session['registration_password'],
                'password2': request.session['registration_password']
            })
        
        try:
            # Create the user with all information
            user = CustomUser.objects.create_user(
                username=request.session['registration_username'],
                email=request.session['registration_email'],
                password=request.session['registration_password'],
                phone_number=phone_number,
                address=address,
                is_restaurant_owner=is_restaurant_owner
            )
            
            # Clear all registration session data
            for key in required_session_keys:
                del request.session[key]
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Menu Server.')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'An error occurred during registration. Please try again.')
            return render(request, 'accounts/register_step4.html', {
                'email': request.session['registration_email'],
                'username': request.session['registration_username'],
                'password1': request.session['registration_password'],
                'password2': request.session['registration_password']
            })
    
    return render(request, 'accounts/register_step4.html', {
        'email': request.session['registration_email'],
        'username': request.session['registration_username'],
        'password1': request.session['registration_password'],
        'password2': request.session['registration_password']
    })

@cache_control(public=True, max_age=3600)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})