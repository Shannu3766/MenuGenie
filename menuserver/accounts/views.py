# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import CustomUser, RegistrationData
from django.http import JsonResponse
from .utils import send_verification_email
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

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
        
        try:
            # Delete any existing registration data for this email
            RegistrationData.objects.filter(email=request.session['registration_email']).delete()
            
            # Create new registration data
            registration = RegistrationData.objects.create(
                email=request.session['registration_email'],
                username=request.session['registration_username'],
                password=make_password(request.session['registration_password']),
                phone_number=phone_number,
                address=address,
                is_restaurant_owner=is_restaurant_owner
            )
            
            # Generate and set verification token
            registration.set_verification_token()
            
            # Send verification email
            try:
                send_verification_email(registration)
            except Exception as email_error:
                print(f"Email sending error: {str(email_error)}")
                registration.delete()  # Clean up if email fails
                messages.error(request, f'Failed to send verification email: {str(email_error)}')
                return render(request, 'accounts/register_step4.html', {
                    'email': request.session['registration_email'],
                    'username': request.session['registration_username'],
                    'password1': request.session['registration_password'],
                    'password2': request.session['registration_password']
                })
            
            # Clear all registration session data
            for key in required_session_keys:
                del request.session[key]
            
            messages.success(request, 'Registration initiated! Please check your email to verify your account.')
            return redirect('accounts:verify_email_pending', registration_id=registration.id)
            
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Add this line for debugging
            messages.error(request, f'An error occurred during registration: {str(e)}')
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

def verify_email_pending(request, registration_id):
    try:
        registration = RegistrationData.objects.get(id=registration_id)
    except RegistrationData.DoesNotExist:
        messages.error(request, 'Invalid registration data.')
        return redirect('accounts:register_step1')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if not otp:
            messages.error(request, 'Please enter the verification code.')
            return render(request, 'accounts/verify_email_pending.html', {'registration': registration})
        
        if registration.is_token_expired():
            messages.error(request, 'Verification code has expired. Please register again.')
            registration.delete()
            return redirect('accounts:register_step1')
        
        if otp == registration.email_verification_token:
            # Create the user
            user = CustomUser.objects.create_user(
                username=registration.username,
                email=registration.email,
                password=registration.password,
                phone_number=registration.phone_number,
                address=registration.address,
                is_restaurant_owner=registration.is_restaurant_owner,
                email_verified=True  # Email is already verified
            )
            
            # Delete the registration data
            registration.delete()
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Email verified successfully! You can now use your account.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid verification code.')
    
    return render(request, 'accounts/verify_email_pending.html', {'registration': registration})

@login_required
def resend_verification(request):
    if request.method == 'POST':
        verification_type = request.GET.get('type')
        registration_id = request.GET.get('id')
        
        try:
            if verification_type == 'email' and registration_id:
                registration = RegistrationData.objects.get(id=registration_id)
                registration.set_verification_token()
                send_verification_email(registration)
                return JsonResponse({'success': True})
        except RegistrationData.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid registration data.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })

def check_username(request):
    if request.method == 'GET':
        username = request.GET.get('username', '')
        exists = CustomUser.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def check_email(request):
    if request.method == 'GET':
        email = request.GET.get('email', '')
        exists = CustomUser.objects.filter(email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)