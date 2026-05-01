# Implementation Plan: Chatbot Smart Results

## Overview

Implement the Smart Results feature for the TakeOpinion enquiry bot. The work is organized into six sequential phases: (1) add the `hypothesis` dependency and `ChatbotSearchSession` model, (2) build the `smart_search.py` module with all core Python components, (3) add the Django views and URL routes, (4) create the `smart_results.html` template, (5) wire up the chatbot widget frontend redirect, and (6) write property-based and unit tests.

All code is Python / Django. Tests use `pytest` / `hypothesis`.

---

## Tasks

- [x] 1. Bootstrap: dependency and database model
  - [x] 1.1 Add `hypothesis` to `requirements.txt`
    - Append `hypothesis` (pinned to a recent stable version, e.g. `hypothesis==6.112.2`) to `requirements.txt`
    - _Requirements: (testing infrastructure — all property test requirements)_

  - [x] 1.2 Create `ChatbotSearchSession` model in `enquiry_bot/models.py`
    - Add the `ChatbotSearchSession` class with fields: `session_key` (CharField, max_length=40, db_index=True), `raw_query` (TextField), `extracted_keywords` (JSONField, default=list), `extracted_conditions` (JSONField, default=list), `report_text_summary` (TextField, blank=True), `created_at` (DateTimeField, auto_now_add=True), `updated_at` (DateTimeField, auto_now=True)
    - Add `class Meta: ordering = ["-updated_at"]` and `__str__` returning `f"Session {self.session_key}: {self.raw_query[:60]}"`
    - _Requirements: 3.3, 3.5_

  - [x] 1.3 Generate and apply migration for `ChatbotSearchSession`
    - Run `python manage.py makemigrations enquiry_bot` to create the migration file
    - Verify the migration file is created under `enquiry_bot/migrations/`
    - _Requirements: 3.3, 3.5_

