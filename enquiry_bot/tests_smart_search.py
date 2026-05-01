"""
Property-based and unit tests for enquiry_bot.smart_search.

Validates: Requirements 2.5, 2.7, 5.1, 6.2, 12.1
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from enquiry_bot.smart_search import (
    CONDITION_SPECIALIZATION_MAP,
    MedicalIntent,
    MedicalIntentExtractor,
    PLACEHOLDER_CATEGORIES,
    PlaceholderRegistry,
    SiteContentAggregator,
)

# Flat set of all valid specialization values from the map
_ALL_SPECIALIZATIONS = {
    spec
    for specs in CONDITION_SPECIALIZATION_MAP.values()
    for spec in specs
}


# ---------------------------------------------------------------------------
# Property 1: raw_query identity
# For any text, extract(text).raw_query must equal the original text exactly.
# Validates: Requirements 2.5
# ---------------------------------------------------------------------------

@given(st.text())
@settings(max_examples=200)
def test_raw_query_identity(text: str) -> None:
    """**Validates: Requirements 2.5**

    Property 1: raw_query identity — the extractor must preserve the original
    input string verbatim in the returned MedicalIntent.raw_query field.
    """
    result = MedicalIntentExtractor().extract(text)
    assert result.raw_query == text


# ---------------------------------------------------------------------------
# Property 2: specializations subset
# For any text, every item in extract(text).specializations must be a value
# that exists in CONDITION_SPECIALIZATION_MAP.
# Validates: Requirements 2.7
# ---------------------------------------------------------------------------

@given(st.text())
@settings(max_examples=200)
def test_specializations_subset(text: str) -> None:
    """**Validates: Requirements 2.7**

    Property 2: specializations subset — every specialization returned by the
    extractor must come from the flat value set of CONDITION_SPECIALIZATION_MAP.
    """
    result = MedicalIntentExtractor().extract(text)
    for spec in result.specializations:
        assert spec in _ALL_SPECIALIZATIONS, (
            f"Unexpected specialization {spec!r} not in CONDITION_SPECIALIZATION_MAP values"
        )


# ---------------------------------------------------------------------------
# Property 4: placeholder count invariant
# For any context_dict, get_placeholders must return exactly
# len(PLACEHOLDER_CATEGORIES) entries — one per category, no more, no less.
# Validates: Requirements 6.2
# ---------------------------------------------------------------------------

@given(
    st.fixed_dictionaries(
        {cat["key"]: st.lists(st.text()) for cat in PLACEHOLDER_CATEGORIES}
    )
)
@settings(max_examples=200)
def test_placeholder_count_invariant(context_dict: dict) -> None:
    """**Validates: Requirements 6.2**

    Property 4: placeholder count invariant — PlaceholderRegistry.get_placeholders
    must always return exactly len(PLACEHOLDER_CATEGORIES) entries regardless of
    the contents of context_dict.
    """
    result = PlaceholderRegistry().get_placeholders(context_dict)
    assert len(result) == len(PLACEHOLDER_CATEGORIES), (
        f"Expected {len(PLACEHOLDER_CATEGORIES)} placeholders, got {len(result)}"
    )


# ---------------------------------------------------------------------------
# Property 3: bounded results
# For any MedicalIntent, SiteContentAggregator must return at most 6 doctors.
# Validates: Requirements 5.1, 12.1
# ---------------------------------------------------------------------------

_medical_intent_strategy = st.builds(
    MedicalIntent,
    keywords=st.lists(st.text(max_size=20), max_size=5),
    conditions=st.lists(st.text(max_size=20), max_size=5),
    specializations=st.lists(st.text(max_size=20), max_size=5),
    raw_query=st.text(max_size=100),
)


@pytest.mark.django_db
@given(_medical_intent_strategy)
@settings(max_examples=50)
def test_bounded_doctor_results(intent: MedicalIntent) -> None:
    """**Validates: Requirements 5.1, 12.1**

    Property 3: bounded results — for any MedicalIntent,
    SiteContentAggregator.aggregate must return at most 6 Doctor objects.
    """
    result = SiteContentAggregator().aggregate(intent)
    doctors = list(result.doctors)
    assert len(doctors) <= 6, (
        f"Expected at most 6 doctors, got {len(doctors)} for intent {intent!r}"
    )


# ===========================================================================
# Task 8.6 — Unit tests for MedicalIntentExtractor
# Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.6
# ===========================================================================

class TestMedicalIntentExtractorUnit:
    """Unit tests for MedicalIntentExtractor with specific known inputs."""

    def test_knee_replacement_specialization(self):
        """'knee replacement' → specializations contains 'Orthopedic Surgery'."""
        intent = MedicalIntentExtractor().extract("knee replacement")
        assert "Orthopedic Surgery" in intent.specializations

    def test_empty_string_returns_empty_lists(self):
        """Empty string → keywords == [], conditions == [], specializations == []."""
        intent = MedicalIntentExtractor().extract("")
        assert intent.keywords == []
        assert intent.conditions == []
        assert intent.specializations == []

    def test_unmatched_word_fallback(self):
        """'hello' (no map match) → keywords == ['hello'] via fallback."""
        intent = MedicalIntentExtractor().extract("hello")
        assert intent.keywords == ["hello"]
        assert intent.conditions == []
        assert intent.specializations == []

    def test_deduplication_repeated_keyword(self):
        """'knee knee' → keyword 'knee' appears exactly once."""
        intent = MedicalIntentExtractor().extract("knee knee")
        assert intent.keywords.count("knee") == 1

    def test_bigram_blood_pressure(self):
        """'blood pressure' → matched as bigram, 'Cardiology' in specializations."""
        intent = MedicalIntentExtractor().extract("blood pressure")
        assert "blood pressure" in intent.keywords
        assert "Cardiology" in intent.specializations

    def test_raw_query_preserved(self):
        """raw_query must equal the original input string exactly."""
        text = "Knee Replacement Surgery"
        intent = MedicalIntentExtractor().extract(text)
        assert intent.raw_query == text

    def test_multiple_conditions(self):
        """'heart diabetes' → both cardiac and endocrine specializations present."""
        intent = MedicalIntentExtractor().extract("heart diabetes")
        assert "Cardiology" in intent.specializations
        assert "Endocrinology" in intent.specializations

    def test_case_insensitive_matching(self):
        """'KNEE' (uppercase) → still matches 'knee' in the map."""
        intent = MedicalIntentExtractor().extract("KNEE")
        assert "Orthopedic Surgery" in intent.specializations


# ===========================================================================
# Task 8.7 — Unit tests for ReportParser
# Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.6, 4.7
# ===========================================================================

import io
from enquiry_bot.smart_search import ReportParser, ReportParseError


class MockFile:
    """Minimal file-like object that mimics Django's UploadedFile interface."""

    def __init__(self, content_type: str, content: bytes = b""):
        self.content_type = content_type
        self._content = content
        self._pos = 0

    def read(self) -> bytes:
        return self._content

    def seek(self, pos: int) -> None:
        self._pos = pos

    @property
    def size(self) -> int:
        return len(self._content)


