
import re
from dataclasses import dataclass, field
from typing import Any

import PyPDF2

from django.db.models import Q


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ReportParseError(Exception):
    """Raised when a medical report file cannot be parsed."""
    pass


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class MedicalIntent:
    """Structured medical intent extracted from free text or a parsed report."""

    keywords: list        # raw search terms matched against the condition map
    conditions: list      # detected medical conditions (map keys that matched)
    specializations: list # matched doctor specializations (map values)
    raw_query: str        # original, un-normalized user input
    has_medical_match: bool = False  # True only when at least one map keyword matched


# ---------------------------------------------------------------------------
# Condition → Specialization mapping
# ---------------------------------------------------------------------------

CONDITION_SPECIALIZATION_MAP = {
    # Cardiac
    "heart":          ["Cardiac Surgeon", "Cardiology", "Cardiovascular Surgery", "Cardiac Surgery"],
    "cardiac":        ["Cardiac Surgeon", "Cardiology", "Cardiac Surgery"],
    "hypertension":   ["Cardiac Surgeon", "Cardiology", "Internal Medicine"],
    "blood pressure": ["Cardiac Surgeon", "Cardiology", "Internal Medicine"],
    # Orthopedic
    "knee":           ["Orthopedic Surgeon", "Orthopedic Surgery", "Joint Replacement"],
    "joint":          ["Orthopedic Surgeon", "Orthopedic Surgery", "Rheumatology"],
    "bone":           ["Orthopedic Surgeon", "Orthopedic Surgery"],
    "arthritis":      ["Orthopedic Surgeon", "Orthopedic Surgery", "Rheumatology"],
    "spine":          ["Orthopedic Surgeon", "Spine Surgery", "Neurosurgeon", "Neurosurgery"],
    # Neuro
    "brain":          ["Neurosurgeon", "Neurology", "Neurosurgery"],
    "neuro":          ["Neurosurgeon", "Neurology", "Neurosurgery"],
    "stroke":         ["Neurosurgeon", "Neurology"],
    "tumor":          ["Neurosurgeon", "Oncology", "Surgical Oncology"],
    # Oncology
    "cancer":         ["Oncology", "Surgical Oncology", "Pulmonologist"],
    # Endocrine
    "diabetes":       ["Endocrinology", "Internal Medicine", "General Medicine", "MBBS"],
    "thyroid":        ["Endocrinology"],
    # Gastro
    "liver":          ["Gastroenterologist", "Gastroenterology", "Hepatology"],
    "stomach":        ["Gastroenterologist", "Gastroenterology"],
    "gastro":         ["Gastroenterologist", "Gastroenterology"],
    # Urology / Nephrology
    "kidney":         ["Nephrology", "Urology"],
    "urology":        ["Urology"],
    # Ophthalmology
    "eye":            ["Ophthalmology"],
    "cataract":       ["Ophthalmology"],
    # Cosmetic / Aesthetic
    "cosmetic":       ["Plastic Surgeon", "Plastic Surgery", "Aesthetic Medicine"],
    "rhinoplasty":    ["Plastic Surgeon", "Plastic Surgery"],
    "breast":         ["Plastic Surgeon", "Plastic Surgery", "Aesthetic Medicine"],
    "augmentation":   ["Plastic Surgeon", "Plastic Surgery"],
    "liposuction":    ["Plastic Surgeon", "Plastic Surgery"],
    "facelift":       ["Plastic Surgeon", "Plastic Surgery"],
    "hair transplant":["Plastic Surgeon", "Plastic Surgery"],
    # Dental
    "dental":         ["Dental Surgeon", "Dentistry"],
    "teeth":          ["Dental Surgeon", "Dentistry"],
    "implant":        ["Dental Surgeon", "Dentistry"],
    "invisalign":     ["Dental Surgeon", "Dentistry"],
    "veneer":         ["Dental Surgeon", "Dentistry"],
    # Fertility
    "ivf":            ["Gynecologist", "Fertility", "Reproductive Medicine"],
    "fertility":      ["Gynecologist", "Fertility", "Reproductive Medicine"],
    "icsi":           ["Gynecologist", "Fertility", "Reproductive Medicine"],
    # Pulmonology
    "lung":           ["Pulmonologist", "Pulmonology"],
    "pulmonary":      ["Pulmonologist", "Pulmonology"],
    "copd":           ["Pulmonologist", "Pulmonology"],
    "asthma":         ["Pulmonologist", "Pulmonology"],
    "bronchoscopy":   ["Pulmonologist", "Pulmonology"],
    # Ophthalmology
    "eye":            ["Ophthalmologist", "Ophthalmology"],
    "cataract":       ["Ophthalmologist", "Ophthalmology"],
    "lasik":          ["Ophthalmologist", "Ophthalmology"],
    "retinal":        ["Ophthalmologist", "Ophthalmology"],
    "glaucoma":       ["Ophthalmologist", "Ophthalmology"],
    # Urology
    "kidney":         ["Nephrology", "Urology", "Urologist"],
    "urology":        ["Urologist", "Urology"],
    "prostate":       ["Urologist", "Urology"],
    # Wellness
    "panchakarma":    ["Wellness"],
    "yoga":           ["Wellness"],
    "ayurveda":       ["Wellness"],
}


