# Implementation Plan: Chatbot Smart Search Real-Time

## Overview

Fix broken JavaScript in `base.html`, replace the floating chatbot's unreliable fetch-redirect with a direct form POST, add real-time AJAX search to `smart_results.html`, wire the results-page chatbot to the smart-search API, add loading spinners, and fix the session context accumulation bug in `views.py`. All changes are frontend JS + backend Python — no new models or migrations required.

## Tasks

- [x] 1. Fix broken JavaScript in base.html (Req 1)
  - Locate the stray `// Enable dropdown submenu functionality` block that sits outside the closing `</script>` tag of the floating chatbot script block
  - Remove the orphaned `</script>` tag that closes the chatbot block prematurely
  - Wrap the dropdown submenu code inside a new `<script>…</script>` element placed before `</body>`, or merge it into the existing chatbot `<script>` block
  - Verify there is exactly one closing `</script>` for the chatbot block and no JS code appears between that tag and `</body>` outside a valid `<script>` element
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Fix floating chatbot form submission in base.html (Req 2)
  - [x] 2.1 Replace `submitToSmartResults()` with a direct HTML form POST
    - Remove the `fetch('/enquiries/results/', …)` call and its `.catch` fallback
    - Build a `<form method="POST" action="/enquiries/results/">` element programmatically (same pattern as `bot_interface.html`'s `submitToSmartResults()`)
    - Add a hidden `csrfmiddlewaretoken` input using `getCsrfToken()`
    - Add a hidden `query` input with the trimmed message value
    - Guard: return early if query is empty AND no file is attached
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

  - [x] 2.2 Handle file attachment in the form POST
    - When `fileInput.files` has a file, set `form.enctype = 'multipart/form-data'`
    - Clone the file input (or append the file input node) into the form before submitting
    - _Requirements: 2.3_

- [x] 3. Enrich `smart_results_api` JSON response (prerequisite for Req 3 & 4)
  - [x] 3.1 Add full card fields to the API serialization in `enquiry_bot/views.py`
    - Doctors: include `profile_picture`, `specialization`, `rating`, `experience_years`, `key_points`, `slug`
    - Hospitals: include `profile_picture`, `city`, `state`, `rating`, `jci_accredited`, `nabh_accredited`, `beds_count`, `slug`
    - Treatments: include `description`, `starting_price`, `duration`, `slug`
    - Blogs: include `title`, `published_at` (ISO string), `slug`
    - Keep existing `name`/`title` and `slug` fields
    - _Requirements: 3.2_

- [x] 4. Fix session context accumulation bug in views.py (Req 6)
  - [x] 4.1 Change `smart_results_view` to store only `intent.conditions`
    - Replace `request.session['chatbot_context'] = intent.keywords` with `request.session['chatbot_context'] = intent.conditions`
    - When merging prior context: read `prior_conditions = request.session.get('chatbot_context', [])` and merge only into the query text if non-empty (existing merge logic is fine once the stored value is conditions-only)
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 4.2 Change `smart_results_api` to store only `intent.conditions`
    - Apply the same fix: replace `intent.keywords` with `intent.conditions` in the session assignment
    - When new query produces no conditions (`intent.conditions` is empty), do NOT overwrite the session — keep prior conditions intact
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 4.3 Write property-based test for session context accumulation
    - Use `hypothesis` (already present in the project via `.hypothesis/` directory)
    - **Property 1: Conditions-only storage** — for any sequence of queries, `session['chatbot_context']` after each call contains only strings that appear in `CONDITION_SPECIALIZATION_MAP` keys (never raw fallback tokens)
    - **Validates: Requirements 6.1, 6.5**
    - **Property 2: Fallback-token isolation** — when a query produces `intent.conditions == []`, the session value is unchanged from before the call
    - **Validates: Requirements 6.3**
    - Place tests in `enquiry_bot/tests/test_session_context.py`

- [x] 5. Add real-time AJAX search to smart_results.html (Req 3)
  - [x] 5.1 Intercept the search form submit with JavaScript
    - Add a `<script>` block at the bottom of `smart_results.html` (inside `{% block content %}`)
    - Call `event.preventDefault()` on the form's `submit` event
    - Collect `query` and optional `medical_report` file into a `FormData` object
    - POST to `/enquiries/results/api/` with the CSRF token in the `X-CSRFToken` header
    - _Requirements: 3.1, 3.5, 3.6_

  - [x] 5.2 Render doctor cards from JSON and inject into the DOM
    - Write a `renderDoctors(doctors)` JS function that builds the same Bootstrap card HTML as the Django template's doctor loop
    - Include `profile_picture` (with `ui-avatars.com` fallback), `name`, `specialization`, `rating`, `experience_years`, `key_points`, and a "View Profile" link using `slug`
    - Target the existing doctors section container and replace its inner HTML
    - _Requirements: 3.2_

  - [x] 5.3 Render hospital, treatment, and blog cards from JSON
    - Write `renderHospitals(hospitals)`, `renderTreatments(treatments)`, `renderBlogs(blogs)` functions matching the existing template card markup
    - Hospitals: `profile_picture`, `name`, `city`, `state`, `rating`, accreditation badges, `beds_count`, "View Hospital" link
    - Treatments: `name`, `description`, `starting_price`, `duration`, "Learn More" link
    - Blogs: `title`, `published_at` (formatted), "Read Article" link
    - _Requirements: 3.2_

  - [x] 5.4 Update query summary strip and handle section visibility
    - After a successful API response, update the `query_summary` strip text with `data.query_summary`
    - Show/hide each section wrapper based on whether the returned array is non-empty (mirror the `has_data` / `coming_soon` logic from the template)
    - _Requirements: 3.3_

  - [x] 5.5 Show error message on API failure
    - On non-2xx response or network error, inject a dismissible Bootstrap alert above the results grid
    - Do not clear or replace existing result cards on failure
    - _Requirements: 3.4_

- [x] 6. Wire results-page chatbot to smart search API (Req 4)
  - [x] 6.1 Replace `sendMessage()` on the results page with a smart-search call
    - In `bot_interface.html`, when `isResultsPage` is true, replace the `fetch('{% url "enquiry_bot:chat_api" %}', …)` call with a POST to `/enquiries/results/api/`
    - Send `query` as form-encoded body (not JSON), include CSRF token
    - _Requirements: 4.1_

  - [x] 6.2 Update result sections from chatbot response
    - After a successful API response, call the same `renderDoctors`, `renderHospitals`, `renderTreatments`, `renderBlogs` functions used by the search form (extract them to a shared module or inline them in `bot_interface.html`)
    - _Requirements: 4.2_

  - [x] 6.3 Show user message bubble and bot response bubble
    - Before the API call: call `addMessage('user', message)` to show the user's text in the chat window
    - On success: call `addMessage('bot', data.query_summary)` to show the bot's response
    - On error: call `addMessage('bot', 'Sorry, I couldn\'t process your request. Please try again.')` 
    - _Requirements: 4.3, 4.4, 4.5_

- [x] 7. Add loading spinner and button disable states (Req 5)
  - [x] 7.1 Add spinner overlay to smart_results.html results area
    - Add a `<div id="results-spinner">` overlay element (Bootstrap spinner or custom CSS) positioned over the results grid container
    - Show it at the start of the AJAX request, hide it on completion (success or error)
    - _Requirements: 5.1_

  - [x] 7.2 Disable/re-enable submit button during AJAX requests on smart_results.html
    - Set `submitBtn.disabled = true` before the fetch call
    - Set `submitBtn.disabled = false` in the `finally` block
    - _Requirements: 5.2, 5.3_

  - [x] 7.3 Disable send button and show loading state in base.html floating chatbot
    - In `base.html`, set `sendBtn.disabled = true` immediately when `submitToSmartResults()` is called
    - Optionally change the button icon to a spinner (`<span class="spinner-border spinner-border-sm">`) while the form navigates away
    - _Requirements: 5.4_

- [x] 8. Checkpoint — verify all changes integrate correctly
  - Ensure all Python tests pass: `python manage.py test enquiry_bot`
  - Manually verify: (a) base.html loads with no JS errors, (b) floating chatbot POSTs correctly, (c) smart_results.html updates in-place on search, (d) chatbot on results page updates cards and shows bubbles, (e) spinner appears and disappears, (f) session stores only conditions
  - Ask the user if any questions arise before proceeding.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Task 3 (API enrichment) must be completed before Tasks 5 and 6, since the JS renderers depend on the richer JSON fields
- Task 4 (session fix) is independent and can be done in parallel with Tasks 5–7
- The `renderDoctors`/`renderHospitals`/`renderTreatments`/`renderBlogs` functions are needed by both the search form (Task 5) and the chatbot (Task 6) — define them once in `smart_results.html` and call them from both handlers
- Property tests in Task 4.3 use `hypothesis`, which is already installed (`.hypothesis/` directory exists in the project root)
- No new Django models or migrations are required for any task
