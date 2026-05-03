from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from .models import Doctor, DoctorMedia
from .forms import DoctorMediaForm
from feedbacks.models import Feedback  # Add this import
from treatments.models import Treatment
from hospitals.models import Hospital


def doctors_list(request: HttpRequest) -> HttpResponse:
    doctors = Doctor.objects.all()  # type: ignore
    
    # Get filter parameters from request
    search = request.GET.get('search', '')
    specialization = request.GET.get('specialization', '')
    experience = request.GET.get('experience', '')
    rating = request.GET.get('rating', '')
    treatment = request.GET.get('treatment', '')  # Add treatment filter
    hospital_id = request.GET.get('hospital', '')  # Add hospital filter for related doctors
    treatment_id = request.GET.get('treatment_id', '')  # Add treatment filter for related doctors
    
    # Apply search filter
    if search:
        name_filter = Q(name__icontains=search)
        specialization_filter = Q(specialization__icontains=search)
        doctors = doctors.filter(name_filter | specialization_filter)  # type: ignore
    
    # Apply filters if provided
    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)  # type: ignore
    
    if experience:
        if experience == '5+ years':
            doctors = doctors.filter(experience_years__gte=5)  # type: ignore
        elif experience == '10+ years':
            doctors = doctors.filter(experience_years__gte=10)  # type: ignore
        elif experience == '15+ years':
            doctors = doctors.filter(experience_years__gte=15)  # type: ignore
        elif experience == '20+ years':
            doctors = doctors.filter(experience_years__gte=20)  # type: ignore
    
    if rating:
        if rating == '4.5+ stars':
            doctors = doctors.filter(rating__gte=4.5)  # type: ignore
        elif rating == '4.0+ stars':
            doctors = doctors.filter(rating__gte=4.0)  # type: ignore
        elif rating == '3.5+ stars':
            doctors = doctors.filter(rating__gte=3.5)  # type: ignore
    
    # Add treatment filter
    if treatment:
        doctors = doctors.filter(treatments__name__icontains=treatment)  # type: ignore
    
    # Add hospital filter for related doctors
    if hospital_id:
        doctors = doctors.filter(hospitals__id=hospital_id)  # type: ignore
    
    # Add treatment ID filter for related doctors
    if treatment_id:
        doctors = doctors.filter(treatments__id=treatment_id)  # type: ignore
    
    # Remove duplicates if any filters were applied
    if search or specialization or experience or rating or treatment or hospital_id or treatment_id:
        doctors = doctors.distinct()  # type: ignore
    
    context = {
        'doctors': doctors,
        'search_filter': search,
        'specialization_filter': specialization,
        'experience_filter': experience,
        'rating_filter': rating,
        'treatment_filter': treatment,
        'hospital_filter': hospital_id,
        'treatment_id_filter': treatment_id,
    }
    
    return render(request, "doctors/list.html", context)


def doctor_detail(request: HttpRequest, slug: str) -> HttpResponse:
    doctor = get_object_or_404(Doctor, slug=slug)
    # Fetch approved feedback for this doctor
    feedbacks = Feedback.objects.filter(doctor=doctor, is_approved=True).select_related('patient').order_by('-created_at')  # type: ignore
    
    # Paginate treatments (areas of expertise)
    treatments = doctor.treatments.all().order_by('name')
    treatments_paginator = Paginator(treatments, 10)
    treatments_page_number = request.GET.get('treatments_page')
    treatments_page_obj = treatments_paginator.get_page(treatments_page_number)
    
    # Paginate feedbacks (patient reviews)
    feedbacks_paginator = Paginator(feedbacks, 10)
    feedbacks_page_number = request.GET.get('feedbacks_page')
    feedbacks_page_obj = feedbacks_paginator.get_page(feedbacks_page_number)
    
    # Get affiliated hospitals
    affiliated_hospitals = doctor.hospitals.all()
    
    return render(request, "doctors/detail.html", {
        "doctor": doctor, 
        "treatments_page_obj": treatments_page_obj,
        "feedbacks_page_obj": feedbacks_page_obj,
        "affiliated_hospitals": affiliated_hospitals
    })


@login_required
def doctor_media_upload(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Check if the logged-in user is the doctor
    user_full_name = f"{request.user.first_name} {request.user.last_name}".strip()
    if not doctor.name.__contains__(user_full_name):
        messages.error(request, "You don't have permission to upload media for this doctor.")
        return redirect('doctor_dashboard')
    
    if request.method == 'POST':
        form = DoctorMediaForm(request.POST)
        if form.is_valid():
            media = form.save(commit=False)
            media.doctor = doctor
            media.save()
            messages.success(request, "Media uploaded successfully!")
            return redirect('doctor_profile')
    else:
        form = DoctorMediaForm()
    
    return render(request, 'doctors/media_upload.html', {'form': form, 'doctor': doctor})


@login_required
def doctor_media_manage(request):
    # Get the doctor object by matching the user's full name with doctor names
    user_full_name = f"{request.user.first_name} {request.user.last_name}".strip()
    doctor = Doctor.objects.filter(name__icontains=user_full_name).first()  # type: ignore
    if not doctor:
        # Fallback to get any doctor if name matching fails
        doctor = Doctor.objects.first()  # type: ignore
    
    if not doctor:
        messages.error(request, "No doctor profile found.")
        return redirect('doctor_dashboard')
    
    # Check if the logged-in user is the doctor
    if not doctor.name.__contains__(user_full_name):
        messages.error(request, "You don't have permission to manage media for this doctor.")
        return redirect('doctor_dashboard')
    
    # Get all media for this doctor
    media_items = DoctorMedia.objects.filter(doctor=doctor)  # type: ignore
    
    if request.method == 'POST':
        # Handle media deletion
        media_id = request.POST.get('media_id')
        if media_id:
            try:
                media = DoctorMedia.objects.get(id=media_id, doctor=doctor)  # type: ignore
                media.delete()
                messages.success(request, "Media deleted successfully!")
            except DoctorMedia.DoesNotExist:  # type: ignore
                messages.error(request, "Media not found.")
        return redirect('doctor_media_manage')
    
    return render(request, 'doctors/media_manage.html', {
        'doctor': doctor,
        'media_items': media_items
    })


@require_http_methods(["GET"])
def search_doctors_api(request: HttpRequest) -> JsonResponse:
    """
    API endpoint to search for doctors by name
    """
    query = request.GET.get('query', '')
    
    if not query or len(query) < 2:
        return JsonResponse({
            'success': False,
            'error': 'Query too short'
        })
    
    doctors = Doctor.objects.filter(name__icontains=query)[:10]  # type: ignore
    
    results = []
    for doctor in doctors:
        # Use a default price since doctors don't have a direct price field
        # We'll use the average of treatments they offer or a default value
        default_price = 100.0  # Default consultation fee
        results.append({
            'id': doctor.id,
            'name': doctor.name,
            'slug': doctor.slug,
            'specialty': doctor.specialization if doctor.specialization else '',
            'price': default_price,
            'url': f'/doctors/{doctor.slug}/'
        })
    
    return JsonResponse({
        'success': True,
        'results': results
    })