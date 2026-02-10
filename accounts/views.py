from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, PatientProfile, DoctorProfile
from hospitals.models import Hospital
from bookings.models import Booking
from doctors.models import Doctor
from treatments.models import Treatment, TreatmentCategory
from blogs.models import BlogPost
from feedbacks.models import Feedback
from core.models import State


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate input
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'accounts/login.html')

        if not password:
            messages.error(request, 'Password is required.')
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user is active
            if not user.is_active:
                messages.error(
                    request, 'Your account has been deactivated. Please contact support.')
                return render(request, 'accounts/login.html')

            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # Redirect based on user type
            try:
                user_profile = user.userprofile
                if user_profile.user_type == 'admin':
                    return redirect('accounts:admin_dashboard')
                elif user_profile.user_type == 'doctor':
                    return redirect('accounts:doctor_profile')
                elif user_profile.user_type == 'patient':
                    return redirect('accounts:patient_dashboard')
                else:
                    # Default redirect for unknown user types
                    return redirect('home')
            except AttributeError as e:
                # This means the user object doesn't have a userprofile attribute
                # Create a default profile for users without one
                try:
                    user_profile = UserProfile.objects.create(
                        user=user,
                        user_type='patient'  # Default to patient
                    )
                    # Also create the specific profile
                    PatientProfile.objects.create(user_profile=user_profile)
                    messages.info(
                        request, 'User profile created successfully.')
                    # Redirect to patient dashboard as default
                    return redirect('accounts:patient_dashboard')
                except Exception as profile_error:
                    messages.warning(
                        request, f'Unable to create user profile: {str(profile_error)}. Please contact support.')
                    return redirect('home')
            except Exception as e:
                messages.error(
                    request, f'An error occurred during login. Please try again. Error details: {str(e)}')
                return redirect('home')
        else:
            messages.error(
                request, 'Invalid username or password. Please try again.')

    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        user_type = request.POST.get('user_type', '')

        # Validation
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'accounts/signup.html')

        if len(username) < 3:
            messages.error(
                request, 'Username must be at least 3 characters long.')
            return render(request, 'accounts/signup.html')

        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'accounts/signup.html')

        if not user_type:
            messages.error(request, 'Please select an account type.')
            return render(request, 'accounts/signup.html')

        if user_type not in ['patient', 'doctor']:
            messages.error(request, 'Invalid account type selected.')
            return render(request, 'accounts/signup.html')

        if not password:
            messages.error(request, 'Password is required.')
            return render(request, 'accounts/signup.html')

        if len(password) < 6:
            messages.error(
                request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')

        # Check if username already exists
        if User.objects.filter(username__iexact=username).exists():
            messages.error(
                request, 'Username already exists. Please choose a different username.')
            return render(request, 'accounts/signup.html')

        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request, 'Email already exists. Please use a different email address.')
            return render(request, 'accounts/signup.html')

        # Validate email format
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'accounts/signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=username, email=email, password=password)

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

            messages.success(
                request, f'Account created successfully for {username}!')
            return redirect('home')
        except Exception as e:
            # If any error occurs, try to delete the user if created
            try:
                if 'user' in locals():
                    user.delete()
            except:
                pass  # If user deletion fails, just continue
            messages.error(
                request, f'An error occurred during registration. Please try again. Error: {str(e)}')
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')


# Removed logout functionality
# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have been logged out.')
#     return redirect('home')

