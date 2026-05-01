# Bugfix Requirements Document

## Introduction

This document captures all confirmed bugs found during a comprehensive audit of the TakeOpinion Django medical tourism website. The bugs span 13 issues across 8 application modules (`bookings`, `core`, `accounts`, `doctors`, `hotels`, `payments`, `enquiry_bot`, and `takeopinion` settings). Severity ranges from CRITICAL application crashes and unreachable pages, through HIGH runtime errors and access control failures, to MEDIUM logic/security flaws and LOW code quality issues. Each bug is documented with its defective behavior, the correct behavior it should exhibit, and the surrounding behaviors that must be preserved unchanged.

---

## Bug Analysis

---

### BUG 1 — CRITICAL: IntegrityError on Simple Appointment Booking

**Affected file:** `bookings/views.py` — `appointment_booking` view

#### Current Behavior (Defect)

1.1 WHEN a user submits the simple appointment booking form THEN the system creates a `Booking` object with `treatment=None` and crashes with a database `IntegrityError` because `Booking.treatment` is a non-nullable `ForeignKey`.

#### Expected Behavior (Correct)

2.1 WHEN a user submits the simple appointment booking form THEN the system SHALL create the `Booking` object with a valid `treatment` value (or handle the absence of a treatment gracefully) without raising an `IntegrityError`.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user submits the full consultation booking form with a valid treatment THEN the system SHALL CONTINUE TO create the booking successfully and redirect to the confirmation page.
3.2 WHEN a user submits any booking form with all required fields populated THEN the system SHALL CONTINUE TO persist the booking to the database correctly.

---

### BUG 2 — CRITICAL: Missing URL for `appointment_booking` View

**Affected file:** `bookings/urls.py`

#### Current Behavior (Defect)

1.1 WHEN a user navigates to the appointment booking page or the template renders `{% url 'appointment_booking' %}` THEN the system raises a `NoReverseMatch` error because the `appointment_booking` view is not registered in `bookings/urls.py`.

#### Expected Behavior (Correct)

2.1 WHEN a user navigates to the appointment booking page THEN the system SHALL resolve the URL correctly and render the appointment booking form without error.
2.2 WHEN the template renders `{% url 'appointment_booking' %}` THEN the system SHALL return the correct URL path without raising `NoReverseMatch`.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user navigates to any other registered booking URL (e.g., consultation booking, booking confirmation) THEN the system SHALL CONTINUE TO resolve and render those pages correctly.

---

### BUG 3 — CRITICAL: Missing Templates `core/terms.html` and `core/static_check.html`

**Affected file:** `core/views.py` — `terms()` and `static_files_check()` views

#### Current Behavior (Defect)

1.1 WHEN a user clicks "Terms of Service" anywhere on the site (base template, signup page, booking pages, contact page) THEN the system raises a `TemplateDoesNotExist` error because `core/terms.html` does not exist on the filesystem.
1.2 WHEN the `static_files_check` view is invoked THEN the system raises a `TemplateDoesNotExist` error because `core/static_check.html` does not exist on the filesystem.

#### Expected Behavior (Correct)

2.1 WHEN a user clicks "Terms of Service" THEN the system SHALL render the `core/terms.html` template and display the terms of service page without error.
2.2 WHEN the `static_files_check` view is invoked THEN the system SHALL render the `core/static_check.html` template without error.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user navigates to any other `core` page (home, contact, privacy, pricing, etc.) THEN the system SHALL CONTINUE TO render those templates correctly.

---

### BUG 4 — HIGH: Wrong URL Name in Redirect After Doctor Profile Update

**Affected files:** `accounts/views.py` (~line 440), `doctors/views.py` (~line 129)

#### Current Behavior (Defect)

1.1 WHEN a doctor saves their profile via `accounts/views.py` THEN the system raises a `NoReverseMatch` error because `redirect('doctor_profile')` is used instead of the namespaced `redirect('accounts:doctor_profile')`.
1.2 WHEN a doctor uploads media via `doctors/views.py` THEN the system raises a `NoReverseMatch` error for the same reason.

#### Expected Behavior (Correct)

2.1 WHEN a doctor saves their profile THEN the system SHALL redirect to `accounts:doctor_profile` successfully without raising `NoReverseMatch`.
2.2 WHEN a doctor uploads media THEN the system SHALL redirect to `accounts:doctor_profile` successfully without raising `NoReverseMatch`.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a doctor views their profile page directly THEN the system SHALL CONTINUE TO render the doctor profile page correctly.
3.2 WHEN a patient saves their profile THEN the system SHALL CONTINUE TO redirect to the correct patient profile URL without error.