# Minimal valid single-page PDF (hand-crafted, no external library needed)
_MINIMAL_PDF_BYTES = (
    b"%PDF-1.4\n"
    b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
    b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
    b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    b"4 0 obj\n<< /Length 44 >>\nstream\n"
    b"BT /F1 12 Tf 100 700 Td (Hello PDF) Tj ET\n"
    b"endstream\nendobj\n"
    b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    b"xref\n0 6\n"
    b"0000000000 65535 f \n"
    b"0000000009 00000 n \n"
    b"0000000058 00000 n \n"
    b"0000000115 00000 n \n"
    b"0000000266 00000 n \n"
    b"0000000360 00000 n \n"
    b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
    b"startxref\n441\n%%EOF\n"
)


class TestReportParserUnit:
    """Unit tests for ReportParser."""

    def test_pdf_parsing_returns_string(self):
        """PDF parsing with a minimal valid PDF → returns a string (may be empty)."""
        mock_file = MockFile(content_type="application/pdf", content=_MINIMAL_PDF_BYTES)
        result = ReportParser().parse(mock_file)
        assert isinstance(result, str)

    def test_image_jpeg_returns_ocr_stub(self):
        """image/jpeg → returns non-None string containing 'OCR'."""
        mock_file = MockFile(content_type="image/jpeg", content=b"\xff\xd8\xff")
        result = ReportParser().parse(mock_file)
        assert result is not None
        assert "OCR" in result

    def test_image_png_returns_ocr_stub(self):
        """image/png → returns non-None string containing 'OCR'."""
        mock_file = MockFile(content_type="image/png", content=b"\x89PNG")
        result = ReportParser().parse(mock_file)
        assert result is not None
        assert "OCR" in result

    def test_plain_text_returns_content(self):
        """text/plain with content b'hello world' → returns 'hello world'."""
        mock_file = MockFile(content_type="text/plain", content=b"hello world")
        result = ReportParser().parse(mock_file)
        assert result == "hello world"

    def test_unsupported_type_raises_error(self):
        """application/msword → raises ReportParseError."""
        mock_file = MockFile(content_type="application/msword", content=b"some bytes")
        with pytest.raises(ReportParseError):
            ReportParser().parse(mock_file)

    def test_corrupted_pdf_returns_empty_string(self):
        """Corrupted PDF bytes → returns '' (no exception propagated)."""
        mock_file = MockFile(content_type="application/pdf", content=b"not a real pdf")
        result = ReportParser().parse(mock_file)
        assert result == ""

    def test_plain_text_utf8_decoding(self):
        """text/plain with UTF-8 bytes → decoded correctly."""
        content = "Diagnosis: Diabetes Mellitus".encode("utf-8")
        mock_file = MockFile(content_type="text/plain", content=content)
        result = ReportParser().parse(mock_file)
        assert "Diabetes" in result