@login_required
def admin_dashboard(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Get statistics for the dashboard
    total_users = User._default_manager.count()
    total_doctors = UserProfile._default_manager.filter(
        user_type='doctor').count()
    total_patients = UserProfile._default_manager.filter(
        user_type='patient').count()

    # Get recent users (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_users = User._default_manager.filter(
        date_joined__gte=week_ago).count()

    # Get user distribution
    user_distribution = UserProfile._default_manager.values(
        'user_type').annotate(count=Count('user_type'))

    # Get actual appointment counts
    total_appointments = Booking._default_manager.count()
    today = timezone.now().date()
    today_appointments = Booking._default_manager.filter(
        preferred_date=today).count()

    # Get booking statistics by status
    pending_appointments = Booking._default_manager.filter(
        status='pending').count()
    confirmed_appointments = Booking._default_manager.filter(
        status='confirmed').count()
    cancelled_appointments = Booking._default_manager.filter(
        status='cancelled').count()

    # Get recent bookings
    recent_bookings = Booking._default_manager.select_related(
        'patient__user', 'treatment', 'preferred_doctor'
    ).order_by('-created_at')[:5]

    # Get recent entities
    recent_doctors = Doctor._default_manager.all()[:5]  # Get first 5 doctors
    recent_hospitals = Hospital._default_manager.all()[
        :5]  # Get first 5 hospitals
    recent_treatments = Treatment._default_manager.all()[
        :5]  # Get first 5 treatments

    # Get content counts
    total_hospitals = Hospital._default_manager.count()
    total_treatments = Treatment._default_manager.count()
    total_blog_posts = BlogPost._default_manager.count()

    # Get actual users for the user management table
    recent_users_for_table = User._default_manager.select_related(
        'userprofile').order_by('-date_joined')[:5]

    context = {
        'user_profile': request.user.userprofile,
        'total_users': total_users,
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'recent_users': recent_users,
        'user_distribution': user_distribution,
        'recent_doctors': recent_doctors,
        'recent_hospitals': recent_hospitals,
        'recent_treatments': recent_treatments,
        'total_hospitals': total_hospitals,
        'total_treatments': total_treatments,
        'total_blog_posts': total_blog_posts,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'recent_users_for_table': recent_users_for_table,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'cancelled_appointments': cancelled_appointments,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


# Add a new view for the advanced booking dashboard
@login_required
def admin_booking_dashboard(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')

    # Get all bookings with related information
    bookings = Booking._default_manager.select_related(
        'patient__user', 'treatment', 'preferred_doctor', 'preferred_hospital'
    ).order_by('-created_at')

    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    # Calculate statistics
    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    cancelled_bookings = bookings.filter(status='cancelled').count()
    in_progress_bookings = bookings.filter(status='in_progress').count()
    completed_bookings = bookings.filter(status='completed').count()

    # Calculate today's bookings
    today = timezone.now().date()
    today_bookings = bookings.filter(created_at__date=today).count()

    # Get recent bookings (last 5)
    recent_bookings = bookings[:5]

    # Get top treatments
    top_treatments = bookings.filter(treatment__isnull=False).values(
        'treatment__name').annotate(count=Count('treatment')).order_by('-count')[:5]

    # Calculate booking trends (last 7 days)
    week_ago = today - timedelta(days=7)
    weekly_bookings = bookings.filter(created_at__date__gte=week_ago).extra(
        {'date': 'date(created_at)'}).values('date').annotate(count=Count('id')).order_by('date')

    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'in_progress_bookings': in_progress_bookings,
        'completed_bookings': completed_bookings,
        'today_bookings': today_bookings,
        'recent_bookings': recent_bookings,
        'top_treatments': top_treatments,
        'weekly_bookings': weekly_bookings,
    }

    return render(request, 'bookings/admin_dashboard.html', context)


# Add API endpoint for updating booking status
@csrf_exempt
@login_required
def admin_update_booking_status(request, booking_id, status):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            booking = Booking._default_manager.get(id=booking_id)

            # Validate status
            valid_statuses = ['pending', 'confirmed',
                              'cancelled', 'in_progress', 'completed']
            if status not in valid_statuses:
                return JsonResponse({'success': False, 'message': 'Invalid status.'})

            # Update status
            booking.status = status
            booking.save()

            return JsonResponse({
                'success': True,
                'message': f'Booking {status} successfully.'
            })
        except Booking.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Booking not found.'})
        except Exception:
            return JsonResponse({'success': False, 'message': 'Booking not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


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
    today = timezone.now().date()
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
    total_appointments = Booking.objects.filter(
        preferred_doctor=doctor).count()
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
    return redirect('accounts:patient_portal')


@login_required
def patient_portal(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(
            request, 'User profile not found. Please contact support.')
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
    today = timezone.now().date()
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

    # Add pagination - show 10 reviews per page
    from django.core.paginator import Paginator
    paginator = Paginator(feedback_list, 10)  # Show 10 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate real-time statistics (based on all reviews, not just current page)
    total_reviews = feedback_list.count()

    # Calculate average rating
    if total_reviews > 0:
        # Calculate weighted average rating
        rating_sum = feedback_list.aggregate(
            total_rating=Sum('rating')
        )['total_rating'] or 0
        average_rating = round(rating_sum / total_reviews, 1)

        # Calculate percentage of 4+ star reviews (would recommend)
        high_rating_count = feedback_list.filter(rating__gte=4).count()
        recommend_percentage = round((high_rating_count / total_reviews) * 100)
    else:
        average_rating = 0
        recommend_percentage = 0

    context = {
        'feedbacks': page_obj,  # Pass the paginated object instead of the full list
        'search_query': search_query,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'recommend_percentage': recommend_percentage,
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

    # Add pagination - show 10 reviews per page
    from django.core.paginator import Paginator
    paginator = Paginator(feedback_list, 10)  # Show 10 reviews per page
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except:
        page_obj = paginator.page(1)

    # Calculate real-time statistics (based on all reviews, not just current page)
    total_reviews = feedback_list.count()

    # Calculate average rating
    if total_reviews > 0:
        # Calculate weighted average rating
        rating_sum = feedback_list.aggregate(
            total_rating=Sum('rating')
        )['total_rating'] or 0
        average_rating = round(rating_sum / total_reviews, 1)

        # Calculate percentage of 4+ star reviews (would recommend)
        high_rating_count = feedback_list.filter(rating__gte=4).count()
        recommend_percentage = round((high_rating_count / total_reviews) * 100)
    else:
        average_rating = 0
        recommend_percentage = 0

    # Convert to JSON serializable format (only for current page)
    reviews_data = []
    for feedback in page_obj:
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

    # Return both reviews and statistics
    return JsonResponse({
        'reviews': reviews_data,
        'statistics': {
            'total_reviews': total_reviews,
            'average_rating': average_rating,
            'recommend_percentage': recommend_percentage,
        },
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        }
    })


@require_http_methods(["POST"])
@login_required
def submit_review(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except Exception as e:
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

    # Validate rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return JsonResponse({'success': False, 'message': 'Rating must be between 1 and 5.'})
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Invalid rating value.'})

    # Validate entity_id
    try:
        entity_id = int(entity_id)
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'message': 'Invalid entity selected.'})

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

    # Handle video upload if present
    if 'video' in request.FILES:
        video_file = request.FILES['video']
        # Generate a unique filename to avoid conflicts
        import uuid
        import os
        filename = f"{uuid.uuid4().hex}_{video_file.name}"

        # Save the video file to the media directory
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.conf import settings

        # Save the file
        path = default_storage.save(os.path.join(
            'videos', filename), ContentFile(video_file.read()))
        feedback.video_url = settings.MEDIA_URL + path

    # Set the appropriate foreign key based on feedback type
    try:
        if feedback_type == 'doctor':
            feedback.doctor = Doctor.objects.get(id=entity_id)
        elif feedback_type == 'hospital':
            feedback.hospital = Hospital.objects.get(id=entity_id)
        elif feedback_type == 'treatment':
            feedback.treatment = Treatment.objects.get(id=entity_id)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid review type.'})
    except (Doctor.DoesNotExist, Hospital.DoesNotExist, Treatment.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Invalid entity selected.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error linking entity: {str(e)}'})

    # Save feedback
    try:
        feedback.save()
        return JsonResponse({'success': True, 'message': 'Review submitted successfully! Your review is now visible to everyone.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error saving review: {str(e)}'})


@login_required
def patient_profile(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(
            request, 'User profile not found. Please contact support.')
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
        # Check if this is a profile picture upload
        if request.POST.get('action') == 'upload_picture' and 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            # Save the file to media directory
            user_profile.profile_picture = profile_picture
            user_profile.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('accounts:patient_profile')

        # Handle profile update (personal and medical info)
        # Personal info
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')

        # Medical info
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
        return redirect('accounts:patient_profile')

    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
    }
    return render(request, 'accounts/patient_profile.html', context)


@login_required
def patient_medical_history_doctors(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(
            request, 'User profile not found. Please contact support.')
        return redirect('home')

    # Check if user is a patient
    if user_profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('home')

    # Get patient profile
    try:
        patient_profile = user_profile.patient_details
    except:
        patient_profile = None

    # Get doctor visit history (this would typically come from bookings or appointments)
    # For now, we'll simulate this data
    doctor_visits = [
        {
            'doctor_name': 'Dr. John Smith',
            'specialization': 'Cardiologist',
            'visit_date': '2023-05-15',
            'diagnosis': 'Routine checkup',
            'treatment': 'Blood pressure medication',
            'notes': 'Patient blood pressure is stable.'
        },
        {
            'doctor_name': 'Dr. Emily Johnson',
            'specialization': 'Dermatologist',
            'visit_date': '2023-03-22',
            'diagnosis': 'Skin rash',
            'treatment': 'Topical cream prescription',
            'notes': 'Follow-up in 2 weeks if not improved.'
        }
    ]

    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
        'doctor_visits': doctor_visits,
    }
    return render(request, 'accounts/patient_medical_history_doctors.html', context)


@login_required
def patient_medical_history_hospitals(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(
            request, 'User profile not found. Please contact support.')
        return redirect('home')

    # Check if user is a patient
    if user_profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('home')

    # Get patient profile
    try:
        patient_profile = user_profile.patient_details
    except:
        patient_profile = None

    # Get hospital visit history (this would typically come from bookings or appointments)
    # For now, we'll simulate this data
    hospital_visits = [
        {
            'hospital_name': 'City General Hospital',
            'visit_date': '2023-05-15',
            'department': 'Cardiology',
            'reason': 'Routine checkup',
            'doctor': 'Dr. John Smith',
            'notes': 'Annual heart health assessment.'
        },
        {
            'hospital_name': 'Metropolitan Medical Center',
            'visit_date': '2023-03-22',
            'department': 'Dermatology',
            'reason': 'Skin consultation',
            'doctor': 'Dr. Emily Johnson',
            'notes': 'Prescribed topical treatment for rash.'
        }
    ]

    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
        'hospital_visits': hospital_visits,
    }
    return render(request, 'accounts/patient_medical_history_hospitals.html', context)


@login_required
def patient_medical_history_treatments(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(
            request, 'User profile not found. Please contact support.')
        return redirect('home')

    # Check if user is a patient
    if user_profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('home')

    # Get patient profile
    try:
        patient_profile = user_profile.patient_details
    except:
        patient_profile = None

    # Get treatment history (this would typically come from bookings or appointments)
    # For now, we'll simulate this data
    treatment_history = [
        {
            'treatment_name': 'Blood Pressure Management',
            'start_date': '2023-05-15',
            'end_date': 'Ongoing',
            'doctor': 'Dr. John Smith',
            'hospital': 'City General Hospital',
            'status': 'Active',
            'notes': 'Monthly checkups scheduled.'
        },
        {
            'treatment_name': 'Skin Rash Treatment',
            'start_date': '2023-03-22',
            'end_date': '2023-04-05',
            'doctor': 'Dr. Emily Johnson',
            'hospital': 'Metropolitan Medical Center',
            'status': 'Completed',
            'notes': 'Treatment successful, rash cleared.'
        }
    ]

    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
        'treatment_history': treatment_history,
    }
    return render(request, 'accounts/patient_medical_history_treatments.html', context)


@login_required
def patient_medical_history_reports(request):
    # Check if user has a profile at all
    try:
        user_profile = request.user.userprofile
    except:
        messages.error(
            request, 'User profile not found. Please contact support.')
        return redirect('home')

    # Check if user is a patient
    if user_profile.user_type != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('home')

    # Get patient profile
    try:
        patient_profile = user_profile.patient_details
    except:
        patient_profile = None

    # Get medical reports (this would typically come from a reports model)
    # For now, we'll simulate this data
    medical_reports = [
        {
            'report_type': 'Blood Test',
            'date': '2023-05-15',
            'doctor': 'Dr. John Smith',
            'hospital': 'City General Hospital',
            'summary': 'Cholesterol levels within normal range.',
            'file_url': '#'
        },
        {
            'report_type': 'MRI Scan',
            'date': '2023-03-22',
            'doctor': 'Dr. Emily Johnson',
            'hospital': 'Metropolitan Medical Center',
            'summary': 'No abnormalities detected in skin tissue.',
            'file_url': '#'
        }
    ]

    context = {
        'user_profile': user_profile,
        'patient_profile': patient_profile,
        'medical_reports': medical_reports,
    }
    return render(request, 'accounts/patient_medical_history_reports.html', context)


@csrf_exempt
@login_required
def admin_doctors_api(request):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    try:
        doctors = Doctor.objects.all().values(
            'id', 'name', 'specialization', 'experience_years',
            'rating', 'review_count', 'email', 'profile_picture'
        )
        return JsonResponse({
            'success': True,
            'doctors': list(doctors)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@login_required
def admin_add_doctor(request):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            specialization = request.POST.get('specialization', '')
            email = request.POST.get('email', '')
            experience_years = request.POST.get('experience_years', 0)

            if not name:
                return JsonResponse({'success': False, 'message': 'Doctor name is required.'})

            doctor = Doctor.objects.create(
                name=name,
                specialization=specialization,
                email=email,
                experience_years=experience_years,
                rating=0.0,
                review_count=0
            )

            return JsonResponse({
                'success': True,
                'message': 'Doctor added successfully.',
                'doctor_id': doctor.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_edit_doctor(request, doctor_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.name = request.POST.get('name', doctor.name)
            doctor.specialization = request.POST.get(
                'specialization', doctor.specialization)
            doctor.email = request.POST.get('email', doctor.email)
            doctor.experience_years = request.POST.get(
                'experience_years', doctor.experience_years)
            doctor.save()

            return JsonResponse({
                'success': True,
                'message': 'Doctor updated successfully.'
            })
        except Doctor.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Doctor not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_delete_doctor(request, doctor_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            doctor.delete()
            return JsonResponse({
                'success': True,
                'message': 'Doctor deleted successfully.'
            })
        except Doctor.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Doctor not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_hospitals_api(request):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    try:
        hospitals = Hospital.objects.all().values(
            'id', 'name', 'city', 'state__name',
            'established_year', 'rating', 'profile_picture'
        )
        return JsonResponse({
            'success': True,
            'hospitals': list(hospitals)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@login_required
def admin_add_hospital(request):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            city = request.POST.get('city', '')
            state_name = request.POST.get('state', '')
            established_year = request.POST.get('established_year', None)

            if not name:
                return JsonResponse({'success': False, 'message': 'Hospital name is required.'})

            # Try to get or create state
            state = None
            if state_name:
                state, created = State.objects.get_or_create(name=state_name)

            hospital = Hospital.objects.create(
                name=name,
                city=city,
                state=state,
                established_year=established_year,
                rating=0.0
            )

            return JsonResponse({
                'success': True,
                'message': 'Hospital added successfully.',
                'hospital_id': hospital.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_edit_hospital(request, hospital_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            hospital = Hospital.objects.get(id=hospital_id)
            hospital.name = request.POST.get('name', hospital.name)
            hospital.city = request.POST.get('city', hospital.city)

            state_name = request.POST.get('state', '')
            if state_name:
                state, created = State.objects.get_or_create(name=state_name)
                hospital.state = state

            established_year = request.POST.get(
                'established_year', hospital.established_year)
            if established_year:
                hospital.established_year = established_year

            hospital.save()

            return JsonResponse({
                'success': True,
                'message': 'Hospital updated successfully.'
            })
        except Hospital.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Hospital not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_delete_hospital(request, hospital_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            hospital = Hospital.objects.get(id=hospital_id)
            hospital.delete()
            return JsonResponse({
                'success': True,
                'message': 'Hospital deleted successfully.'
            })
        except Hospital.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Hospital not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_treatments_api(request):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    try:
        treatments = Treatment.objects.select_related('category').all().values(
            'id', 'name', 'category__name', 'starting_price'
        )
        return JsonResponse({
            'success': True,
            'treatments': list(treatments)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@login_required
def admin_add_treatment(request):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            name = request.POST.get('name', '')
            category_name = request.POST.get('category', 'medical')
            starting_price = request.POST.get('starting_price', 0)

            if not name:
                return JsonResponse({'success': False, 'message': 'Treatment name is required.'})

            # Get or create category
            category, created = TreatmentCategory.objects.get_or_create(
                name=category_name.title(),
                defaults={'type': category_name}
            )

            treatment = Treatment.objects.create(
                name=name,
                category=category,
                starting_price=starting_price
            )

            return JsonResponse({
                'success': True,
                'message': 'Treatment added successfully.',
                'treatment_id': treatment.id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_edit_treatment(request, treatment_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            treatment = Treatment.objects.get(id=treatment_id)
            treatment.name = request.POST.get('name', treatment.name)

            category_name = request.POST.get('category', '')
            if category_name:
                category, created = TreatmentCategory.objects.get_or_create(
                    name=category_name.title(),
                    defaults={'type': category_name}
                )
                treatment.category = category

            starting_price = request.POST.get(
                'starting_price', treatment.starting_price)
            treatment.starting_price = starting_price
            treatment.save()

            return JsonResponse({
                'success': True,
                'message': 'Treatment updated successfully.'
            })
        except Treatment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Treatment not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_delete_treatment(request, treatment_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            treatment = Treatment.objects.get(id=treatment_id)
            treatment.delete()
            return JsonResponse({
                'success': True,
                'message': 'Treatment deleted successfully.'
            })
        except Treatment.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Treatment not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_delete_user(request, user_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'success': True, 'message': 'User deleted successfully.'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
@login_required
def admin_delete_review(request, review_id):
    if request.user.userprofile.user_type != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied.'})

    if request.method == 'POST':
        try:
            review = Feedback.objects.get(id=review_id)
            review.delete()
            return JsonResponse({
                'success': True,
                'message': 'Review deleted successfully.'
            })
        except Feedback.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Review not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
def patient_delete_review(request, review_id):
    if request.user.userprofile.user_type != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')

    if request.method == 'POST':
        try:
            review = Feedback.objects.get(
                id=review_id, patient=request.user.userprofile)
            review.delete()
            messages.success(request, 'Review deleted successfully.')
        except Feedback.DoesNotExist:
            messages.error(
                request, 'Review not found or you do not have permission to delete it.')
        except Exception as e:
            messages.error(request, f'Error deleting review: {str(e)}')

        return redirect('accounts:reviews_page')

    return redirect('accounts:reviews_page')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        user_type = request.POST.get('user_type', '')

        # Validation
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'accounts/signup.html')

        if len(username) < 3:
            messages.error(
                request, 'Username must be at least 3 characters long.')
            return render(request, 'accounts/signup.html')

        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'accounts/signup.html')

        if not user_type:
            messages.error(request, 'Please select an account type.')
            return render(request, 'accounts/signup.html')

        if user_type not in ['patient', 'doctor']:
            messages.error(request, 'Invalid account type selected.')
            return render(request, 'accounts/signup.html')

        if not password:
            messages.error(request, 'Password is required.')
            return render(request, 'accounts/signup.html')

        if len(password) < 6:
            messages.error(
                request, 'Password must be at least 6 characters long.')
            return render(request, 'accounts/signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')

        # Check if username already exists
        if User.objects.filter(username__iexact=username).exists():
            messages.error(
                request, 'Username already exists. Please choose a different username.')
            return render(request, 'accounts/signup.html')

        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request, 'Email already registered. Please use a different email or login instead.')
            return render(request, 'accounts/signup.html')

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

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

            messages.success(
                request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')

        except Exception as e:
            messages.error(
                request, 'There was an error creating your account. Please try again.')
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')


def test_auto_login(request):
    """Test view to verify auto-login functionality"""
    return render(request, 'accounts/test_auto_login.html')