- [x] 2. Core Python module: `enquiry_bot/smart_search.py`
  - [x] 2.1 Create module skeleton with `ReportParseError`, `MedicalIntent`, and `CONDITION_SPECIALIZATION_MAP`
    - Create `enquiry_bot/smart_search.py`
    - Define `class ReportParseError(Exception): pass`
    - Define `class MedicalIntent` as a dataclass or simple class with fields: `keywords: list[str]`, `conditions: list[str]`, `specializations: list[str]`, `raw_query: str`
    - Define `CONDITION_SPECIALIZATION_MAP` as a module-level dict constant exactly matching the design document (cardiac, orthopedic, neuro, oncology, endocrine, gastro, urology, ophthalmology, cosmetic, dental, fertility, general entries)
    - _Requirements: 2.1, 2.7, 12.3_

  - [x] 2.2 Implement `MedicalIntentExtractor` class
    - Add `class MedicalIntentExtractor` with a `extract(self, text: str) -> MedicalIntent` method
    - Normalize input: `text.lower().strip()`
    - Tokenize by splitting on whitespace and punctuation (use `re.split`)
    - Single-token matching loop: for each token, check `CONDITION_SPECIALIZATION_MAP` and append to `keywords`, `conditions`, `specializations`
    - Bigram matching loop: for consecutive token pairs, check bigram against map
    - Deduplicate all three lists while preserving order (use `dict.fromkeys`)
    - Fallback: if `keywords` is empty after matching, set `keywords = tokens[:5]`
    - Always set `raw_query = text` (original, un-normalized input)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

  - [x] 2.3 Write property tests for `MedicalIntentExtractor`
    - **Property 1: raw_query identity** — for any `text: str`, `MedicalIntentExtractor().extract(text).raw_query == text`
    - **Property 2: specializations subset** — for any `text: str`, all values in `extract(text).specializations` are present in the flat value set of `CONDITION_SPECIALIZATION_MAP`
    - **Validates: Requirements 2.5, 2.7**
    - Add to `enquiry_bot/tests_smart_search.py` using `@given(st.text())`

  - [x] 2.4 Implement `ReportParser` class
    - Add `class ReportParser` with `parse(self, uploaded_file) -> str` method
    - Branch on `uploaded_file.content_type`:
      - `application/pdf`: use `PyPDF2.PdfReader` to extract text from all pages; wrap in try/except and return `""` on any exception (satisfies Requirement 4.7)
      - `image/jpeg`, `image/png`, `image/gif`: return stub string `"[Image report uploaded — OCR not yet available]"`
      - `text/plain`: read and decode file bytes, return as string
      - Any other type: raise `ReportParseError(f"Unsupported file type: {uploaded_file.content_type}")`
    - Do not mutate `uploaded_file` (seek back to 0 after reading if needed)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [x] 2.5 Implement `PlaceholderRegistry` and `PLACEHOLDER_CATEGORIES`
    - Define `PLACEHOLDER_CATEGORIES` list constant with all 10 entries from the design: doctors, hospitals, treatments, blogs, pricing, feedbacks, videos, packages, hotels, insurance — each with `key`, `label`, `icon`, `url`
    - Add `class PlaceholderRegistry` with `get_placeholders(self, context_dict: dict) -> list[dict]` method
    - For each category in `PLACEHOLDER_CATEGORIES`, check if `context_dict.get(category["key"])` is truthy (non-empty queryset/list)
    - Return a list of dicts: each entry is the category definition merged with `has_data: bool` and `coming_soon: bool`
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [x] 2.6 Write property test for `PlaceholderRegistry`
    - **Property 4: placeholder count invariant** — for any `context_dict`, `len(PlaceholderRegistry().get_placeholders(context_dict)) == len(PLACEHOLDER_CATEGORIES)`
    - **Validates: Requirements 6.2**
    - Add to `enquiry_bot/tests_smart_search.py`

  - [x] 2.7 Implement `SmartResultsContext` dataclass
    - Define `class SmartResultsContext` (dataclass or plain class) with fields: `query_summary: str`, `doctors`, `hospitals`, `treatments`, `blogs`, `pricing_data: list`, `feedbacks`, `placeholders: list`, `intent: MedicalIntent`, `report_summary: str = ""`
    - _Requirements: 5.1–5.10_

  - [x] 2.8 Implement `SiteContentAggregator` class
    - Add `class SiteContentAggregator` with `aggregate(self, intent: MedicalIntent) -> SmartResultsContext` method
    - Import `Doctor`, `Hospital`, `Treatment`, `BlogPost`, `Feedback` from their respective apps
    - Build `text_q` from `intent.keywords` using `Q(name__icontains=kw)` ORed together; if keywords empty, use `Q()` (match all)
    - **Doctors**: build `spec_q` from `intent.specializations` using `Q(specialization__icontains=spec)`; combine with `text_q`; apply `select_related` and `prefetch_related('hospitals', 'treatments')`; `distinct()[:6]`
    - **Hospitals**: build `treatment_q` from keywords using `Q(treatments__name__icontains=kw)`; combine with `Q(name__icontains=raw_query) | Q(about__icontains=raw_query)`; `order_by('-rating')`; `select_related`; `prefetch_related('treatments', 'doctors')`; `distinct()[:6]`
    - **Treatments**: build `treat_q` from keywords using `Q(name__icontains=kw) | Q(description__icontains=kw)`; `distinct()[:6]`
    - **Blogs**: build `blog_q` from keywords using `Q(title__icontains=kw) | Q(content__icontains=kw)`; `distinct()[:4]`
    - **Feedbacks**: filter `is_approved=True` and `doctor__in=doctors` (if doctors non-empty); `distinct()[:4]`
    - **Pricing data**: build list of dicts `{treatment_name, hospital_name, price}` from matched treatments and hospitals that have `starting_price`
    - Call `PlaceholderRegistry().get_placeholders(...)` with the assembled context dict
    - Build `query_summary` string: `f"Showing results for: {', '.join(intent.keywords)}"` or a default prompt if keywords empty
    - Return `SmartResultsContext(...)`
    - _Requirements: 5.1–5.10, 12.1, 12.2_

  - [x] 2.9 Write property test for `SiteContentAggregator`
    - **Property 3: bounded results** — for any `MedicalIntent`, `len(list(aggregate(intent).doctors)) <= 6` (test with a real or in-memory SQLite test DB using `@pytest.mark.django_db`)
    - **Validates: Requirements 5.1, 12.1**
    - Add to `enquiry_bot/tests_smart_search.py`

