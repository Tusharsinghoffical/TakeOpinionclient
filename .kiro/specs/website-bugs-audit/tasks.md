# Implementation Tasks — Website Bugs Audit

## Tasks

- [x] 1. Fix CRITICAL bugs — application crashes and unreachable pages
  - [x] 1.1 Fix BUG 1: IntegrityError on simple appointment booking (`bookings/views.py`)
    - In `appointment_booking` view, replace `treatment=None` with a get-or-create fallback for a "General Appointment" Treatment
    - Ensure the fallback Treatment is linked to a "General" TreatmentCategory (get-or-create that too)
    - The booking must save successfully without raising IntegrityError
  - [x] 1.2 Fix BUG 2: Register missing `appointment_booking` URL (`bookings/urls.py`)
    - Add `path("appointment/", views.appointment_booking, name="appointment_booking")` to `bookings/urls.py`
    - Verify `{% url 'bookings:appointment_booking' %}` resolves without NoReverseMatch
  - [x] 1.3 Fix BUG 3: Create missing `core/terms.html` template
    - Create `core/templates/core/terms.html` extending the base template
    - Include standard Terms of Service sections: Introduction, Use of Service, Privacy, Disclaimers, Contact
    - Style consistently with the existing `core/privacy.html` template
  - [x] 1.4 Fix BUG 3: Create missing `core/static_check.html` template
    - Create `core/templates/core/static_check.html` extending the base template
    - Display a simple static files status/diagnostic page

- [x] 2. Fix HIGH bugs — runtime errors and access control failures
  - [x] 2.1 Fix BUG 4: Correct URL namespace in doctor profile redirect (`accounts/views.py`)
    - Change `redirect('doctor_profile')` to `redirect('accounts:doctor_profile')` in `accounts/views.py` (~line 440)
  - [x] 2.2 Fix BUG 4: Correct URL namespace in doctor media upload redirect (`doctors/views.py`)
    - Change `redirect('doctor_profile')` to `redirect('accounts:doctor_profile')` in `doctors/views.py` (~line 129)
  - [x] 2.3 Fix BUG 5: Replace non-existent `doctor_dashboard` URL in `doctors/views.py`
    - Change `redirect('doctor_dashboard')` to `redirect('home')` in both `doctor_media_upload` and `doctor_media_manage` views
  - [x] 2.4 Fix BUG 6: Rewrite hotel search queryset to avoid `.filter()` on `.union()` (`hotels/views.py`)
    - Replace the `name_results.union(description_results, amenities_results)` pattern with a single `Q`-based filter
    - The city filter must be applied after the query filter without error
  - [x] 2.5 Fix BUG 7: Role-based redirect in `payment_success` view (`payments/views.py`)
    - Check `request.user.userprofile.user_type` and redirect admins to `accounts:admin_dashboard`, all other users to `accounts:patient_portal`
    - Wrap in try/except so any profile lookup failure falls back to `redirect('home')`

- [x] 3. Fix MEDIUM bugs — logic errors and security issues
  - [x] 3.1 Fix BUG 8: Make `Booking.__str__` null-safe (`bookings/models.py`)
    - Change `__str__` to return `"Booking (no treatment)"` when `self.treatment` is `None`
    - Return `f"Booking for {self.treatment.name}"` when treatment exists (unchanged)
  - [x] 3.2 Fix BUG 9: Replace fragile name-based doctor lookup with reliable identifier lookup (`accounts/views.py`, `doctors/views.py`)
    - In `accounts/views.py` `doctor_profile` view: look up Doctor by `email__iexact=request.user.email` first, then fall back to `name__iexact` full name match; remove the unsafe `Doctor.objects.first()` fallback
    - In `doctors/views.py` `doctor_media_manage` view: apply the same reliable lookup and remove the `Doctor.objects.first()` fallback
    - If no Doctor record is found, show an error message and redirect to `home` instead of silently using the wrong record
  - [x] 3.3 Fix BUG 10: Complete the truncated `analyze_medical_report` function (`enquiry_bot/views.py`)
    - Complete the cut-off `elif` branch for cancer/oncology with `Doctor.objects.prefetch_related('hospitals').filter(Q(specialization__icontains='oncology') | Q(specialization__icontains='cancer'))[:3]`
    - Add remaining `elif` branches for gastroenterology, urology, dermatology, and a final `else` fallback that returns general doctors
    - Ensure the function is syntactically complete and returns a valid `JsonResponse`
  - [x] 3.4 Fix BUG 11: Remove duplicate `login_required` import (`hotels/views.py`)
    - Remove the second `from django.contrib.auth.decorators import login_required` import line (the one in the middle of the file, after the `import json` block)
    - Keep only the first import at the top of the file

- [x] 4. Fix LOW bugs — security hardening and configuration cleanup
  - [x] 4.1 Fix BUG 12: Move `SECRET_KEY` to environment variable (`takeopinion/settings.py`)
    - Replace the hardcoded string with `os.environ.get('SECRET_KEY', '<current-insecure-key-as-dev-fallback>')`
    - Confirm `import os` is already present at the top of the file
  - [x] 4.2 Fix BUG 13: Remove duplicate WhiteNoise middleware entry (`takeopinion/settings_prod.py`)
    - Locate and remove the duplicate `whitenoise.middleware.WhiteNoiseMiddleware` entry from the `MIDDLEWARE` list in `settings_prod.py`
