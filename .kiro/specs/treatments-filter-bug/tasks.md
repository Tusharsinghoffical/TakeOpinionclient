# Treatments Filter Bug — Tasks

## Task List

- [x] 1. Write exploratory tests (bug condition checking on unfixed code)
  - [x] 1.1 Create test file `treatments/tests_filter_bug.py` with Django test-client setup and fixtures (at least one treatment per category, linked to a hospital and a doctor)
  - [x] 1.2 Write test: GET `/treatments/?search=<name>` asserts only matching treatment cards appear — run on unfixed code to confirm failure
  - [x] 1.3 Write test: GET `/treatments/?hospital=<name>` asserts only treatments at that hospital appear — run on unfixed code to confirm failure
  - [x] 1.4 Write test: GET `/treatments/?doctor=<name>` asserts only treatments by that doctor appear — run on unfixed code to confirm failure
  - [x] 1.5 Write test: GET `/treatments/?search=xyznonexistent` asserts "No treatments found" message appears and no treatment cards are rendered — run on unfixed code to confirm failure

- [x] 2. Fix `treatments/views.py` — build `categories_with_treatments` context variable
  - [x] 2.1 After the existing filter/distinct logic in `treatments_home`, group the filtered `treatments` queryset by category: iterate over `treatments`, bucket by `treatment.category_id`, then build a list of `(category, treatments_list)` tuples preserving the original `categories` ordering
  - [x] 2.2 Add `"categories_with_treatments": categories_with_treatments` to the `render` context dict (keep existing `"categories"` for sidebar jump-links and stats counters)

- [x] 3. Fix `treatments/templates/treatments/home.html` — use `categories_with_treatments`
  - [x] 3.1 Replace `{% for category in categories %}` / `{% with cat_treatments=category.treatments.all %}` with `{% for category, cat_treatments in categories_with_treatments %}`
  - [x] 3.2 Remove the `{% endwith %}` tag that is no longer needed
  - [x] 3.3 Change the empty-state guard from `{% if not categories %}` to `{% if not categories_with_treatments %}`

- [x] 4. Verify fix checking — run exploratory tests against fixed code
  - [x] 4.1 Run the tests from task 1 against the fixed code and confirm all four tests now pass (search, hospital, doctor filters, and empty-state message)

- [x] 5. Write and run preservation tests (regression prevention)
  - [x] 5.1 Write test: GET `/treatments/` with no query params — assert all treatments and all categories appear (requirement 3.1)
  - [x] 5.2 Write test: GET `/treatments/<category_slug>/` — assert only treatments in that category appear (requirement 3.2)
  - [x] 5.3 Write test: filter returning results — assert matching treatments are grouped under correct category headings (requirement 3.3)
  - [x] 5.4 Write test: submit filter form — assert form inputs retain submitted values in the rendered response (requirement 3.4)
  - [x] 5.5 Write test: assert the "Clear Filters" anchor href is `/treatments/` (requirement 3.5)
  - [x] 5.6 Run all preservation tests and confirm they pass

- [x] 6. Run the full test suite and confirm no regressions
  - [x] 6.1 Run `python manage.py test treatments` and confirm all tests pass with no errors
