# Treatments Filter Bug — Bugfix Design

## Overview

The treatments page (`/treatments/`) has a sidebar filter form (Search, Hospital, Doctor) that updates the URL with query parameters but has no visible effect on the displayed treatments. The view (`treatments_home` in `treatments/views.py`) correctly builds a filtered `treatments` queryset from the GET parameters, but the template (`treatments/templates/treatments/home.html`) ignores it entirely — it iterates over `categories` and calls `category.treatments.all` inside the loop, fetching every treatment directly from the database. Additionally, the "No treatments found" empty-state message is gated on `{% if not categories %}`, which is always truthy because categories are fetched independently of any filter.

The fix is minimal and targeted:
1. In `treatments/views.py`, build a `categories_with_treatments` context variable — a list of `(category, filtered_treatments)` tuples derived from the already-filtered `treatments` queryset.
2. In `treatments/templates/treatments/home.html`, replace the `category.treatments.all` loop with iteration over `categories_with_treatments`, and update the empty-state guard to check `categories_with_treatments` instead of `categories`.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug — a filter parameter (search, hospital, or doctor) is present in the GET request, causing the view to build a filtered queryset that the template then ignores.
- **Property (P)**: The desired behavior when a filter is active — only treatments matching the filter criteria are displayed, grouped by category.
- **Preservation**: Existing behaviors that must remain unchanged by the fix — unfiltered page load, category-slug scoping, grouping under correct headings, filter value persistence in form inputs, and "Clear Filters" navigation.
- **`treatments_home`**: The view function in `treatments/views.py` that builds the filtered `treatments` queryset from GET parameters and renders `treatments/home.html`.
- **`categories_with_treatments`**: The new context variable — a list of `(TreatmentCategory, QuerySet[Treatment])` tuples — that groups the filtered treatments by category for the template to consume.
- **`category.treatments.all`**: The ORM reverse relation call in the original template that bypasses the filtered queryset and fetches all treatments for a category unconditionally.

## Bug Details

### Bug Condition

The bug manifests whenever any filter parameter (`search`, `hospital`, or `doctor`) is present in the GET request. The `treatments_home` view correctly filters the `treatments` queryset, but the template calls `category.treatments.all` inside the loop, which re-fetches all treatments for each category from the database, discarding the filtered queryset entirely. The empty-state message is also never shown because `{% if not categories %}` evaluates to false whenever any categories exist, regardless of whether any filtered treatments were found.

**Formal Specification:**
```
FUNCTION isBugCondition(request)
  INPUT: request of type HttpRequest
  OUTPUT: boolean

  has_filter := request.GET.get('search') != ''
             OR request.GET.get('hospital') != ''
             OR request.GET.get('doctor') != ''

  RETURN has_filter
         AND template_uses_category_treatments_all()
         -- i.e., the template ignores the filtered queryset
END FUNCTION
```

### Examples

- **Search filter active**: User searches "knee" → URL becomes `?search=knee` → view filters treatments to knee-related entries → template calls `category.treatments.all` → all treatments displayed. **Expected**: only treatments matching "knee" shown.
- **Hospital filter active**: User enters "Apollo" → URL becomes `?hospital=Apollo` → view filters to treatments at Apollo hospitals → template ignores filter → all treatments displayed. **Expected**: only treatments at Apollo hospitals shown.
- **Doctor filter active**: User enters "Dr. Sharma" → URL becomes `?doctor=Dr.+Sharma` → view filters to treatments by that doctor → template ignores filter → all treatments displayed. **Expected**: only treatments by Dr. Sharma shown.
- **No matching results**: User searches "xyznonexistent" → view returns empty queryset → template still shows all treatments; empty-state message never appears. **Expected**: "No treatments found" message displayed.

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- When no filters are applied, all treatments must continue to display grouped by category (requirement 3.1).
- When a category slug is provided in the URL, only treatments in that category must continue to display (requirement 3.2).
- When filters are applied and treatments are found, matching treatments must continue to be grouped under their correct category headings (requirement 3.3).
- Filter values entered by the user must continue to be preserved in the form inputs after the page reloads (requirement 3.4).
- Clicking "Clear Filters" must continue to navigate to `/treatments/` and display all treatments unfiltered (requirement 3.5).

**Scope:**
All requests that do NOT include a filter parameter (`search`, `hospital`, `doctor`) should be completely unaffected by this fix. This includes:
- Direct page loads with no query parameters
- Category-scoped URLs (e.g., `/treatments/cardiology/`)
- Any other GET parameters not related to filtering

## Hypothesized Root Cause

Based on the bug description and code inspection, the root cause is confirmed:

1. **Template bypasses the filtered queryset**: `home.html` uses `{% with cat_treatments=category.treatments.all %}` inside `{% for category in categories %}`. This ORM call is evaluated at render time and fetches all treatments for each category unconditionally, completely ignoring the `treatments` queryset passed in the context.

2. **Context variable mismatch**: The view passes a filtered `treatments` queryset in the context, but the template never references it for rendering treatment cards — it only uses `treatments|length` in the hero/stats section (which does reflect the filter) while the actual card rendering uses `category.treatments.all`.

