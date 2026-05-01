# Requirements Document

## Introduction

The TakeOpinion platform has two user-facing search/chat surfaces: a floating chatbot widget (present on every page via `base.html`) and a dedicated Smart Results page (`/enquiries/results/`). Both surfaces share the same backend intent-extraction and content-aggregation pipeline (`enquiry_bot/smart_search.py`), but they are currently disconnected and broken in several ways:

1. A stray JavaScript block outside a `</script>` tag in `base.html` causes a syntax error on every page.
2. The floating chatbot uses an unreliable `fetch`-then-redirect pattern instead of a direct form POST.
3. The Smart Results page reloads fully on every follow-up query even though a JSON API endpoint (`/enquiries/results/api/`) already exists.
4. The chatbot on the results page calls the old text-only `chat_message_api` instead of the smart-search API, so results are never updated in-place.
5. No loading/spinner feedback is shown while a search is in progress.
6. Session context accumulates fallback tokens (raw words) alongside real medical conditions, polluting follow-up queries.

This spec covers the fixes and enhancements needed to make both surfaces work correctly and in real-time.

---

## Glossary

- **Floating_Chatbot**: The fixed-position chat widget rendered in `base.html` that appears on every page of the site.
- **Smart_Results_Page**: The Django view and template at `/enquiries/results/` that displays doctors, hospitals, treatments, blogs, pricing, and feedback cards.
- **Smart_Results_API**: The JSON endpoint at `/enquiries/results/api/` (`smart_results_api` view) that accepts a POST with `query` and returns structured results as JSON.
- **Intent_Extractor**: The `MedicalIntentExtractor` class in `smart_search.py` that maps free text to medical conditions and specializations.
- **Session_Context**: The server-side Django session data used to accumulate medical conditions across follow-up queries within a single user session.
- **Conditions**: Map-matched medical keywords produced by `Intent_Extractor` (stored in `intent.conditions`).
- **Fallback_Tokens**: Raw word tokens produced by `Intent_Extractor` when no map match is found (stored only in `intent.keywords`, not in `intent.conditions`).
- **Spinner**: A visible loading indicator shown to the user while an asynchronous search request is in flight.
- **CSRF_Token**: The Django cross-site request forgery token required on all POST requests.

---

## Requirements

### Requirement 1: Fix Broken JavaScript in base.html

**User Story:** As a site visitor, I want every page to load without JavaScript errors, so that the navigation, dropdowns, and chatbot widget all function correctly.

#### Acceptance Criteria

1. THE `base.html` template SHALL contain exactly one closing `</script>` tag for the floating chatbot script block, with no JavaScript code appearing after that closing tag and before the `</body>` tag outside of a valid `<script>` element.
2. WHEN a browser parses `base.html`, THE Browser SHALL report zero JavaScript syntax errors originating from the floating chatbot script block.
3. THE dropdown submenu initialization code SHALL be placed inside a valid `<script>` element so that it executes correctly.

---

### Requirement 2: Fix Floating Chatbot Form Submission

**User Story:** As a user on any page, I want to type a query into the floating chatbot and be taken to the Smart Results page with my results, so that I can find relevant doctors, hospitals, and treatments without the redirect failing silently.

#### Acceptance Criteria

1. WHEN a user submits a query via the Floating_Chatbot on any non-results page, THE Floating_Chatbot SHALL submit the query using a direct HTML form POST to `/enquiries/results/` rather than using `fetch` with redirect-following.
2. WHEN the form POST is submitted, THE Browser SHALL navigate to the Smart_Results_Page and display results for the submitted query.
3. WHEN a user attaches a medical report file in the Floating_Chatbot before submitting, THE Floating_Chatbot SHALL include the file in the form POST using `enctype="multipart/form-data"`.
4. THE Floating_Chatbot form submission SHALL include a valid CSRF_Token in the POST body.
5. IF the query field is empty and no file is attached, THEN THE Floating_Chatbot SHALL NOT submit the form.

---

### Requirement 3: Real-Time AJAX Search on Smart Results Page

**User Story:** As a user on the Smart Results page, I want to submit a follow-up query and see updated results appear in-place without a full page reload, so that my search experience feels fast and continuous.