- [x] 3. Checkpoint — verify module integrity
  - Import `smart_search` in a Django shell or test and confirm all classes instantiate without errors.
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Django views and URL routing
  - [x] 4.1 Implement `smart_results_view` in `enquiry_bot/views.py`
    - Add `smart_results_view(request)` function
    - **GET**: read `q` from `request.GET`, set `query_text = q`, `uploaded_file = None`
    - **POST**: read `query` from `request.POST`, `medical_report` from `request.FILES`
    - File size check: if `uploaded_file` and `uploaded_file.size > 10 * 1024 * 1024`, add warning and skip parsing (Requirement 4.8, 11.1)
    - Content-type validation before passing to `ReportParser` (Requirement 11.2)
    - Call `ReportParser().parse(uploaded_file)` inside try/except `ReportParseError`; on error set `report_summary = ""` and add warning message (Requirement 4.9)
    - Merge with `request.session.get('chatbot_context', [])` prior keywords
    - Call `MedicalIntentExtractor().extract(merged_text)`
    - Store `request.session['chatbot_context'] = intent.keywords` (Requirement 3.1)
    - `ChatbotSearchSession.objects.update_or_create(session_key=..., defaults={...})` (Requirement 3.3)
    - Wrap ORM aggregation in try/except `DatabaseError`; on error render page with all-placeholder context and log error (Requirement 8.1)
    - Call `SiteContentAggregator().aggregate(intent)`
    - Render `enquiry_bot/smart_results.html` with context dict including `results`, `query_text`, `report_summary`, `warnings`
    - _Requirements: 1.3, 1.4, 3.1, 3.2, 3.3, 3.4, 4.8, 4.9, 7.5, 8.1, 8.2, 8.5, 9.1, 9.2, 9.4, 11.1–11.5_

  - [x] 4.2 Implement `smart_results_api` in `enquiry_bot/views.py`
    - Add `smart_results_api(request)` function decorated with `@require_POST`
    - Parse `query` from `request.POST`
    - Run the same intent extraction + aggregation pipeline as `smart_results_view`
    - Return `JsonResponse` with serialized results (doctor names/slugs, hospital names/slugs, treatment names/slugs, blog titles/slugs, placeholder list)
    - Protect with CSRF (Django default for POST views)
    - _Requirements: 9.3_

  - [x] 4.3 Register new URLs in `enquiry_bot/urls.py`
    - Add `path('results/', views.smart_results_view, name='smart_results')` for GET and POST
    - Add `path('results/api/', views.smart_results_api, name='smart_results_api')` for POST
    - _Requirements: 9.1, 9.2, 9.3_

