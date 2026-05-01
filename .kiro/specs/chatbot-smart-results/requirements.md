# Requirements Document

## Introduction

The Chatbot Smart Results feature transforms the existing TakeOpinion enquiry bot into a smart, context-aware assistant. When a user submits a query or uploads a medical report in the chatbot widget, the browser navigates to a dedicated `/enquiries/results/` page that displays all relevant website content — doctors, hospitals, treatments, blogs, pricing, and patient reviews — organized in categorized sections. Categories with no matching data show a "Coming Soon" placeholder so the page always presents a complete, extensible layout. Follow-up queries remain on the results page, and session context is preserved so subsequent searches can be merged with prior intent.

---

## Glossary

- **SmartResultsView**: The Django view at `/enquiries/results/` that orchestrates the full search pipeline and renders the results page.
- **MedicalIntentExtractor**: The component that parses free text or extracted report text into a structured `MedicalIntent` object.
- **MedicalIntent**: A data structure containing extracted keywords, detected medical conditions, matched doctor specializations, and the original raw query.
- **SiteContentAggregator**: The component that queries all content models using a `MedicalIntent` and returns a unified `SmartResultsContext`.
- **SmartResultsContext**: A data structure holding all aggregated query results (doctors, hospitals, treatments, blogs, pricing, feedbacks, placeholders, and intent).
- **ReportParser**: The component that extracts plain text from uploaded medical report files (PDF, images, plain text).
- **PlaceholderRegistry**: The component that defines all content categories the results page must always show, marking empty ones as "Coming Soon".
- **PLACEHOLDER_CATEGORIES**: The Python list of content category definitions used by `PlaceholderRegistry`.
- **CONDITION_SPECIALIZATION_MAP**: The Python dictionary mapping medical keywords and bigrams to doctor specialization strings.
- **ChatbotSearchSession**: The Django model that stores extracted intent per session key for follow-up query context merging.
- **Chatbot_Widget**: The existing JavaScript chatbot widget embedded on site pages that intercepts user submissions and redirects to the results page.
- **ReportParseError**: The exception raised by `ReportParser` when an unsupported file format is submitted.
- **Session**: A Django server-side session identified by `session_key`, used to store `chatbot_context` between requests.

---

## Requirements

### Requirement 1: Smart Results Page Navigation

**User Story:** As a user, I want to be taken to a dedicated results page when I submit a query or upload a report in the chatbot, so that I can see all relevant medical content in one organized view.

#### Acceptance Criteria

1. WHEN a user submits a text query in the Chatbot_Widget, THE Chatbot_Widget SHALL perform a POST request to `/enquiries/results/` with the query text and navigate the browser to that URL.
2. WHEN a user uploads a medical report file in the Chatbot_Widget, THE Chatbot_Widget SHALL perform a multipart POST request to `/enquiries/results/` with the file and navigate the browser to that URL.
3. WHEN a GET request is made to `/enquiries/results/` with a `q` query parameter, THE SmartResultsView SHALL render the results page pre-filled with the query value.
4. THE SmartResultsView SHALL accept both GET and POST requests at `/enquiries/results/`.
5. WHEN a user submits a follow-up query on the results page, THE SmartResultsView SHALL process the new query on the same `/enquiries/results/` URL without navigating away.

---

### Requirement 2: Medical Intent Extraction

**User Story:** As a user, I want the system to understand the medical meaning of my query, so that I receive results relevant to my condition or treatment interest.

#### Acceptance Criteria

1. WHEN `MedicalIntentExtractor.extract` is called with a non-empty text string, THE MedicalIntentExtractor SHALL tokenize the text, match tokens against `CONDITION_SPECIALIZATION_MAP`, and return a `MedicalIntent` with populated `keywords`, `conditions`, and `specializations` fields.
2. WHEN `MedicalIntentExtractor.extract` is called with a text string, THE MedicalIntentExtractor SHALL check all consecutive two-token bigrams against `CONDITION_SPECIALIZATION_MAP` in addition to single tokens.
3. WHEN `MedicalIntentExtractor.extract` is called with a text string that matches no entries in `CONDITION_SPECIALIZATION_MAP`, THE MedicalIntentExtractor SHALL populate `keywords` with up to the first five raw tokens as a fallback.
4. WHEN `MedicalIntentExtractor.extract` is called with an empty string, THE MedicalIntentExtractor SHALL return a `MedicalIntent` with empty `keywords`, `conditions`, and `specializations` lists and `raw_query` set to the empty string.
5. THE MedicalIntentExtractor SHALL return a `MedicalIntent` where `raw_query` equals the original input text passed to `extract`.
6. THE MedicalIntentExtractor SHALL deduplicate `keywords`, `conditions`, and `specializations` so that no value appears more than once in each list.
7. THE MedicalIntentExtractor SHALL only include values in `specializations` that exist as values in `CONDITION_SPECIALIZATION_MAP`.

