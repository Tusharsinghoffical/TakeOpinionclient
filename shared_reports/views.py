from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from doctors.models import Doctor
from .models import SharedReport, ReportMessage
import json


def share_report_page(request):
    """Page where a patient selects a doctor and uploads a report."""
    doctors = Doctor.objects.all().order_by('name')
    selected_doctor_id = request.GET.get('doctor')
    selected_doctor = None
    if selected_doctor_id:
        try:
            selected_doctor = Doctor.objects.get(id=selected_doctor_id)
        except Doctor.DoesNotExist:
            pass

    if request.method == 'POST':
        doctor_id   = request.POST.get('doctor_id')
        sender_name = request.POST.get('sender_name', '').strip()
        sender_email= request.POST.get('sender_email', '').strip()
        notes       = request.POST.get('notes', '').strip()
        report_file = request.FILES.get('report_file')

        if not doctor_id or not sender_name or not sender_email or not report_file:
            messages.error(request, 'Please fill all required fields and upload a report.')
            return render(request, 'shared_reports/share_report.html', {
                'doctors': doctors, 'selected_doctor': selected_doctor
            })

        doctor = get_object_or_404(Doctor, id=doctor_id)

        shared = SharedReport.objects.create(
            sender_name=sender_name,
            sender_email=sender_email,
            sender_user=request.user if request.user.is_authenticated else None,
            doctor=doctor,
            report_file=report_file,
            report_name=report_file.name,
            notes=notes,
        )

        # Auto-add patient's note as first message
        if notes:
            ReportMessage.objects.create(
                report=shared,
                sender=request.user if request.user.is_authenticated else None,
                sender_name=sender_name,
                is_doctor=False,
                message=notes,
            )

        messages.success(request, f'Report sent to Dr. {doctor.name} successfully!')
        return redirect('shared_reports:report_chat', report_id=shared.id)

    return render(request, 'shared_reports/share_report.html', {
        'doctors': doctors,
        'selected_doctor': selected_doctor,
    })


def report_chat(request, report_id):
    """Chat page for a specific shared report — visible to patient and doctor."""
    report = get_object_or_404(SharedReport, id=report_id)
    chat_messages = report.messages.all()

    # Mark as viewed if doctor is viewing
    if (request.user.is_authenticated and
            hasattr(request.user, 'userprofile') and
            request.user.userprofile.user_type == 'doctor' and
            report.status == 'pending'):
        report.status = 'viewed'
        report.save()

    if request.method == 'POST':
        msg_text = request.POST.get('message', '').strip()
        if msg_text:
            is_doc = (request.user.is_authenticated and
                      hasattr(request.user, 'userprofile') and
                      request.user.userprofile.user_type == 'doctor')
            sender_name = (request.user.get_full_name() or request.user.username
                           if request.user.is_authenticated else report.sender_name)
            ReportMessage.objects.create(
                report=report,
                sender=request.user if request.user.is_authenticated else None,
                sender_name=sender_name,
                is_doctor=is_doc,
                message=msg_text,
            )
            if is_doc:
                report.status = 'replied'
                report.save()
            return redirect('shared_reports:report_chat', report_id=report.id)

    return render(request, 'shared_reports/report_chat.html', {
        'report': report,
        'chat_messages': chat_messages,
    })


@login_required
def doctor_reports_inbox(request):
    """Doctor's inbox — all reports shared with them."""
    try:
        doctor = Doctor.objects.get(name__icontains=request.user.get_full_name() or request.user.username)
    except Doctor.DoesNotExist:
        doctor = Doctor.objects.filter(email=request.user.email).first()

    if not doctor:
        messages.error(request, 'No doctor profile linked to your account.')
        return redirect('home')

    reports = SharedReport.objects.filter(doctor=doctor).order_by('-created_at')
    return render(request, 'shared_reports/doctor_inbox.html', {
        'reports': reports,
        'doctor': doctor,
    })


def my_shared_reports(request):
    """Patient's list of reports they've shared."""
    if request.user.is_authenticated:
        reports = SharedReport.objects.filter(sender_user=request.user).order_by('-created_at')
    else:
        email = request.GET.get('email', '')
        reports = SharedReport.objects.filter(sender_email=email).order_by('-created_at') if email else []

    return render(request, 'shared_reports/my_reports.html', {'reports': reports})
