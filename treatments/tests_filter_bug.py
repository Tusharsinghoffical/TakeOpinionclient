"""
Bug condition exploration tests for the treatments filter bug.

These tests are EXPECTED TO FAIL on the unfixed code. Failure confirms the bug exists.

Bug: treatments/templates/treatments/home.html calls `category.treatments.all` inside
the template loop, ignoring the filtered `treatments` queryset that `treatments_home`
in treatments/views.py correctly builds from GET parameters. The empty-state message
is gated on `{% if not categories %}` which is always truthy.
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse

from treatments.models import Treatment, TreatmentCategory
from hospitals.models import Hospital
from doctors.models import Doctor

# The treatments home URL — resolved once so all tests use the same path.
# i18n_patterns with LocaleMiddleware may redirect /treatments/ → /en/treatments/,
# so we use follow=True on all requests to land on the final rendered page.
TREATMENTS_URL = reverse("treatments_home")

# Override static files storage to avoid needing collectstatic during tests.
# WhiteNoise's CompressedManifestStaticFilesStorage requires a pre-built manifest
# which is not available in the test environment.
STATIC_OVERRIDE = override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)


class TreatmentsFilterBugFixtures(TestCase):
    """Base class that sets up shared fixtures for all filter bug tests."""

    @classmethod
    def setUpTestData(cls):
        # Create two treatment categories
        cls.cat_cardiology = TreatmentCategory.objects.create(
            name="Cardiology",
            slug="cardiology",
            type="medical",
        )
        cls.cat_aesthetics = TreatmentCategory.objects.create(
            name="Aesthetics",
            slug="aesthetics",
            type="aesthetic",
        )

        # Create a hospital
        cls.hospital_apollo = Hospital.objects.create(
            name="Apollo Hospital",
            slug="apollo-hospital",
            city="Mumbai",
        )
        cls.hospital_other = Hospital.objects.create(
            name="City Care Hospital",
            slug="city-care-hospital",
            city="Delhi",
        )

        # Create a doctor
        cls.doctor_sharma = Doctor.objects.create(
            name="Dr. Sharma",
            slug="dr-sharma",
            specialization="Cardiology",
        )
        cls.doctor_other = Doctor.objects.create(
            name="Dr. Patel",
            slug="dr-patel",
            specialization="Aesthetics",
        )

        # Create treatments — one per category
        cls.treatment_bypass = Treatment.objects.create(
            name="Bypass Surgery",
            slug="bypass-surgery",
            category=cls.cat_cardiology,
            starting_price=150000,
        )
        cls.treatment_rhinoplasty = Treatment.objects.create(
            name="Rhinoplasty",
            slug="rhinoplasty",
            category=cls.cat_aesthetics,
            starting_price=80000,
        )

        # Link treatments to hospitals and doctors
        cls.hospital_apollo.treatments.add(cls.treatment_bypass)
        cls.hospital_other.treatments.add(cls.treatment_rhinoplasty)

        cls.doctor_sharma.treatments.add(cls.treatment_bypass)
        cls.doctor_sharma.hospitals.add(cls.hospital_apollo)

        cls.doctor_other.treatments.add(cls.treatment_rhinoplasty)
        cls.doctor_other.hospitals.add(cls.hospital_other)

    def setUp(self):
        self.client = Client()

    def get_treatments(self, params=None):
        """
        Helper: GET the treatments home page, following any locale redirects,
        and return the final response.

        The HTTP_ACCEPT_LANGUAGE header is required so that Django's
        LocaleMiddleware resolves the language and redirects correctly to
        /en/treatments/ (since i18n_patterns is used in the URL config).
        """
        return self.client.get(
            TREATMENTS_URL,
            params or {},
            follow=True,
            HTTP_ACCEPT_LANGUAGE="en-us,en;q=0.9",
        )


@STATIC_OVERRIDE
class SearchFilterTest(TreatmentsFilterBugFixtures):
    """
    Task 1.2 — GET /treatments/?search=<name> asserts only matching treatment cards appear.

    On unfixed code this FAILS because the template calls category.treatments.all,
    rendering all treatments regardless of the search filter.
    """

    def test_search_filter_shows_only_matching_treatment(self):
        """
        Searching for 'Bypass Surgery' should show only that treatment card
        and NOT show 'Rhinoplasty'.

        **Validates: Requirements 1.1, 2.1**
        """
        response = self.get_treatments({"search": "Bypass Surgery"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The matching treatment should appear
        self.assertIn("Bypass Surgery", content)

        # The non-matching treatment must NOT appear as a card
        # (it may appear in filter inputs or other UI elements, so we check
        # for the treatment card link which uses the slug)
        self.assertNotIn("/treatments/rhinoplasty/", content,
                         "Rhinoplasty card should not appear when searching for 'Bypass Surgery'")


@STATIC_OVERRIDE
class HospitalFilterTest(TreatmentsFilterBugFixtures):
    """
    Task 1.3 — GET /treatments/?hospital=<name> asserts only treatments at that hospital appear.

    On unfixed code this FAILS because the template ignores the filtered queryset.
    """

    def test_hospital_filter_shows_only_treatments_at_that_hospital(self):
        """
        Filtering by 'Apollo Hospital' should show only 'Bypass Surgery'
        (linked to Apollo) and NOT show 'Rhinoplasty' (linked to City Care).

        **Validates: Requirements 1.2, 2.2**
        """
        response = self.get_treatments({"hospital": "Apollo"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The treatment at Apollo should appear
        self.assertIn("Bypass Surgery", content)

        # The treatment NOT at Apollo must not appear as a card
        self.assertNotIn("/treatments/rhinoplasty/", content,
                         "Rhinoplasty card should not appear when filtering by 'Apollo Hospital'")


@STATIC_OVERRIDE
class DoctorFilterTest(TreatmentsFilterBugFixtures):
    """
    Task 1.4 — GET /treatments/?doctor=<name> asserts only treatments by that doctor appear.

    On unfixed code this FAILS because the template ignores the filtered queryset.
    """

    def test_doctor_filter_shows_only_treatments_by_that_doctor(self):
        """
        Filtering by 'Dr. Sharma' should show only 'Bypass Surgery'
        (linked to Dr. Sharma) and NOT show 'Rhinoplasty' (linked to Dr. Patel).

        **Validates: Requirements 1.3, 2.3**
        """
        response = self.get_treatments({"doctor": "Sharma"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The treatment by Dr. Sharma should appear
        self.assertIn("Bypass Surgery", content)

        # The treatment NOT by Dr. Sharma must not appear as a card
        self.assertNotIn("/treatments/rhinoplasty/", content,
                         "Rhinoplasty card should not appear when filtering by 'Dr. Sharma'")


@STATIC_OVERRIDE
class EmptyStateFilterTest(TreatmentsFilterBugFixtures):
    """
    Task 1.5 — GET /treatments/?search=xyznonexistent asserts "No treatments found"
    message appears and no treatment cards are rendered.

    On unfixed code this FAILS because:
    1. The template still renders all treatment cards (via category.treatments.all).
    2. The empty-state guard is `{% if not categories %}` which is always False.
    """

    def test_no_match_search_shows_empty_state_message(self):
        """
        Searching for a term that matches nothing should show the
        "No treatments found" message and render no treatment cards.

        **Validates: Requirements 1.4, 2.4**
        """
        response = self.get_treatments({"search": "xyznonexistent"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The empty-state message must appear
        self.assertIn("No treatments found", content,
                      "'No treatments found' message should appear when no treatments match")

        # No treatment cards should be rendered
        self.assertNotIn("/treatments/bypass-surgery/", content,
                         "Bypass Surgery card should not appear for a non-matching search")
        self.assertNotIn("/treatments/rhinoplasty/", content,
                         "Rhinoplasty card should not appear for a non-matching search")


# ---------------------------------------------------------------------------
# Preservation Tests (Task 5) — Regression Prevention
#
# These tests verify that the fix does NOT break existing behavior.
# They should pass on the fixed code.
# ---------------------------------------------------------------------------

@STATIC_OVERRIDE
class NoFilterPreservationTest(TreatmentsFilterBugFixtures):
    """
    Task 5.1 — GET /treatments/ with no query params asserts all treatments
    and all categories appear.

    Validates: Requirement 3.1
    """

    def test_no_filter_shows_all_treatments_and_categories(self):
        """
        When no filters are applied, all treatments must continue to display
        grouped by category.

        **Validates: Requirements 3.1**
        """
        response = self.get_treatments()
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # Both treatments must appear
        self.assertIn("Bypass Surgery", content,
                      "Bypass Surgery should appear when no filters are applied")
        self.assertIn("Rhinoplasty", content,
                      "Rhinoplasty should appear when no filters are applied")

        # Both category names must appear
        self.assertIn("Cardiology", content,
                      "Cardiology category should appear when no filters are applied")
        self.assertIn("Aesthetics", content,
                      "Aesthetics category should appear when no filters are applied")

        # The "No treatments found" empty-state must NOT appear
        self.assertNotIn("No treatments found", content,
                         "'No treatments found' must not appear when all treatments are shown")


@STATIC_OVERRIDE
class CategorySlugPreservationTest(TreatmentsFilterBugFixtures):
    """
    Task 5.2 — GET /treatments/category/<slug>/ asserts only treatments in
    that category appear.

    Validates: Requirement 3.2
    """

    def test_category_slug_shows_only_treatments_in_that_category(self):
        """
        When a category slug is provided in the URL, only treatments belonging
        to that category must continue to display.

        **Validates: Requirements 3.2**
        """
        # Use the named URL for the category-scoped page
        from django.urls import reverse as _reverse
        url = _reverse("treatments_by_category", kwargs={"category_slug": "cardiology"})

        response = self.client.get(
            url,
            follow=True,
            HTTP_ACCEPT_LANGUAGE="en-us,en;q=0.9",
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # Only the Cardiology treatment should appear as a card
        self.assertIn("Bypass Surgery", content,
                      "Bypass Surgery should appear for the cardiology category")

        # The Aesthetics treatment must NOT appear as a card
        self.assertNotIn("/treatments/rhinoplasty/", content,
                         "Rhinoplasty card should not appear when scoped to cardiology")


@STATIC_OVERRIDE
class FilterGroupingPreservationTest(TreatmentsFilterBugFixtures):
    """
    Task 5.3 — Filter returning results asserts matching treatments are grouped
    under correct category headings.

    Validates: Requirement 3.3
    """

    def test_filter_results_grouped_under_correct_category_heading(self):
        """
        When filters are applied and treatments are found, matching treatments
        must continue to be grouped under their correct category headings.

        **Validates: Requirements 3.3**
        """
        # Search for "Bypass Surgery" — it belongs to Cardiology
        response = self.get_treatments({"search": "Bypass Surgery"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The matching treatment must appear
        self.assertIn("Bypass Surgery", content,
                      "Bypass Surgery should appear in filtered results")

        # The correct category heading must appear
        self.assertIn("Cardiology", content,
                      "Cardiology category heading should appear for Bypass Surgery")

        # The non-matching category must NOT appear as a heading for a treatment block
        # (Aesthetics category block should be absent since Rhinoplasty is filtered out)
        self.assertNotIn("/treatments/rhinoplasty/", content,
                         "Rhinoplasty card should not appear when searching for 'Bypass Surgery'")


@STATIC_OVERRIDE
class FilterValuePersistencePreservationTest(TreatmentsFilterBugFixtures):
    """
    Task 5.4 — Submit filter form asserts form inputs retain submitted values
    in the rendered response.

    Validates: Requirement 3.4
    """

    def test_filter_values_are_preserved_in_form_inputs(self):
        """
        Filter values entered by the user must continue to be preserved in the
        form inputs after the page reloads.

        **Validates: Requirements 3.4**
        """
        response = self.get_treatments({
            "search": "Bypass",
            "hospital": "Apollo",
            "doctor": "Sharma",
        })
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The search input must retain its submitted value
        self.assertIn('value="Bypass"', content,
                      "Search input should retain the submitted value 'Bypass'")

        # The hospital input must retain its submitted value
        self.assertIn('value="Apollo"', content,
                      "Hospital input should retain the submitted value 'Apollo'")

        # The doctor input must retain its submitted value
        self.assertIn('value="Sharma"', content,
                      "Doctor input should retain the submitted value 'Sharma'")


@STATIC_OVERRIDE
class ClearFiltersPreservationTest(TreatmentsFilterBugFixtures):
    """
    Task 5.5 — Assert the "Clear Filters" anchor href is /treatments/.

    Validates: Requirement 3.5
    """

    def test_clear_filters_link_points_to_treatments_root(self):
        """
        Clicking "Clear Filters" must continue to navigate to /treatments/ and
        display all treatments unfiltered. We verify the href is correct.

        **Validates: Requirements 3.5**
        """
        # Load the page with an active filter so the Clear Filters link is visible
        response = self.get_treatments({"search": "Bypass"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()

        # The "Clear Filters" link must point to /treatments/ (or locale-prefixed equivalent)
        # The template has: <a href="/treatments/" class="dl-clear-btn ...">Clear Filters</a>
        self.assertIn('href="/treatments/"', content,
                      "Clear Filters link must have href='/treatments/'")