---

### Requirement 3: Session-Based Query Context

**User Story:** As a user, I want my follow-up queries to be aware of my previous search, so that I can refine results without repeating my full medical context.

#### Acceptance Criteria

1. WHEN `SmartResultsView` processes a query, THE SmartResultsView SHALL store the extracted `keywords` from the resulting `MedicalIntent` in `request.session['chatbot_context']`.
2. WHEN `SmartResultsView` processes a follow-up query and `request.session['chatbot_context']` contains prior keywords, THE SmartResultsView SHALL merge the prior keywords with the new query text before passing it to `MedicalIntentExtractor`.
3. WHEN `SmartResultsView` processes a query, THE SmartResultsView SHALL create or update a `ChatbotSearchSession` record keyed by `request.session.session_key` with the raw query, extracted keywords, and extracted conditions.
4. IF `request.session` is unavailable or `chatbot_context` is absent, THEN THE SmartResultsView SHALL proceed with the current query only, without raising an exception.
5. THE ChatbotSearchSession SHALL store `session_key`, `raw_query`, `extracted_keywords`, `extracted_conditions`, `report_text_summary`, `created_at`, and `updated_at` fields.
6. THE SmartResultsView SHALL ensure that `chatbot_context` stored in the Session is scoped to the individual session key so that different users' sessions never share extracted keywords.

---

### Requirement 4: Medical Report Parsing

**User Story:** As a user, I want to upload a medical report PDF or image and have the system extract its content, so that I receive results relevant to my diagnosis without manually typing it.

#### Acceptance Criteria

1. WHEN `ReportParser.parse` is called with a PDF file (`application/pdf`), THE ReportParser SHALL extract and return the text content of the PDF using PyPDF2.
2. WHEN `ReportParser.parse` is called with an image file (`image/jpeg`, `image/png`, or `image/gif`), THE ReportParser SHALL return a non-null string (stub implementation acceptable; OCR may be added later).
3. WHEN `ReportParser.parse` is called with a plain text file (`text/plain`), THE ReportParser SHALL return the file's text content directly.
4. WHEN `ReportParser.parse` is called with an unsupported file type, THE ReportParser SHALL raise `ReportParseError`.
5. THE ReportParser SHALL not mutate the `uploaded_file` object passed to `parse`.
6. THE ReportParser SHALL return a non-None string for all supported file types (the string may be empty if extraction yields no text).
7. WHEN a PDF is corrupted or password-protected and PyPDF2 raises an exception, THE ReportParser SHALL catch the exception and return an empty string.
8. WHEN `SmartResultsView` receives a file upload, THE SmartResultsView SHALL validate that the file size does not exceed 10 MB before passing it to `ReportParser`.
9. WHEN `SmartResultsView` catches a `ReportParseError`, THE SmartResultsView SHALL set `report_summary` to an empty string, continue processing any typed query text, and include a warning message in the response: "We couldn't read your file format. Please upload PDF, JPG, or PNG."

---

### Requirement 5: Site Content Aggregation

**User Story:** As a user, I want to see all types of relevant medical content — doctors, hospitals, treatments, articles, pricing, and reviews — in response to my query, so that I can make an informed decision.

#### Acceptance Criteria