# ---------------------------------------------------------------------------
# Intent extraction
# ---------------------------------------------------------------------------

class MedicalIntentExtractor:
    """
    Extracts structured medical intent from free text or parsed report text.

    Normalizes and tokenizes the input, then matches tokens (and bigrams) against
    CONDITION_SPECIALIZATION_MAP to produce a MedicalIntent with keywords,
    detected conditions, and matched doctor specializations.
    """

    def extract(self, text: str) -> MedicalIntent:
        """
        Parse free text into a MedicalIntent.

        Args:
            text: Raw query string or extracted report text (may be empty).

        Returns:
            MedicalIntent with keywords, conditions, specializations, and raw_query.
        """
        # Normalize: lowercase and strip leading/trailing whitespace
        text_lower = text.lower().strip()

        # Tokenize: split on whitespace and punctuation, filter empty strings
        tokens = [t for t in re.split(r'[\s\W]+', text_lower) if t]

        keywords: list = []
        conditions: list = []
        specializations: list = []

        # Single-token matching
        for token in tokens:
            if token in CONDITION_SPECIALIZATION_MAP:
                keywords.append(token)
                conditions.append(token)
                specializations.extend(CONDITION_SPECIALIZATION_MAP[token])

        # Bigram matching (e.g. "blood pressure", "knee replacement")
        for i in range(len(tokens) - 1):
            bigram = tokens[i] + ' ' + tokens[i + 1]
            if bigram in CONDITION_SPECIALIZATION_MAP:
                keywords.append(bigram)
                conditions.append(bigram)
                specializations.extend(CONDITION_SPECIALIZATION_MAP[bigram])

        # Deduplicate all three lists while preserving order
        keywords = list(dict.fromkeys(keywords))
        conditions = list(dict.fromkeys(conditions))
        specializations = list(dict.fromkeys(specializations))

        # Track whether any real medical condition was matched
        has_medical_match = bool(conditions)

        # Fallback: if no map matches found, use first 5 raw tokens as keywords
        # These are ONLY used for doctor name search, not treatment/hospital search
        if not keywords:
            keywords = tokens[:5]

        return MedicalIntent(
            keywords=keywords,
            conditions=conditions,
            specializations=specializations,
            raw_query=text,
            has_medical_match=has_medical_match,
        )


# ---------------------------------------------------------------------------
# Report parsing
# ---------------------------------------------------------------------------