3. **Incorrect empty-state guard**: The empty-state `{% if not categories %}` block checks whether any categories exist, not whether any filtered treatments exist. Since `categories` is always populated (it's fetched independently with `TreatmentCategory.objects.all()`), this block never renders.

4. **No grouping step in the view**: The view does not group the filtered `treatments` queryset by category before passing it to the template, leaving the template with no way to render filtered treatments per category without calling `.all()` itself.

## Correctness Properties

Property 1: Bug Condition — Filters Produce Filtered Results

_For any_ request where the bug condition holds (at least one of `search`, `hospital`, or `doctor` GET parameters is non-empty), the fixed `treatments_home` view SHALL render only the treatments that match the active filter criteria, grouped by their respective categories, and SHALL display the "No treatments found" message when no treatments match.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

Property 2: Preservation — Unfiltered and Scoped Requests Unchanged

_For any_ request where the bug condition does NOT hold (no filter parameters present, or only a category slug is provided), the fixed view SHALL produce exactly the same rendered output as the original view, preserving all treatments grouped by category, correct category headings, filter value persistence, and "Clear Filters" navigation.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Fix Implementation

### Changes Required

**File**: `treatments/views.py`

**Function**: `treatments_home`

**Specific Changes**:
1. **Build `categories_with_treatments`**: After the existing filter logic, group the filtered `treatments` queryset by category. Iterate over the filtered treatments and bucket them into a dict keyed by `treatment.category_id`, then build a list of `(category, treatments_list)` tuples preserving the original category ordering.
2. **Pass `categories_with_treatments` to the template**: Add `"categories_with_treatments": categories_with_treatments` to the `render` context dict. Keep `"categories"` in the context for the sidebar "Jump to Category" links and stats counters (they should still reflect all categories, not just filtered ones — or filtered ones, depending on desired UX; the minimal fix is to keep them as-is).

**File**: `treatments/templates/treatments/home.html`

**Function**: Template rendering loop

**Specific Changes**:
1. **Replace the outer loop**: Change `{% for category in categories %}` / `{% with cat_treatments=category.treatments.all %}` to `{% for category, cat_treatments in categories_with_treatments %}`.
2. **Remove the `{% with %}` / `{% endwith %}` tags**: They are no longer needed since `cat_treatments` comes directly from the loop variable.
3. **Fix the empty-state guard**: Change `{% if not categories %}` to `{% if not categories_with_treatments %}` so the "No treatments found" message appears when the filtered result set is empty.

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on the unfixed code to confirm the root cause, then verify the fix works correctly and preserves existing behavior.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm the root cause analysis. If refuted, re-hypothesize.

**Test Plan**: Write Django test-client tests that submit GET requests with filter parameters and assert that only matching treatments appear in the response. Run these tests on the UNFIXED code to observe failures and confirm the root cause.

**Test Cases**:
1. **Search filter test**: GET `/treatments/?search=<specific_treatment_name>` — assert only that treatment's card appears in the response (will fail on unfixed code).
2. **Hospital filter test**: GET `/treatments/?hospital=<specific_hospital_name>` — assert only treatments at that hospital appear (will fail on unfixed code).
3. **Doctor filter test**: GET `/treatments/?doctor=<specific_doctor_name>` — assert only treatments by that doctor appear (will fail on unfixed code).
4. **No-match empty-state test**: GET `/treatments/?search=xyznonexistent` — assert the "No treatments found" message appears and no treatment cards are rendered (will fail on unfixed code).

**Expected Counterexamples**:
- All treatments continue to appear in the response despite active filters.
- The "No treatments found" message never appears even when no treatments match.
- Root cause confirmed: template calls `category.treatments.all` instead of using the filtered queryset.

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed view produces the expected behavior.

**Pseudocode:**
```
FOR ALL request WHERE isBugCondition(request) DO
  response := treatments_home_fixed(request)
  ASSERT only_matching_treatments_displayed(response, request.GET)
  IF no_treatments_match(request.GET) THEN
    ASSERT "No treatments found" IN response.content
  END IF
END FOR
```

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed view produces the same rendered output as the original view.

**Pseudocode:**
```
FOR ALL request WHERE NOT isBugCondition(request) DO
  ASSERT treatments_home_original(request) == treatments_home_fixed(request)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across the input domain (random category slugs, random absent-filter requests).
- It catches edge cases that manual unit tests might miss.
- It provides strong guarantees that behavior is unchanged for all non-buggy inputs.

**Test Plan**: Observe behavior on UNFIXED code for unfiltered requests, then write property-based tests capturing that behavior.

**Test Cases**:
1. **No-filter preservation**: GET `/treatments/` with no query params — assert all treatments and all categories appear, same as before the fix.
2. **Category-slug preservation**: GET `/treatments/<slug>/` — assert only treatments in that category appear, same as before the fix.
3. **Filter value persistence**: Submit filter form, reload — assert form inputs retain the submitted values.
4. **Clear Filters navigation**: Assert the "Clear Filters" link points to `/treatments/`.

### Unit Tests

- Test that `categories_with_treatments` contains only categories that have at least one matching treatment when a filter is active.
- Test that `categories_with_treatments` contains all categories (with all their treatments) when no filter is active.
- Test that the empty-state message renders when `categories_with_treatments` is empty.
- Test edge cases: filter matching treatments in multiple categories, filter matching no treatments, category-slug scope combined with a filter.

### Property-Based Tests

- Generate random search strings and verify that only treatments whose names contain the string (case-insensitive) appear in the response.
- Generate random sets of treatments and verify that the grouping by category is always correct regardless of which treatments match the filter.
- Generate random non-filter requests and verify that the response is identical to the pre-fix baseline (preservation property).

### Integration Tests

- Full page load with each filter type applied — verify correct treatments displayed and URL params preserved in form inputs.
- Full page load with no filters — verify all treatments displayed grouped by category.
- Full page load with a filter that matches nothing — verify "No treatments found" message and no treatment cards.
- Category-slug URL with and without additional filters — verify correct scoping behavior.