1. WHEN `SiteContentAggregator.aggregate` is called with a `MedicalIntent`, THE SiteContentAggregator SHALL query the `Doctor` model filtering by specialization match and keyword match and return at most 6 distinct `Doctor` objects.
2. WHEN `SiteContentAggregator.aggregate` is called with a `MedicalIntent`, THE SiteContentAggregator SHALL query the `Hospital` model filtering by associated treatment names and raw query match, order results by descending rating, and return at most 6 distinct `Hospital` objects.
3. WHEN `SiteContentAggregator.aggregate` is called with a `MedicalIntent`, THE SiteContentAggregator SHALL query the `Treatment` model filtering by name and description keyword match and return at most 6 distinct `Treatment` objects.
4. WHEN `SiteContentAggregator.aggregate` is called with a `MedicalIntent`, THE SiteContentAggregator SHALL query the `BlogPost` model filtering by title and content keyword match and return at most 4 distinct `BlogPost` objects.
5. WHEN `SiteContentAggregator.aggregate` is called with a `MedicalIntent`, THE SiteContentAggregator SHALL query approved `Feedback` objects associated with matched doctors and return at most 4 distinct `Feedback` objects.
6. WHEN `SiteContentAggregator.aggregate` is called with a `MedicalIntent` whose `keywords` list is empty, THE SiteContentAggregator SHALL apply a broad filter that matches all records, ensuring the results page is never completely empty when the database has content.
7. THE SiteContentAggregator SHALL use Django `Q` objects for all ORM filters and SHALL NOT use raw SQL queries.
8. THE SiteContentAggregator SHALL call `distinct()` on all QuerySets that involve many-to-many joins to prevent duplicate objects in results.
9. THE SiteContentAggregator SHALL use `select_related` and `prefetch_related` on `Doctor` (hospitals, treatments) and `Hospital` (treatments, doctors) queries to avoid N+1 database queries.
10. THE SiteContentAggregator SHALL return a `SmartResultsContext` that includes `pricing_data` as a list of dicts containing treatment name, hospital name, and price, derived from matched treatments and hospitals.

---

### Requirement 6: Placeholder Registry and Always-Present Sections

**User Story:** As a user, I want to see all content categories on the results page even when some have no matching data, so that I know what types of information are available on the platform.

#### Acceptance Criteria

1. THE PlaceholderRegistry SHALL define all content categories in `PLACEHOLDER_CATEGORIES`, including at minimum: doctors, hospitals, treatments, blogs, pricing, feedbacks, videos, packages, hotels, and insurance.
2. WHEN `PlaceholderRegistry.get_placeholders` is called with a `SmartResultsContext`, THE PlaceholderRegistry SHALL return a list with exactly `len(PLACEHOLDER_CATEGORIES)` entries.
3. WHEN a category key in `PLACEHOLDER_CATEGORIES` has no matching results in the context, THE PlaceholderRegistry SHALL mark that entry with `has_data=False` and `coming_soon=True`.
4. WHEN a category key in `PLACEHOLDER_CATEGORIES` has one or more matching results in the context, THE PlaceholderRegistry SHALL mark that entry with `has_data=True` and `coming_soon=False`.
5. WHEN a new entry is added to `PLACEHOLDER_CATEGORIES` and its corresponding database model is populated, THE SmartResultsView SHALL render the new category section on the results page without requiring any template changes.
6. THE smart_results.html template SHALL render a section for every entry in the `placeholders` list passed in the template context.
7. WHEN a section has `coming_soon=True`, THE smart_results.html template SHALL render a styled "Coming Soon" card displaying the category icon and label.

---

### Requirement 7: Smart Results Page Rendering

**User Story:** As a user, I want the results page to clearly display my query context and all matched content in organized sections, so that I can quickly find what I need.

#### Acceptance Criteria

1. THE smart_results.html template SHALL display a search bar pre-filled with the current query that POSTs to `/enquiries/results/` on submission.
2. THE smart_results.html template SHALL display a report upload button allowing users to submit a new file from the results page.
3. THE smart_results.html template SHALL display a query summary banner showing the terms the results are based on (e.g., "Showing results for: knee replacement").
4. WHEN a medical report was uploaded in the current request, THE smart_results.html template SHALL display a report summary card showing the first 500 characters of the extracted report text.
5. WHEN `SmartResultsView` processes an empty query with no file and the database has content, THE SmartResultsView SHALL return a results page showing top-rated content across all categories and a prompt: "Try searching for a condition, treatment, or doctor name."
6. THE smart_results.html template SHALL extend the site's base template and maintain consistent site navigation and styling.

---

### Requirement 8: Error Handling and Resilience

**User Story:** As a user, I want the results page to always load gracefully even when something goes wrong, so that I am never shown a broken page.

#### Acceptance Criteria