class ReportParser:
    """
    Parses uploaded medical report files into plain text.

    Supports PDF, common image formats (stub), and plain text.
    Raises ReportParseError for unsupported content types.
    """

    def parse(self, uploaded_file) -> str:
        """
        Extract text content from an uploaded file.

        Args:
            uploaded_file: A Django UploadedFile (or any file-like object with
                           a ``content_type`` attribute and ``read()`` / ``seek()``
                           methods).

        Returns:
            Extracted text as a string, or ``""`` if extraction fails.

        Raises:
            ReportParseError: If the content type is not supported.
        """
        content_type = uploaded_file.content_type

        if content_type == "application/pdf":
            try:
                reader = PyPDF2.PdfReader(uploaded_file)
                pages_text = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                return "\n".join(pages_text)
            except Exception:
                return ""
            finally:
                # Seek back so the file is not consumed for any subsequent reads
                try:
                    uploaded_file.seek(0)
                except Exception:
                    pass

        elif content_type in ("image/jpeg", "image/png", "image/gif"):
            return "[Image report uploaded — OCR not yet available]"

        elif content_type == "text/plain":
            try:
                data = uploaded_file.read()
                return data.decode("utf-8", errors="replace")
            finally:
                try:
                    uploaded_file.seek(0)
                except Exception:
                    pass

        else:
            raise ReportParseError(f"Unsupported file type: {content_type}")


# ---------------------------------------------------------------------------
# Placeholder categories
# ---------------------------------------------------------------------------

PLACEHOLDER_CATEGORIES = [
    {"key": "doctors",    "label": "Specialist Doctors",   "icon": "bi-person-badge",   "url": "/doctors/"},
    {"key": "hospitals",  "label": "Hospitals",            "icon": "bi-building",       "url": "/hospitals/"},
    {"key": "treatments", "label": "Treatments",           "icon": "bi-bandaid",        "url": "/treatments/"},
    {"key": "blogs",      "label": "Health Articles",      "icon": "bi-journal-text",   "url": "/blogs/"},
    {"key": "pricing",    "label": "Pricing & Packages",   "icon": "bi-currency-rupee", "url": "/pricing/"},
    {"key": "feedbacks",  "label": "Patient Reviews",      "icon": "bi-star",           "url": "/feedbacks/"},
    {"key": "videos",     "label": "Video Consultations",  "icon": "bi-camera-video",   "url": "#"},
    {"key": "packages",   "label": "Medical Packages",     "icon": "bi-box-seam",       "url": "#"},
    {"key": "hotels",     "label": "Nearby Hotels",        "icon": "bi-house",          "url": "/hotels/"},
    {"key": "insurance",  "label": "Insurance & Finance",  "icon": "bi-shield-check",   "url": "#"},
]


class PlaceholderRegistry:
    """
    Determines which content categories have data and which are placeholders.

    Compares each category key in PLACEHOLDER_CATEGORIES against the provided
    context dict. Categories with non-empty (truthy) values are marked as having
    data; empty/missing categories are marked as coming soon.
    """

    def get_placeholders(self, context_dict: dict) -> list[dict]:
        """
        Build a list of category dicts annotated with data availability.

        Args:
            context_dict: Mapping of category keys to their content
                          (QuerySet, list, or any truthy/falsy value).

        Returns:
            A list with exactly ``len(PLACEHOLDER_CATEGORIES)`` entries.
            Each entry is a copy of the category definition plus:
            - ``has_data`` (bool): True if the category has content.
            - ``coming_soon`` (bool): True if the category has no content.
        """
        result = []
        for category in PLACEHOLDER_CATEGORIES:
            value = context_dict.get(category["key"])
            has_data = bool(value)
            entry = dict(category)  # shallow copy to avoid mutating the constant
            entry["has_data"] = has_data
            entry["coming_soon"] = not has_data
            result.append(entry)
        return result


# ---------------------------------------------------------------------------
# Smart results context
# ---------------------------------------------------------------------------

