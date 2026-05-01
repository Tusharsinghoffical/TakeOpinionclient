# Bugfix Requirements Document

## Introduction

On the treatments page (`/treatments/`), the sidebar filter form accepts Search (treatment name), Hospital, and Doctor inputs. When the user submits the form, the URL updates correctly with query parameters, but the displayed treatments do not change — all treatments continue to appear regardless of the filter values entered.

The root cause is a template-level bypass: `treatments/templates/treatments/home.html` iterates over `categories` and calls `category.treatments.all` inside the template, which fetches all treatments for each category directly from the database. This completely ignores the filtered `treatments` queryset that `treatments_home` in `treatments/views.py` correctly builds from the GET parameters. Additionally, the "No treatments found" message is never shown because it is gated on `{% if not categories %}`, which is always truthy since categories are fetched independently of any filter.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN the user submits the filter form with a search term THEN the system displays all treatments for every category, ignoring the search term

1.2 WHEN the user submits the filter form with a hospital name THEN the system displays all treatments for every category, ignoring the hospital filter

1.3 WHEN the user submits the filter form with a doctor name THEN the system displays all treatments for every category, ignoring the doctor filter

1.4 WHEN the user applies filters that match no treatments THEN the system still displays all treatments and never shows the "No treatments found" message

### Expected Behavior (Correct)

2.1 WHEN the user submits the filter form with a search term THEN the system SHALL display only treatments whose names match the search term, grouped by their respective categories

2.2 WHEN the user submits the filter form with a hospital name THEN the system SHALL display only treatments associated with hospitals matching that name, grouped by their respective categories

2.3 WHEN the user submits the filter form with a doctor name THEN the system SHALL display only treatments associated with doctors matching that name, grouped by their respective categories

2.4 WHEN the user applies filters that match no treatments THEN the system SHALL display the "No treatments found" message instead of any treatment cards

### Unchanged Behavior (Regression Prevention)

3.1 WHEN no filters are applied THEN the system SHALL CONTINUE TO display all treatments grouped by category

3.2 WHEN a category slug is provided in the URL THEN the system SHALL CONTINUE TO display only treatments belonging to that category

3.3 WHEN filters are applied and treatments are found THEN the system SHALL CONTINUE TO group the matching treatments under their correct category headings

3.4 WHEN filters are applied THEN the system SHALL CONTINUE TO preserve the entered filter values in the form inputs after the page reloads

3.5 WHEN the user clicks "Clear Filters" THEN the system SHALL CONTINUE TO navigate to `/treatments/` and display all treatments unfiltered
