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
from bookings.models import Booking
from doctors.models import Doctor


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
        # Get the doctor object by matching the user's full name with doctor names
        user_full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        doctor = Doctor.objects.filter(name__icontains=user_full_name).first()
        if not doctor:
            # Fallback to get any doctor if name matching fails
            doctor = Doctor.objects.first()
        
        # Get today's appointments for this doctor
        today = datetime.now().date()
        todays_appointments = Booking.objects.filter(
            preferred_doctor=doctor,
            preferred_date=today
        ).select_related('patient', 'treatment')
        
        # Get upcoming appointments
        upcoming_appointments = Booking.objects.filter(
            preferred_doctor=doctor,
            preferred_date__gte=today
        ).select_related('patient', 'treatment').order_by('preferred_date')[:5]
        
        # Get statistics
        total_appointments = Booking.objects.filter(preferred_doctor=doctor).count()
        pending_reviews = 3  # Placeholder
        this_month = Booking.objects.filter(
            preferred_doctor=doctor,
            preferred_date__month=today.month
        ).count()
        patient_satisfaction = 4.8  # Placeholder
        
    except Exception as e:
        # Handle case where doctor profile doesn't exist or other errors
        doctor_profile = None
        todays_appointments = []
        upcoming_appointments = []
        total_appointments = 0
        pending_reviews = 0
        this_month = 0
        patient_satisfaction = 0
    
    context = {
        'user_profile': request.user.userprofile,
        'doctor_profile': doctor_profile,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'total_appointments': total_appointments,
        'pending_reviews': pending_reviews,
        'this_month': this_month,
        'patient_satisfaction': patient_satisfaction,
    }
    return render(request, 'accounts/doctor_dashboard.html', context)


@login_required
def doctor_profile(request):
    if request.user.userprofile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        doctor_profile = request.user.userprofile.doctor_details
    except DoctorProfile.DoesNotExist:
        doctor_profile = None
    
    if request.method == 'POST':
        # Handle profile update
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        specialization = request.POST.get('specialization', '')
        license_number = request.POST.get('license_number', '')
        years_of_experience = request.POST.get('years_of_experience', 0)
        
        # Update user info
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        
        # Update user profile
        user_profile = request.user.userprofile
        user_profile.phone = phone
        user_profile.address = address
        user_profile.city = city

        user_profile.save()
        
        # Update doctor profile
        if doctor_profile:
            doctor_profile.specialization = specialization
            doctor_profile.license_number = license_number
            doctor_profile.years_of_experience = years_of_experience
            doctor_profile.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('doctor_profile')
    
    context = {
        'user_profile': request.user.userprofile,
        'doctor_profile': doctor_profile,
    }
    return render(request, 'accounts/doctor_profile.html', context)


@login_required
def patient_dashboard(request):
    if request.user.userprofile.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        patient_profile = request.user.userprofile.patient_details
        
        # Get upcoming appointments for this patient
        today = datetime.now().date()
        upcoming_appointments = Booking.objects.filter(
            patient=request.user.userprofile,
            preferred_date__gte=today
        ).select_related('preferred_doctor', 'treatment').order_by('preferred_date')
        
        # Get recent medical records (placeholder for now)
        recent_records = [
            {'title': 'Blood Test Report', 'doctor': 'Dr. John Smith', 'date': 'Oct 10, 2025', 'status': 'Normal'},
            {'title': 'MRI Scan', 'doctor': 'Dr. Emily Johnson', 'date': 'Oct 5, 2025', 'status': 'Review'},
        ]
        
        # Get statistics
        total_appointments = Booking.objects.filter(patient=request.user.userprofile).count()
        medical_records = 12  # Placeholder
        prescriptions = 3  # Placeholder
        health_score = "85%"  # Placeholder
        
    except PatientProfile.DoesNotExist:
        patient_profile = None
        upcoming_appointments = []
        recent_records = []
        total_appointments = 0
        medical_records = 0
        prescriptions = 0
        health_score = "0%"
    
    context = {
        'user_profile': request.user.userprofile,
        'patient_profile': patient_profile,
        'upcoming_appointments': upcoming_appointments,
        'recent_records': recent_records,
        'total_appointments': total_appointments,
        'medical_records': medical_records,
        'prescriptions': prescriptions,
        'health_score': health_score,
    }
    return render(request, 'accounts/patient_dashboard.html', context)


@login_required
def patient_profile(request):
    if request.user.userprofile.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        patient_profile = request.user.userprofile.patient_details
    except PatientProfile.DoesNotExist:
        patient_profile = None
    
    if request.method == 'POST':
        # Handle profile update
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')

        blood_type = request.POST.get('blood_type', '')
        emergency_contact = request.POST.get('emergency_contact', '')
        medical_history = request.POST.get('medical_history', '')
        
        # Update user info
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        
        # Update user profile
        user_profile = request.user.userprofile
        user_profile.phone = phone
        user_profile.address = address
        user_profile.city = city

        user_profile.save()
        
        # Update patient profile
        if patient_profile:
            patient_profile.blood_type = blood_type
            patient_profile.emergency_contact = emergency_contact
            patient_profile.medical_history = medical_history
            patient_profile.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('patient_profile')
    
    context = {
        'user_profile': request.user.userprofile,
        'patient_profile': patient_profile,
    }
    return render(request, 'accounts/patient_profile.html', context)