#### Acceptance Criteria

1. WHEN a user submits the search form on the Smart_Results_Page, THE Smart_Results_Page SHALL send the query to Smart_Results_API via an AJAX POST request instead of performing a full page reload.
2. WHEN the Smart_Results_API returns a successful JSON response, THE Smart_Results_Page SHALL update the doctors, hospitals, treatments, blogs, pricing, and feedback sections in-place without reloading the page.
3. WHEN the Smart_Results_API returns a successful JSON response, THE Smart_Results_Page SHALL update the query summary strip to reflect the new search.
4. IF the Smart_Results_API returns an error response, THEN THE Smart_Results_Page SHALL display a user-visible error message without losing the previously displayed results.
5. THE Smart_Results_Page AJAX request SHALL include a valid CSRF_Token in the POST headers or body.
6. WHEN a medical report file is attached to the search form on the Smart_Results_Page, THE Smart_Results_Page SHALL include the file in the AJAX POST using `FormData`.

---

### Requirement 4: Chatbot on Results Page Uses Smart Search API

**User Story:** As a user on the Smart Results page, I want the chatbot's send button to trigger a smart search and update the results sections, so that I can refine my search through the chat interface without leaving the page.

#### Acceptance Criteria

1. WHEN a user sends a message via the chatbot interface while on the Smart_Results_Page, THE Smart_Results_Page SHALL POST the message to Smart_Results_API instead of to `chat_message_api`.
2. WHEN the Smart_Results_API returns results, THE Smart_Results_Page SHALL update all result sections (doctors, hospitals, treatments, blogs, pricing, feedbacks) in-place with the new data.
3. WHEN a user sends a message via the chatbot on the Smart_Results_Page, THE Smart_Results_Page SHALL display the user's message in the chat window as a sent message bubble.
4. WHEN the Smart_Results_API returns a `query_summary`, THE Smart_Results_Page SHALL display it as a bot response bubble in the chat window.
5. IF the Smart_Results_API returns an error, THEN THE Smart_Results_Page SHALL display an error message bubble in the chat window.

---

### Requirement 5: Loading Spinner During Search

**User Story:** As a user, I want to see a visual loading indicator whenever a search is in progress, so that I know the system is working and I do not submit duplicate requests.

#### Acceptance Criteria

1. WHEN an AJAX search request is initiated on the Smart_Results_Page, THE Smart_Results_Page SHALL display a Spinner overlay or inline loading indicator within the results area.
2. WHILE a search request is in flight, THE Smart_Results_Page SHALL disable the search submit button to prevent duplicate submissions.
3. WHEN the search request completes (success or error), THE Smart_Results_Page SHALL hide the Spinner and re-enable the submit button.
4. WHEN the Floating_Chatbot is submitting a query via form POST, THE Floating_Chatbot SHALL disable the send button and show a visual loading state until the form submission navigates away.

---

### Requirement 6: Fix Session Context Accumulation Bug

**User Story:** As a user making follow-up queries, I want my search context to accumulate only real medical conditions, so that unrelated words from earlier queries do not pollute my results.

#### Acceptance Criteria

1. WHEN the Smart_Results_API stores search context in Session_Context, THE Smart_Results_API SHALL store only `intent.conditions` (map-matched keywords) and SHALL NOT store `intent.keywords` when those keywords are Fallback_Tokens.
2. WHEN a follow-up query is processed and Session_Context contains prior Conditions, THE Intent_Extractor SHALL merge the prior Conditions with the new query's Conditions to produce a combined intent.
3. WHEN a follow-up query produces no new Conditions (only Fallback_Tokens), THE Smart_Results_API SHALL use only the prior Session_Context Conditions for content aggregation and SHALL NOT add the Fallback_Tokens to Session_Context.
4. WHEN a user starts a new session or clears their session, THE Session_Context SHALL be empty and no prior Conditions SHALL influence the new query.
5. FOR ALL sequences of queries where at least one query contains a valid medical Condition, the Session_Context SHALL contain only Conditions that appeared in `intent.conditions` of at least one query in the sequence, never raw Fallback_Tokens.