# ===========================================================================
# Task 8.8 — Unit tests for PlaceholderRegistry
# Validates: Requirements 6.2, 6.3, 6.4
# ===========================================================================


class TestPlaceholderRegistryUnit:
    """Unit tests for PlaceholderRegistry."""

    def _all_keys_context(self, value):
        """Build a context dict with all category keys set to the given value."""
        return {cat["key"]: value for cat in PLACEHOLDER_CATEGORIES}

    def test_fully_populated_context_all_has_data(self):
        """Fully populated context → all entries have has_data=True."""
        context = self._all_keys_context(["item1", "item2"])
        result = PlaceholderRegistry().get_placeholders(context)
        for entry in result:
            assert entry["has_data"] is True, (
                f"Expected has_data=True for key '{entry['key']}'"
            )

    def test_empty_context_all_coming_soon(self):
        """Empty context {} → all entries have coming_soon=True."""
        result = PlaceholderRegistry().get_placeholders({})
        for entry in result:
            assert entry["coming_soon"] is True, (
                f"Expected coming_soon=True for key '{entry['key']}'"
            )

    def test_partial_context_mixed_has_data(self):
        """Partial context → mixed has_data values."""
        # Populate only the first category key
        first_key = PLACEHOLDER_CATEGORIES[0]["key"]
        context = {first_key: ["some_item"]}
        result = PlaceholderRegistry().get_placeholders(context)

        # First entry should have data; at least one other should not
        first_entry = next(e for e in result if e["key"] == first_key)
        assert first_entry["has_data"] is True

        other_entries = [e for e in result if e["key"] != first_key]
        assert any(e["coming_soon"] is True for e in other_entries)

    def test_return_length_equals_placeholder_categories(self):
        """Return length always equals len(PLACEHOLDER_CATEGORIES)."""
        result = PlaceholderRegistry().get_placeholders({})
        assert len(result) == len(PLACEHOLDER_CATEGORIES)

    def test_empty_list_value_is_coming_soon(self):
        """A key mapped to an empty list [] → coming_soon=True (falsy)."""
        context = self._all_keys_context([])
        result = PlaceholderRegistry().get_placeholders(context)
        for entry in result:
            assert entry["coming_soon"] is True

    def test_has_data_and_coming_soon_are_complementary(self):
        """has_data and coming_soon must always be logical opposites."""
        context = {PLACEHOLDER_CATEGORIES[0]["key"]: ["x"]}
        result = PlaceholderRegistry().get_placeholders(context)
        for entry in result:
            assert entry["has_data"] != entry["coming_soon"], (
                f"has_data and coming_soon must be complementary for key '{entry['key']}'"
            )