1. WHEN a database query raises a `DatabaseError` during aggregation, THE SmartResultsView SHALL catch the exception, log it, and render the results page with all sections displayed as "Coming Soon" placeholders.
2. WHEN `SmartResultsView` processes a request with no query text and no uploaded file, THE SmartResultsView SHALL return HTTP 200 and render the results page with general top-rated content rather than an error response.
3. IF a PDF parsing exception occurs inside `ReportParser`, THEN THE ReportParser SHALL catch the exception and return an empty string without propagating the exception to `SmartResultsView`.
4. IF an unsupported file type is uploaded, THEN THE SmartResultsView SHALL display the warning "We couldn't read your file format. Please upload PDF, JPG, or PNG." and continue processing any typed query text.
5. THE SmartResultsView SHALL protect all POST endpoints with Django CSRF token validation.
6. THE SmartResultsView SHALL treat all text extracted from uploaded files as untrusted input and SHALL only use it as search keywords, never rendering it as raw HTML.

---

### Requirement 9: URL Structure and Routing

**User Story:** As a developer, I want the smart results feature to be accessible via well-defined URLs, so that the feature integrates cleanly with the existing URL configuration.

#### Acceptance Criteria

1. THE enquiry_bot URL configuration SHALL register `GET /enquiries/results/` mapped to `SmartResultsView`.
2. THE enquiry_bot URL configuration SHALL register `POST /enquiries/results/` mapped to `SmartResultsView`.
3. THE enquiry_bot URL configuration SHALL register `POST /enquiries/results/api/` mapped to `smart_results_api` for AJAX follow-up queries returning JSON.
4. WHEN `SmartResultsView` is accessed via GET with a `q` parameter, THE SmartResultsView SHALL produce a shareable link that renders the same results as a POST with the equivalent query.

---

### Requirement 10: Chatbot Widget Integration

**User Story:** As a developer, I want the existing chatbot widget to redirect the first submission to the smart results page, so that users are seamlessly transitioned to the richer results experience.

#### Acceptance Criteria

1. WHEN a user clicks the send button or presses Enter in the chatbot message input on any page, THE Chatbot_Widget SHALL intercept the submission and POST the query to `/enquiries/results/` instead of responding inline.
2. WHEN a user attaches a file in the Chatbot_Widget before submitting, THE Chatbot_Widget SHALL use `FormData` for a multipart POST to `/enquiries/results/`.
3. THE Chatbot_Widget SHALL attach its submit handler to the existing `#send-button` click event and `#message-input` Enter key event in `bot_interface.html`.
4. WHEN the browser has navigated to `/enquiries/results/`, all subsequent query submissions SHALL be handled by the results page's own search form rather than the Chatbot_Widget.

---

### Requirement 11: Security and Data Handling

**User Story:** As a system operator, I want all file uploads and search queries to be handled securely, so that the platform is protected from injection attacks and data leaks.

#### Acceptance Criteria

1. THE SmartResultsView SHALL reject uploaded files larger than 10 MB and return an appropriate error message.
2. THE SmartResultsView SHALL validate the content type of uploaded files before passing them to `ReportParser`.
3. THE SmartResultsView SHALL read uploaded files into memory for parsing and SHALL NOT persist them to disk unless explicitly saved to the `MedicalReport` model.
4. THE SmartResultsView SHALL use only Django ORM parameterized `Q` object filters for all database queries and SHALL NOT construct raw SQL strings.
5. THE SmartResultsView SHALL not expose session keywords in the results page URL; keywords SHALL be stored server-side in the Session only.

---

### Requirement 12: Performance and Scalability

**User Story:** As a system operator, I want the results page to load efficiently even as the database grows, so that users experience acceptable response times.

#### Acceptance Criteria

1. THE SiteContentAggregator SHALL limit all content category result sets to their defined maximums (doctors: 6, hospitals: 6, treatments: 6, blogs: 4, feedbacks: 4) using ORM slice notation.
2. THE SiteContentAggregator SHALL apply `select_related` and `prefetch_related` on Doctor and Hospital queries to prevent N+1 query patterns.
3. THE CONDITION_SPECIALIZATION_MAP SHALL be defined as a module-level constant so that it is loaded once at application startup and does not require a database query on each request.
4. THE smart_results.html template SHALL include a "View All" link per content section pointing to the corresponding existing list page (e.g., `/doctors/`, `/hospitals/`, `/treatments/`, `/blogs/`) rather than paginating inline.