---

### BUG 5 — HIGH: `doctor_dashboard` URL Name Does Not Exist

**Affected file:** `doctors/views.py` — `doctor_media_upload` and `doctor_media_manage` views

#### Current Behavior (Defect)

1.1 WHEN a non-doctor user attempts to access the `doctor_media_upload` view THEN the system raises a `NoReverseMatch` error because `redirect('doctor_dashboard')` references a URL name that does not exist anywhere in the project.
1.2 WHEN a non-doctor user attempts to access the `doctor_media_manage` view THEN the system raises a `NoReverseMatch` error for the same reason.

#### Expected Behavior (Correct)

2.1 WHEN a non-doctor user attempts to access `doctor_media_upload` THEN the system SHALL redirect to an existing URL (e.g., the home page or login page) with an appropriate permission-denied message.
2.2 WHEN a non-doctor user attempts to access `doctor_media_manage` THEN the system SHALL redirect to an existing URL with an appropriate permission-denied message.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN an authenticated doctor accesses `doctor_media_upload` THEN the system SHALL CONTINUE TO render the media upload form correctly.
3.2 WHEN an authenticated doctor accesses `doctor_media_manage` THEN the system SHALL CONTINUE TO render the media management page correctly.

---

### BUG 6 — HIGH: `.filter()` Called on a `.union()` Queryset in Hotel Search

**Affected file:** `hotels/views.py` — `search_hotels_api` view (~line 112–115)

#### Current Behavior (Defect)

1.1 WHEN a user provides both a `query` parameter and a `city` parameter in the hotel search API THEN the system raises a `TypeError` at runtime because `.filter(city__icontains=city)` is called on a `.union()` queryset, which Django does not support.

#### Expected Behavior (Correct)

2.1 WHEN a user provides both a `query` parameter and a `city` parameter THEN the system SHALL apply the city filter before combining querysets (or use an alternative approach that avoids filtering on a union queryset) and return the correctly filtered hotel results without error.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user provides only a `query` parameter (no `city`) THEN the system SHALL CONTINUE TO return hotel search results correctly.
3.2 WHEN a user provides only a `city` parameter (no `query`) THEN the system SHALL CONTINUE TO return hotel results filtered by city correctly.
3.3 WHEN a user provides neither `query` nor `city` THEN the system SHALL CONTINUE TO return the default hotel listing without error.

---

### BUG 7 — HIGH: `payment_success` View Redirects All Users to Admin Dashboard

**Affected file:** `payments/views.py` — `payment_success` view

#### Current Behavior (Defect)

1.1 WHEN any user (including a patient) completes a successful payment THEN the system redirects them to `accounts:admin_dashboard`, which denies access to non-admin users and shows an "Access denied" error immediately after payment.

#### Expected Behavior (Correct)

2.1 WHEN a patient completes a successful payment THEN the system SHALL redirect them to the patient dashboard or a payment confirmation page appropriate for their role.
2.2 WHEN an admin completes a payment THEN the system SHALL redirect them to the admin dashboard.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a payment fails or is cancelled THEN the system SHALL CONTINUE TO handle the failure case correctly and not redirect to any dashboard.
3.2 WHEN an admin user views the admin dashboard directly THEN the system SHALL CONTINUE TO render it correctly with no change to admin access controls.

---

### BUG 8 — MEDIUM: `Booking.__str__` Crashes When `treatment` Is None

**Affected file:** `bookings/models.py`

#### Current Behavior (Defect)

1.1 WHEN `str()` is called on a `Booking` instance where `treatment` is `None` (e.g., in the Django admin panel or any queryset rendering) THEN the system raises `AttributeError: 'NoneType' object has no attribute 'name'`.

#### Expected Behavior (Correct)

2.1 WHEN `str()` is called on a `Booking` instance where `treatment` is `None` THEN the system SHALL return a safe fallback string (e.g., `"Booking (no treatment)"`) without raising an `AttributeError`.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN `str()` is called on a `Booking` instance where `treatment` is a valid `Treatment` object THEN the system SHALL CONTINUE TO return the string including the treatment name as before.

---

### BUG 9 — MEDIUM: Doctor Profile Matched by Name Is Fragile and Insecure

**Affected files:** `accounts/views.py` — `doctor_profile` view, `doctors/views.py` — `doctor_media_manage`

#### Current Behavior (Defect)

