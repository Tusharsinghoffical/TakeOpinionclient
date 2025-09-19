from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime, timedelta
from .models import UserProfile, PatientProfile, DoctorProfile
from hospitals.models import Hospital


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user type
            try:
                user_profile = user.userprofile
                if user_profile.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif user_profile.user_type == 'doctor':
                    return redirect('doctor_dashboard')
                elif user_profile.user_type == 'patient':
                    return redirect('patient_dashboard')
            except UserProfile.DoesNotExist:
                # If no profile, redirect to home
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_type = request.POST['user_type']
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/signup.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create user profile
        user_profile = UserProfile.objects.create(
            user=user,
            user_type=user_type
        )
        
        # Create specific profile based on user type
        if user_type == 'patient':
            PatientProfile.objects.create(user_profile=user_profile)
        elif user_type == 'doctor':
            DoctorProfile.objects.create(user_profile=user_profile)
        
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    
    return render(request, 'accounts/signup.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def admin_dashboard(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Get statistics for the dashboard
    total_users = User.objects.count()
    total_doctors = UserProfile.objects.filter(user_type='doctor').count()
    total_patients = UserProfile.objects.filter(user_type='patient').count()
    
    # Get recent users (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_users = User.objects.filter(date_joined__gte=week_ago).count()
    
    # Get user distribution
    user_distribution = UserProfile.objects.values('user_type').annotate(count=Count('user_type'))
    
    # Get recent activity (simplified for now)
    recent_activity = [
        {'user': 'Dr. John Smith', 'action': 'Updated profile', 'time': '2 minutes ago'},
        {'user': 'Patient Jane Doe', 'action': 'Booked appointment', 'time': '15 minutes ago'},
        {'user': 'Dr. Robert Johnson', 'action': 'Added treatment notes', 'time': '1 hour ago'},
        {'user': 'Patient Mike Wilson', 'action': 'Uploaded medical records', 'time': '2 hours ago'},
        {'user': 'Admin Sarah', 'action': 'Added new hospital', 'time': '3 hours ago'},
    ]
    
    # Get system status (simplified for now)
    system_status = {
        'database': 'Online',
        'web_server': 'Online',
        'storage': '78%',
        'last_backup': '2 hours ago'
    }
    
    # Get recent hospitals
    recent_hospitals = Hospital.objects.all()[:5]  # Get first 5 hospitals
    
    context = {
        'user_profile': request.user.userprofile,
        'total_users': total_users,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'recent_users': recent_users,
        'user_distribution': user_distribution,
        'recent_activity': recent_activity,
        'system_status': system_status,
        'recent_hospitals': recent_hospitals,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    if request.user.userprofile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        doctor_profile = request.user.userprofile.doctor_details
    except DoctorProfile.DoesNotExist:
        doctor_profile = None
    
    context = {
        'user_profile': request.user.userprofile,
        'doctor_profile': doctor_profile,
    }
    return render(request, 'accounts/doctor_dashboard.html', context)


@login_required
def patient_dashboard(request):
    if request.user.userprofile.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        patient_profile = request.user.userprofile.patient_details
    except PatientProfile.DoesNotExist:
        patient_profile = None
    
    context = {
        'user_profile': request.user.userprofile,
        'patient_profile': patient_profile,
    }
    return render(request, 'accounts/patient_dashboard.html', context)