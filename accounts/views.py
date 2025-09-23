from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .models import UserProfile, PatientProfile, DoctorProfile
from hospitals.models import Hospital
from bookings.models import Booking
from doctors.models import Doctor
from treatments.models import Treatment
from blogs.models import BlogPost
from feedbacks.models import Feedback

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
                    return redirect('doctor_profile')  # Changed from 'doctor_dashboard'
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
    
    # Get actual appointment counts
    total_appointments = Booking.objects.count()
    today = datetime.now().date()
    today_appointments = Booking.objects.filter(preferred_date=today).count()
    
    # Get recent hospitals
    recent_hospitals = Hospital.objects.all()[:5]  # Get first 5 hospitals
    
    # Get content counts
    total_hospitals = Hospital.objects.count()
    total_treatments = Treatment.objects.count()
    total_blog_posts = BlogPost.objects.count()
    
    # Get actual users for the user management table
    recent_users_for_table = User.objects.select_related('userprofile').order_by('-date_joined')[:5]
    
    context = {
        'user_profile': request.user.userprofile,
        'total_users': total_users,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'recent_users': recent_users,
        'user_distribution': user_distribution,
        'recent_hospitals': recent_hospitals,
        'total_hospitals': total_hospitals,
        'total_treatments': total_treatments,
        'total_blog_posts': total_blog_posts,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'recent_users_for_table': recent_users_for_table,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def doctor_profile(request):
    if request.user.userprofile.user_type != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        doctor_profile = request.user.userprofile.doctor_details
    except DoctorProfile.DoesNotExist:
        doctor_profile = None
    
    # Get the doctor object by matching the user's full name with doctor names
    user_full_name = f"{request.user.first_name} {request.user.last_name}".strip()
    doctor = Doctor.objects.filter(name__icontains=user_full_name).first()
    if not doctor:
        # Fallback to get any doctor if name matching fails
        doctor = Doctor.objects.first()
    
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
        about = request.POST.get('about', '')
        key_points = request.POST.get('key_points', '')
        education = request.POST.get('education', '')
        experience_years = request.POST.get('experience_years', 0)
        medical_license_number = request.POST.get('medical_license_number', '')
        languages_spoken = request.POST.get('languages_spoken', '')
        website = request.POST.get('website', '')
        profile_picture = request.POST.get('profile_picture', '')
        
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
        user_profile.profile_picture = profile_picture
        user_profile.save()
        
        # Update doctor profile
        if doctor_profile:
            doctor_profile.specialization = specialization
            doctor_profile.license_number = license_number
            doctor_profile.years_of_experience = years_of_experience
            doctor_profile.save()
        
        # Update public doctor profile
        if doctor:
            doctor.specialization = specialization
            doctor.about = about
            doctor.key_points = key_points
            doctor.education = education
            doctor.experience_years = experience_years
            doctor.medical_license_number = medical_license_number
            doctor.languages_spoken = languages_spoken
            doctor.phone = phone
            doctor.email = email
            doctor.website = website
            doctor.profile_picture = profile_picture
            doctor.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('doctor_profile')
    
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
    
    context = {
        'user_profile': request.user.userprofile,
        'doctor_profile': doctor_profile,
        'doctor': doctor,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'total_appointments': total_appointments,
        'pending_reviews': pending_reviews,
        'this_month': this_month,
        'patient_satisfaction': patient_satisfaction,
    }
    return render(request, 'accounts/doctor_profile.html', context)


@login_required
def patient_dashboard(request):
    # Redirect to the new patient portal
    return redirect('patient_portal')


@login_required
def patient_portal(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(request, 'User profile not found. Please contact support.')
        return redirect('home')
    
    # Check if user is a patient
    if user_profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('home')
    
    try:
        patient_profile = user_profile.patient_details
    except:
        patient_profile = None
    
    # Get upcoming appointments for this patient
    today = datetime.now().date()
    upcoming_appointments = Booking.objects.filter(
        patient=user_profile,
        preferred_date__gte=today
    ).select_related('preferred_doctor', 'treatment').order_by('preferred_date')
    
    # Get statistics
    total_appointments = Booking.objects.filter(patient=user_profile).count()
    
    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
        'upcoming_appointments': upcoming_appointments,
        'total_appointments': total_appointments,
    }
    return render(request, 'accounts/patient_portal.html', context)


def get_entities(request, entity_type):
    """API endpoint to fetch entities based on type for review selection"""
    try:
        if entity_type == 'doctor':
            entities = Doctor.objects.values('id', 'name')
        elif entity_type == 'hospital':
            entities = Hospital.objects.values('id', 'name')
        elif entity_type == 'treatment':
            entities = Treatment.objects.values('id', 'name')
        else:
            return JsonResponse({'error': 'Invalid entity type'}, status=400)
        
        return JsonResponse(list(entities), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def reviews_page(request):
    """Dedicated page for viewing and submitting reviews"""
    # Get all approved feedback for display with pagination
    feedback_list = Feedback.objects.filter(is_approved=True).select_related(
        'patient', 'doctor', 'hospital', 'treatment'
    ).order_by('-created_at')
    
    # Check if there's a search query
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Filter feedback based on search query (title, comment, entity names)
        feedback_list = feedback_list.filter(
            Q(title__icontains=search_query) |
            Q(comment__icontains=search_query) |
            Q(doctor__name__icontains=search_query) |
            Q(hospital__name__icontains=search_query) |
            Q(treatment__name__icontains=search_query)
        )
    
    context = {
        'feedbacks': feedback_list,
        'search_query': search_query,
    }
    return render(request, 'accounts/reviews.html', context)


def reviews_api(request):
    """API endpoint for fetching reviews data in JSON format"""
    # Get all approved feedback for display
    feedback_list = Feedback.objects.filter(is_approved=True).select_related(
        'patient', 'doctor', 'hospital', 'treatment'
    ).order_by('-created_at')
    
    # Check if there's a search query
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Filter feedback based on search query (title, comment, entity names)
        feedback_list = feedback_list.filter(
            Q(title__icontains=search_query) |
            Q(comment__icontains=search_query) |
            Q(doctor__name__icontains=search_query) |
            Q(hospital__name__icontains=search_query) |
            Q(treatment__name__icontains=search_query)
        )
    
    # Convert to JSON serializable format
    reviews_data = []
    for feedback in feedback_list:
        review_data = {
            'id': feedback.id,
            'title': feedback.title,
            'comment': feedback.comment,
            'rating': feedback.rating,
            'feedback_type': feedback.feedback_type,
            'is_anonymous': feedback.is_anonymous,
            'created_at': feedback.created_at.strftime('%b %d, %Y'),
            'patient_name': 'Anonymous' if feedback.is_anonymous else f"{feedback.patient.user.first_name} {feedback.patient.user.last_name}",
        }
        
        # Add entity information based on feedback type
        if feedback.feedback_type == 'doctor' and feedback.doctor:
            review_data['entity_name'] = f"Dr. {feedback.doctor.name}"
        elif feedback.feedback_type == 'hospital' and feedback.hospital:
            review_data['entity_name'] = feedback.hospital.name
        elif feedback.feedback_type == 'treatment' and feedback.treatment:
            review_data['entity_name'] = feedback.treatment.name
        else:
            review_data['entity_name'] = 'Unknown'
            
        # Add video URL if available
        review_data['video_url'] = feedback.video_url
        
        reviews_data.append(review_data)
    
    return JsonResponse({'reviews': reviews_data})


@require_http_methods(["POST"])
@login_required
def submit_review(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        return JsonResponse({'success': False, 'message': 'User profile not found.'})
    
    # Check if user is a patient or admin (both can submit reviews)
    if user_profile.user_type not in ['patient', 'admin']:
        return JsonResponse({'success': False, 'message': 'Access denied. Only patients and admins can submit reviews.'})
    
    # Get form data
    feedback_type = request.POST.get('reviewType')
    entity_id = request.POST.get('entityId')
    rating = request.POST.get('rating')
    title = request.POST.get('title')
    comment = request.POST.get('comment')
    is_anonymous = request.POST.get('anonymous', False)
    
    # Validate required fields
    if not all([feedback_type, entity_id, rating, title, comment]):
        return JsonResponse({'success': False, 'message': 'All fields are required.'})
    
    # Create feedback object - explicitly set is_approved to True for immediate visibility
    feedback = Feedback(
        patient=user_profile,
        feedback_type=feedback_type,
        rating=rating,
        title=title,
        comment=comment,
        is_anonymous=bool(is_anonymous),
        is_approved=True  # Explicitly set to True so reviews are immediately visible
    )
    
    # Set the appropriate foreign key based on feedback type
    try:
        if feedback_type == 'doctor':
            feedback.doctor = Doctor.objects.get(id=entity_id)
        elif feedback_type == 'hospital':
            feedback.hospital = Hospital.objects.get(id=entity_id)
        elif feedback_type == 'treatment':
            feedback.treatment = Treatment.objects.get(id=entity_id)
    except (Doctor.DoesNotExist, Hospital.DoesNotExist, Treatment.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Invalid entity selected.'})
    
    # Save feedback first to get an ID
    feedback.save()
    
    return JsonResponse({'success': True, 'message': 'Review submitted successfully! Your review is now visible to everyone.'})


@login_required
def patient_profile(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(request, 'User profile not found. Please contact support.')
        return redirect('home')
    
    # Check if user is a patient
    if user_profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('home')
    
    try:
        patient_profile = user_profile.patient_details
    except:
        patient_profile = None
    
    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            # In a real implementation, you would upload this to a storage service
            # For now, we'll just save a placeholder URL
            # In production, you would use Django's file storage system
            user_profile.profile_picture = f"https://ui-avatars.com/api/?name={request.user.first_name}+{request.user.last_name}&background=random"
            user_profile.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('patient_profile')
        
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
        'user_profile': user_profile,
        'patient_profile': patient_profile,
    }
    return render(request, 'accounts/patient_profile.html', context)