@dataclass
class SmartResultsContext:
    """
    Aggregated results context passed to the smart_results.html template.

    Holds all matched content categories plus metadata about the search intent.
    """

    query_summary: str       # human-readable summary of the search (e.g. "Showing results for: knee")
    doctors: Any             # QuerySet or list of Doctor objects
    hospitals: Any           # QuerySet or list of Hospital objects
    treatments: Any          # QuerySet or list of Treatment objects
    blogs: Any               # QuerySet or list of BlogPost objects
    pricing_data: list       # list of dicts: {treatment_name, hospital_name, price}
    feedbacks: Any           # QuerySet or list of Feedback objects
    placeholders: list       # list of category dicts from PlaceholderRegistry
    intent: MedicalIntent    # the extracted medical intent that produced these results
    report_summary: str = "" # first ~500 chars of parsed report text (empty if no report)


# ---------------------------------------------------------------------------
# Site content aggregator
# ---------------------------------------------------------------------------


class SiteContentAggregator:
    """
    Queries all content models using a MedicalIntent and returns a unified
    SmartResultsContext ready for template rendering.
    """

    def aggregate(self, intent: MedicalIntent) -> SmartResultsContext:
        """
        Aggregate site content matching the given medical intent.

        Args:
            intent: A MedicalIntent produced by MedicalIntentExtractor.

        Returns:
            SmartResultsContext with matched doctors, hospitals, treatments,
            blogs, feedbacks, pricing data, placeholders, and a query summary.
        """
        # Lazy imports to avoid AppRegistryNotReady at module load time
        from doctors.models import Doctor
        from hospitals.models import Hospital
        from treatments.models import Treatment
        from blogs.models import BlogPost
        from feedbacks.models import Feedback

        keywords = intent.keywords
        specializations = intent.specializations
        raw_query = intent.raw_query.strip()
        # conditions = only the map-matched keywords (not fallback tokens)
        conditions = intent.conditions
        has_medical_match = intent.has_medical_match

        # ------------------------------------------------------------------
        # No query at all → return empty results with a prompt.
        # ------------------------------------------------------------------
        has_query = bool(keywords or raw_query)
        if not has_query:
            empty_placeholders = PlaceholderRegistry().get_placeholders({})
            return SmartResultsContext(
                query_summary="Try searching for a condition, treatment, or doctor name.",
                doctors=[],
                hospitals=[],
                treatments=[],
                blogs=[],
                pricing_data=[],
                feedbacks=[],
                placeholders=empty_placeholders,
                intent=intent,
            )

        # ------------------------------------------------------------------
        # For treatments, hospitals, blogs: use ONLY map-matched conditions.
        # Fallback tokens (e.g. "high", "normal", "patient") must NOT drive
        # these queries — they would match unrelated DB records.
        # Exception: if raw_query looks like a treatment name (no map match
        # but query is meaningful), search treatments directly by name.
        # ------------------------------------------------------------------
        search_keywords = conditions if has_medical_match else []

        # Direct treatment name search when no map match but query exists
        # e.g. "Breast Augmentation", "LASIK Surgery", "Knee Replacement"
        direct_treatment_search = not has_medical_match and len(raw_query) >= 4

        # ------------------------------------------------------------------
        # Doctors: match by specialization (primary) OR condition keyword name.
        # Use icontains so "Orthopedic Surgeon" matches "Orthopedic Surgery" etc.
        # ------------------------------------------------------------------
        spec_q = Q()
        for spec in specializations:
            spec_q |= Q(specialization__icontains=spec)

        # Also try matching the condition keyword directly against specialization
        # e.g. "cardiac" matches "Cardiac Surgeon"
        for cond in conditions:
            spec_q |= Q(specialization__icontains=cond)

        # For direct treatment queries (e.g. "Breast Augmentation"), match by
        # treatment name or specialization keywords from the raw query
        if direct_treatment_search:
            for word in raw_query.split():
                if len(word) >= 4:
                    spec_q |= Q(specialization__icontains=word)
                    spec_q |= Q(treatments__name__icontains=word)

        if spec_q:
            doctors_list = list(
                Doctor.objects
                .filter(spec_q)
                .prefetch_related('hospitals', 'treatments')
                .distinct()[:6]
            )
        else:
            doctors_list = []

        # ------------------------------------------------------------------
        # Treatments: match by name or description — only real conditions.
        # Also search by raw_query directly when no map match (e.g. "Breast Augmentation").
        # ------------------------------------------------------------------
        treat_q = Q()
        for kw in search_keywords:
            treat_q |= Q(name__icontains=kw) | Q(description__icontains=kw)

        # Direct name search for unmatched queries like "Breast Augmentation"
        if direct_treatment_search:
            treat_q |= Q(name__icontains=raw_query) | Q(description__icontains=raw_query)
            # Also try individual words from the query
            for word in raw_query.split():
                if len(word) >= 4:
                    treat_q |= Q(name__icontains=word)

        if not treat_q:
            treatments_list = []
        else:
            treatments_list = list(Treatment.objects.filter(treat_q).distinct()[:6])

        # ------------------------------------------------------------------
        # Hospitals: show only hospitals that offer the matched treatments.
        # This is more precise than keyword matching on treatment names.
        # ------------------------------------------------------------------
        if treatments_list:
            hospitals_list = list(
                Hospital.objects
                .filter(treatments__in=treatments_list)
                .order_by('-rating')
                .select_related('country', 'state')
                .prefetch_related('treatments', 'doctors')
                .distinct()[:6]
            )
        elif doctors_list:
            # Fallback: hospitals associated with matched doctors
            hospitals_list = list(
                Hospital.objects
                .filter(doctors__in=doctors_list)
                .order_by('-rating')
                .select_related('country', 'state')
                .distinct()[:6]
            )
        else:
            hospitals_list = []

        # ------------------------------------------------------------------
        # Blogs: match by title or content — only real conditions.
        # ------------------------------------------------------------------
        blog_q = Q()
        for kw in search_keywords:
            blog_q |= Q(title__icontains=kw) | Q(content__icontains=kw)

        if not blog_q:
            blogs_list = []
        else:
            blogs_list = list(BlogPost.objects.filter(blog_q).distinct()[:4])

        # ------------------------------------------------------------------
        # Feedbacks: approved reviews for matched doctors only.
        # ------------------------------------------------------------------
        if doctors_list:
            feedbacks_list = list(
                Feedback.objects
                .filter(is_approved=True, doctor__in=doctors_list)
                .distinct()[:4]
            )
        else:
            feedbacks_list = []

        # ------------------------------------------------------------------
        # Pricing data: one row per treatment showing its own starting price.
        # Do NOT cross-join treatments × hospitals — that creates duplicate rows.
        # ------------------------------------------------------------------
        pricing_data: list = []
        for treatment in treatments_list:
            if treatment.starting_price:
                pricing_data.append({
                    "treatment_name": treatment.name,
                    "hospital_name": "",   # not hospital-specific
                    "price": treatment.starting_price,
                })

        # ------------------------------------------------------------------
        # Placeholders
        # ------------------------------------------------------------------
        context_dict = {
            "doctors": doctors_list,
            "hospitals": hospitals_list,
            "treatments": treatments_list,
            "blogs": blogs_list,
            "pricing": pricing_data,
            "feedbacks": feedbacks_list,
        }
        placeholders = PlaceholderRegistry().get_placeholders(context_dict)

        # ------------------------------------------------------------------
        # Query summary
        # ------------------------------------------------------------------
        if conditions:
            query_summary = f"Showing results for: {', '.join(conditions)}"
        elif raw_query:
            query_summary = f"Showing results for: {raw_query}"
        else:
            query_summary = "Try searching for a condition, treatment, or doctor name."

        return SmartResultsContext(
            query_summary=query_summary,
            doctors=doctors_list,
            hospitals=hospitals_list,
            treatments=treatments_list,
            blogs=blogs_list,
            pricing_data=pricing_data,
            feedbacks=feedbacks_list,
            placeholders=placeholders,
            intent=intent,
        )