# ===========================================================================
# Task 8.9 — Integration tests for smart_results_view
# Validates: Requirements 1.3, 1.4, 7.3, 7.5, 8.2, 11.1
# ===========================================================================

import io as _io
from django.test import TestCase, Client, override_settings
from django.urls import reverse


@pytest.mark.django_db
@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class TestSmartResultsViewIntegration(TestCase):
    """Integration tests for smart_results_view using Django TestClient.

    The project uses i18n_patterns with LocaleMiddleware, which redirects
    language-neutral URLs (e.g. /enquiries/results/) to language-prefixed
    ones (e.g. /en/enquiries/results/).  We use follow=True on all requests
    so the client transparently follows that redirect and we can assert on
    the final 200 response.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("enquiry_bot:smart_results")

    def test_post_knee_replacement_returns_200_with_summary(self):
        """POST {'query': 'knee replacement'} → HTTP 200, response contains 'Showing results for'."""
        response = self.client.post(
            self.url, {"query": "knee replacement"}, follow=True
        )
        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "Showing results for" in content

    def test_get_with_query_param_returns_200(self):
        """GET ?q=diabetes → HTTP 200."""
        response = self.client.get(self.url, {"q": "diabetes"}, follow=True)
        assert response.status_code == 200

    def test_post_empty_query_returns_200(self):
        """POST with empty query → HTTP 200 (no 500 error)."""
        response = self.client.post(self.url, {"query": ""}, follow=True)
        assert response.status_code == 200

    def test_post_oversized_file_shows_limit_warning(self):
        """POST with oversized file mock → response contains '10 MB' or 'exceeds'."""
        from django.core.files.uploadedfile import SimpleUploadedFile
        from unittest.mock import patch, MagicMock

        # Django's multipart parser creates a new InMemoryUploadedFile from
        # the uploaded bytes, so we can't override .size on the original object.
        # Instead, patch the view's MAX_REPORT_SIZE_BYTES to 0 so any file triggers
        # the size warning.
        import enquiry_bot.views as views_module
        original = views_module.MAX_REPORT_SIZE_BYTES
        try:
            views_module.MAX_REPORT_SIZE_BYTES = 0  # any file exceeds 0 bytes
            mock_file = SimpleUploadedFile(
                "big_report.pdf", b"%PDF-1.4 fake", content_type="application/pdf"
            )
            response = self.client.post(
                self.url,
                {"query": "knee", "medical_report": mock_file},
                follow=True,
            )
        finally:
            views_module.MAX_REPORT_SIZE_BYTES = original

        assert response.status_code == 200
        content = response.content.decode("utf-8")
        assert "10 MB" in content or "exceeds" in content

    def test_get_no_query_returns_200(self):
        """GET with no query param → HTTP 200 (broad fallback)."""
        # Use the language-prefixed URL directly to avoid LocaleMiddleware redirect
        # issues when no query params are present.
        response = self.client.get("/en/enquiries/results/", data={}, follow=True)
        assert response.status_code == 200

    def test_post_cardiac_query_returns_200(self):
        """POST {'query': 'heart surgery'} → HTTP 200."""
        response = self.client.post(self.url, {"query": "heart surgery"}, follow=True)
        assert response.status_code == 200
