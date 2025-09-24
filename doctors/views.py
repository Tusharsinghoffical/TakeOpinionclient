from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Doctor, DoctorMedia
from .forms import DoctorMediaForm


def doctors_list(request: HttpRequest) -> HttpResponse:
    doctors = Doctor.objects.all()  # type: ignore
    
    # Get filter parameters from request
    specialization = request.GET.get('specialization', '')
    experience = request.GET.get('experience', '')
    rating = request.GET.get('rating', '')
    
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
    
    context = {
        'doctors': doctors,
        'specialization_filter': specialization,
        'experience_filter': experience,
        'rating_filter': rating,
    }
    
    return render(request, "doctors/list.html", context)


def doctor_detail(request: HttpRequest, slug: str) -> HttpResponse:
    doctor = get_object_or_404(Doctor, slug=slug)
    return render(request, "doctors/detail.html", {"doctor": doctor})


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