1.1 WHEN a logged-in doctor's full name does not exactly match any `Doctor` record via `icontains` lookup THEN the system falls back to `Doctor.objects.first()`, causing the wrong doctor's profile to be displayed or edited.
1.2 WHEN multiple doctors have similar names THEN the system may match the wrong doctor's profile due to the `icontains` partial-match logic.

#### Expected Behavior (Correct)

2.1 WHEN a logged-in doctor views or edits their profile THEN the system SHALL look up the `Doctor` record by a reliable unique identifier (e.g., a foreign key from `UserProfile` to `Doctor`) rather than by name string matching.
2.2 WHEN no matching `Doctor` record is found for the logged-in user THEN the system SHALL return an appropriate error or redirect rather than falling back to an arbitrary doctor record.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN a doctor with a correctly linked profile views their profile page THEN the system SHALL CONTINUE TO display their own profile data correctly.
3.2 WHEN a patient views a doctor's public profile page THEN the system SHALL CONTINUE TO display the correct doctor's information.

---

### BUG 10 — MEDIUM: `enquiry_bot/views.py` Has a Truncated/Incomplete Function Causing Syntax Error

**Affected file:** `enquiry_bot/views.py` — `analyze_medical_report` function

#### Current Behavior (Defect)

1.1 WHEN Django starts up and attempts to import the `enquiry_bot` app THEN the system raises a `SyntaxError` (or `IndentationError`) because `analyze_medical_report` is truncated mid-statement (`doctor_queryset = Doct`), causing the entire application to fail to start.

#### Expected Behavior (Correct)

2.1 WHEN Django starts up THEN the system SHALL import the `enquiry_bot` app successfully without any syntax errors.
2.2 WHEN `analyze_medical_report` is called THEN the system SHALL execute the complete function logic and return a valid response.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN any other view in `enquiry_bot/views.py` is called THEN the system SHALL CONTINUE TO function correctly once the syntax error is resolved.
3.2 WHEN Django starts up with all other apps intact THEN the system SHALL CONTINUE TO start successfully regardless of the `enquiry_bot` fix.

---

### BUG 11 — MEDIUM: Duplicate Import of `login_required` in `hotels/views.py`

**Affected file:** `hotels/views.py`

#### Current Behavior (Defect)

1.1 WHEN `hotels/views.py` is imported THEN the system contains a duplicate `from django.contrib.auth.decorators import login_required` statement, indicating copy-paste errors and reducing code maintainability.

#### Expected Behavior (Correct)

2.1 WHEN `hotels/views.py` is imported THEN the system SHALL contain only a single import of `login_required` at the top of the file.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN any hotel view decorated with `@login_required` is accessed by an unauthenticated user THEN the system SHALL CONTINUE TO redirect to the login page correctly.
3.2 WHEN any hotel view decorated with `@login_required` is accessed by an authenticated user THEN the system SHALL CONTINUE TO render the view correctly.

---

### BUG 12 — LOW: Hardcoded Secret Key in `settings.py`

**Affected file:** `takeopinion/settings.py`

#### Current Behavior (Defect)

1.1 WHEN `takeopinion/settings.py` is committed to version control THEN the system exposes the hardcoded `SECRET_KEY` string literal, creating a security vulnerability that allows attackers to forge session cookies and CSRF tokens.

#### Expected Behavior (Correct)

2.1 WHEN the application loads its configuration THEN the system SHALL read `SECRET_KEY` from an environment variable or a secrets manager rather than from a hardcoded string literal in the settings file.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN the application starts in any environment where the `SECRET_KEY` environment variable is set THEN the system SHALL CONTINUE TO start successfully and use the provided key.
3.2 WHEN session-based authentication and CSRF protection are used THEN the system SHALL CONTINUE TO function correctly after the key is moved to an environment variable.

---

### BUG 13 — LOW: WhiteNoise Middleware Added Twice in Production Settings

**Affected file:** `takeopinion/settings_prod.py`

#### Current Behavior (Defect)

1.1 WHEN the application runs in production THEN the `MIDDLEWARE` list contains `WhiteNoiseMiddleware` twice (once from base settings and once from the production settings override), causing redundant static file processing on every request.

#### Expected Behavior (Correct)

2.1 WHEN the application runs in production THEN the `MIDDLEWARE` list SHALL contain `WhiteNoiseMiddleware` exactly once, with no duplicate entries.

#### Unchanged Behavior (Regression Prevention)

3.1 WHEN the application runs in production THEN the system SHALL CONTINUE TO serve static files correctly via WhiteNoise after the duplicate is removed.
3.2 WHEN the application runs in development (using base settings only) THEN the system SHALL CONTINUE TO behave as before with no change to middleware configuration.
