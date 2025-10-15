from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import Feedback
from accounts.models import UserProfile

def feedback_list(request, content_type, object_id):
    """Display feedback for a specific object (doctor, hospital, treatment)"""
    # Map content types to models
    content_types = {
        'doctor': 'doctors.Doctor',
        'hospital': 'hospitals.Hospital',
        'treatment': 'treatments.Treatment',
    }
    
    if content_type not in content_types:
        return JsonResponse({'error': 'Invalid content type'}, status=400)
    
    # Get the model class
    model_path = content_types[content_type]
    app_label, model_name = model_path.split('.')
    content_type_obj = get_object_or_404(ContentType, app_label=app_label, model=model_name.lower())
    
    # Get the object
    obj = get_object_or_404(content_type_obj.model_class(), id=object_id)
    
    # Get approved feedback for this object
    feedback_filter = {}
    feedback_filter[content_type] = obj
    feedback_filter['is_approved'] = True
    
    feedbacks = Feedback.objects.filter(**feedback_filter).select_related('patient')
    
    return render(request, 'feedbacks/feedback_list.html', {
        'feedbacks': feedbacks,
        'object': obj,
        'content_type': content_type
    })

@login_required
@transaction.atomic
def submit_feedback(request, content_type, object_id):
    """Handle feedback submission"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Map content types to models
    content_types = {
        'doctor': 'doctors.Doctor',
        'hospital': 'hospitals.Hospital',
        'treatment': 'treatments.Treatment',
    }
    
    if content_type not in content_types:
        return JsonResponse({'error': 'Invalid content type'}, status=400)
    
    # Get the model class
    model_path = content_types[content_type]
    app_label, model_name = model_path.split('.')
    content_type_obj = get_object_or_404(ContentType, app_label=app_label, model=model_name.lower())
    
    # Get the object
    obj = get_object_or_404(content_type_obj.model_class(), id=object_id)
    
    # Get form data
    rating = request.POST.get('rating')
    title = request.POST.get('title')
    comment = request.POST.get('comment')
    
    # Validate data
    if not all([rating, title, comment]):
        return JsonResponse({'error': 'All fields are required'}, status=400)
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid rating'}, status=400)
    
    # Create feedback - Changed to is_approved=True so reviews are immediately visible
    feedback = Feedback.objects.create(
        patient=request.user.userprofile,
        feedback_type=content_type,
        rating=rating,
        title=title,
        comment=comment,
        is_approved=True  # Changed from False to True - reviews are immediately public
    )
    
    # Set the appropriate foreign key based on content type
    if content_type == 'doctor':
        feedback.doctor = obj
    elif content_type == 'hospital':
        feedback.hospital = obj
    elif content_type == 'treatment':
        feedback.treatment = obj
    
    feedback.save()
    
    messages.success(request, 'Thank you for your feedback! Your review is now visible to everyone.')
    
    # Redirect based on content type
    if content_type == 'doctor':
        return redirect('doctor_detail', slug=obj.slug)
    elif content_type == 'hospital':
        return redirect('hospital_detail', slug=obj.slug)
    else:  # treatment
        return redirect('treatment_detail', pk=object_id)