- [x] 5. Smart results template
  - [x] 5.1 Create `enquiry_bot/templates/enquiry_bot/smart_results.html`
    - Extend `base.html` (or the project's base template) to maintain site navigation and styling (Requirement 7.6)
    - **Search bar**: `<form method="POST" action="{% url 'enquiry_bot:smart_results' %}">` with `{% csrf_token %}`, text input named `query` pre-filled with `{{ query_text }}`, submit button (Requirement 7.1, 8.5)
    - **Report upload**: file input named `medical_report` with `enctype="multipart/form-data"` on the form (Requirement 7.2)
    - **Query summary banner**: display `{{ results.query_summary }}` or the default prompt when keywords are empty (Requirement 7.3, 7.5)
    - **Report summary card**: `{% if report_summary %}` block showing first 500 chars of extracted text — escape with `{{ report_summary|escape }}` (never raw HTML, Requirement 8.6, 7.4)
    - **Warning messages**: display any `warnings` list items (file parse errors, size errors)
    - **Results sections loop**: `{% for section in results.placeholders %}` — if `section.has_data`, render content cards; else render "Coming Soon" card with `section.icon` and `section.label` (Requirements 6.6, 6.7)
    - **Content cards**: for doctors show name, specialization, rating, profile picture link; for hospitals show name, city, rating; for treatments show name, category, starting price; for blogs show title, excerpt; for feedbacks show rating, comment excerpt
    - **"View All" links**: each section footer links to `section.url` (Requirement 12.4)
    - _Requirements: 6.5, 6.6, 6.7, 7.1–7.6, 8.5, 8.6, 12.4_

- [x] 6. Checkpoint — end-to-end view + template
  - Start the dev server locally and manually verify that `GET /enquiries/results/?q=diabetes` renders the page with sections.
  - Ensure all automated tests pass, ask the user if questions arise.

- [x] 7. Chatbot widget frontend integration
  - [x] 7.1 Modify `bot_interface.html` to intercept chatbot submissions
    - Locate the existing `#send-button` click handler and `#message-input` Enter key handler in `bot_interface.html`
    - Replace / wrap the handler: build a `<form>` dynamically (or use `FormData`) and POST to `/enquiries/results/` with field name `query`
    - If a file input exists in the widget, use `FormData` for multipart POST (Requirement 10.2)
    - Submit the form so the browser navigates to the results page (full-page navigation, not AJAX) (Requirement 10.1)
    - Guard: only intercept on pages that are NOT already `/enquiries/results/` so the results page's own form is unaffected (Requirement 10.4)
    - Attach handlers to `#send-button` click and `#message-input` keydown (Enter key) (Requirement 10.3)
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 8. Property-based and unit tests
  - [x] 8.1 Create `enquiry_bot/tests_smart_search.py` test file
    - Add `hypothesis` import and `pytest` imports
    - Add `@pytest.mark.django_db` marker where DB access is needed
    - _Requirements: (test infrastructure)_

  - [x] 8.2 Write property test — Property 1: raw_query identity
    - `@given(st.text())` — assert `MedicalIntentExtractor().extract(text).raw_query == text`
    - **Property 1: raw_query identity**
    - **Validates: Requirements 2.5**

  - [x] 8.3 Write property test — Property 2: specializations subset
    - `@given(st.text())` — assert all items in `extract(text).specializations` are in the flat value set of `CONDITION_SPECIALIZATION_MAP`
    - **Property 2: specializations subset**
    - **Validates: Requirements 2.7**

  - [x] 8.4 Write property test — Property 3: bounded doctor results
    - `@given(...)` with a strategy that builds a `MedicalIntent` — assert `len(list(SiteContentAggregator().aggregate(intent).doctors)) <= 6`
    - **Property 3: bounded results**
    - **Validates: Requirements 5.1, 12.1**

  - [x] 8.5 Write property test — Property 4: placeholder count invariant
    - `@given(st.fixed_dictionaries({...}))` — assert `len(PlaceholderRegistry().get_placeholders(ctx)) == len(PLACEHOLDER_CATEGORIES)`
    - **Property 4: placeholder count invariant**
    - **Validates: Requirements 6.2**

  - [x] 8.6 Write unit tests for `MedicalIntentExtractor`
    - Test with `"knee replacement"` → `specializations` contains `"Orthopedic Surgery"`
    - Test with `""` → `keywords == []`, `conditions == []`, `specializations == []`
    - Test with `"hello"` (no map match) → `keywords == ["hello"]` (fallback)
    - Test deduplication: repeated keyword appears once
    - Test bigram: `"blood pressure"` → matched as bigram
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6_

  - [x] 8.7 Write unit tests for `ReportParser`
    - Test PDF parsing with a minimal valid PDF bytes object
    - Test image stub: pass a mock file with `content_type="image/jpeg"` → returns non-None string
    - Test plain text: pass mock file with `content_type="text/plain"` → returns file content
    - Test unsupported type: `content_type="application/msword"` → raises `ReportParseError`
    - Test corrupted PDF: PyPDF2 raises exception → returns `""`
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.6, 4.7_

  - [x] 8.8 Write unit tests for `PlaceholderRegistry`
    - Test fully populated context → all entries have `has_data=True`
    - Test empty context → all entries have `coming_soon=True`
    - Test partial context → mixed `has_data` values
    - Test return length equals `len(PLACEHOLDER_CATEGORIES)`
    - _Requirements: 6.2, 6.3, 6.4_

  - [x] 8.9 Write integration test for `smart_results_view`
    - Use Django `TestClient` with `@pytest.mark.django_db`
    - POST `{"query": "knee replacement"}` → assert HTTP 200, response contains `"Showing results for"`
    - GET `?q=diabetes` → assert HTTP 200
    - POST with empty query → assert HTTP 200 (no 500 error)
    - POST with oversized file mock → assert warning message in response
    - _Requirements: 1.3, 1.4, 7.3, 7.5, 8.2, 11.1_

- [x] 9. Final checkpoint — full test suite
  - Run `python manage.py test enquiry_bot` (or `pytest enquiry_bot/`) and confirm all tests pass.
  - Ensure all tests pass, ask the user if questions arise.

---

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation before moving to the next phase
- Property tests validate universal correctness properties; unit tests validate specific examples and edge cases
- The `hypothesis` library must be installed (`pip install hypothesis==6.112.2`) before running property tests
- The `CONDITION_SPECIALIZATION_MAP` is intentionally a module-level constant — do not move it into a class or function
- All report text rendered in templates must use `|escape` (never `|safe`) to prevent XSS
