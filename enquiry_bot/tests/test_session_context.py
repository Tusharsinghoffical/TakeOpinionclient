"""
Property-based tests for session context accumulation in smart_results_api.

**Validates: Requirements 6.1, 6.3, 6.5**

These tests verify that:
  - Property 1 (Conditions-only storage): session['chatbot_context'] after any
    sequence of queries contains only strings that are keys in
    CONDITION_SPECIALIZATION_MAP — never raw fallback tokens.
  - Property 2 (Fallback-token isolation): when a query produces
    intent.conditions == [], the session value is unchanged from before the call.
"""

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st
from hypothesis.extra.django import TestCase

from enquiry_bot.smart_search import (
    CONDITION_SPECIALIZATION_MAP,
    MedicalIntentExtractor,
    MedicalIntent,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_CONDITIONS = list(CONDITION_SPECIALIZATION_MAP.keys())

# Tokens that are guaranteed NOT to be in the map (pure noise words)
NOISE_WORDS = [
    "the", "and", "or", "is", "a", "an", "of", "in", "to", "for",
    "with", "on", "at", "by", "from", "up", "about", "into", "through",
    "during", "before", "after", "above", "below", "between", "out",
    "off", "over", "under", "again", "further", "then", "once",
    "hello", "please", "help", "me", "my", "i", "we", "you", "they",
    "normal", "high", "low", "good", "bad", "patient", "doctor",
    "hospital", "report", "test", "result", "value", "level",
]


def _make_session_dict(initial=None):
    """Return a simple dict that mimics Django's session interface."""
    d = {} if initial is None else dict(initial)
    return d


def _simulate_smart_results_api_session_logic(query_text: str, session: dict) -> dict:
    """
    Replicate the session-update logic from smart_results_api (views.py) in isolation,
    without touching the database or HTTP layer.

    Returns the updated session dict.
    """
    prior_conditions = session.get("chatbot_context", [])
    if prior_conditions:
        merged_text = (query_text + " " + " ".join(prior_conditions)).strip()
    else:
        merged_text = query_text

    intent = MedicalIntentExtractor().extract(merged_text)

    # Mirror the exact logic from smart_results_api:
    # Only update session when new conditions are found; otherwise leave intact.
    if intent.conditions:
        session["chatbot_context"] = intent.conditions

    return session


# ---------------------------------------------------------------------------
# Strategy helpers
# ---------------------------------------------------------------------------

# A strategy that generates a single valid condition key from the map
valid_condition_strategy = st.sampled_from(VALID_CONDITIONS)

# A strategy that generates a noise-only query (no map keys)
noise_query_strategy = st.lists(
    st.sampled_from(NOISE_WORDS), min_size=1, max_size=6
).map(lambda words: " ".join(words))

# A strategy that generates a query containing at least one valid condition
medical_query_strategy = st.lists(
    st.one_of(
        st.sampled_from(VALID_CONDITIONS),
        st.sampled_from(NOISE_WORDS),
    ),
    min_size=1,
    max_size=8,
).map(lambda words: " ".join(words))

# A strategy for any query (may or may not contain conditions)
any_query_strategy = st.one_of(noise_query_strategy, medical_query_strategy)


# ---------------------------------------------------------------------------
# Property 1: Conditions-only storage
# **Validates: Requirements 6.1, 6.5**
#
# For any sequence of queries, session['chatbot_context'] after each call
# contains only strings that appear in CONDITION_SPECIALIZATION_MAP keys
# (never raw fallback tokens).
# ---------------------------------------------------------------------------

class TestConditionsOnlyStorage(TestCase):
    """
    **Validates: Requirements 6.1, 6.5**

    Property 1: Conditions-only storage.
    After any sequence of queries, every string stored in
    session['chatbot_context'] must be a key in CONDITION_SPECIALIZATION_MAP.
    """

    @given(queries=st.lists(any_query_strategy, min_size=1, max_size=10))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_session_stores_only_condition_map_keys(self, queries):
        """
        **Validates: Requirements 6.1, 6.5**

        For any sequence of queries, every value stored in
        session['chatbot_context'] is a key in CONDITION_SPECIALIZATION_MAP.
        """
        session = {}

        for query in queries:
            session = _simulate_smart_results_api_session_logic(query, session)

        stored = session.get("chatbot_context", [])

        for token in stored:
            self.assertIn(
                token,
                CONDITION_SPECIALIZATION_MAP,
                msg=(
                    f"Token {token!r} stored in session['chatbot_context'] is NOT "
                    f"a key in CONDITION_SPECIALIZATION_MAP. "
                    f"Queries were: {queries!r}"
                ),
            )

    @given(
        noise_query=noise_query_strategy,
        medical_query=medical_query_strategy,
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_noise_query_after_medical_does_not_add_fallback_tokens(
        self, noise_query, medical_query
    ):
        """
        **Validates: Requirements 6.1, 6.5**

        After a medical query sets conditions in the session, a subsequent
        noise-only query must NOT add any fallback tokens to the session.
        The session must still contain only CONDITION_SPECIALIZATION_MAP keys.
        """
        session = {}

        # First: a query that may set real conditions
        session = _simulate_smart_results_api_session_logic(medical_query, session)

        # Second: a noise-only query (no map matches)
        session = _simulate_smart_results_api_session_logic(noise_query, session)

        stored = session.get("chatbot_context", [])

        for token in stored:
            self.assertIn(
                token,
                CONDITION_SPECIALIZATION_MAP,
                msg=(
                    f"Token {token!r} in session after noise query is NOT a "
                    f"CONDITION_SPECIALIZATION_MAP key. "
                    f"medical_query={medical_query!r}, noise_query={noise_query!r}"
                ),
            )


# ---------------------------------------------------------------------------
# Property 2: Fallback-token isolation
# **Validates: Requirements 6.3**
#
# When a query produces intent.conditions == [], the session value is
# unchanged from before the call.
# ---------------------------------------------------------------------------

class TestFallbackTokenIsolation(TestCase):
    """
    **Validates: Requirements 6.3**

    Property 2: Fallback-token isolation.
    When a query produces no conditions (only fallback tokens), the session
    must remain exactly as it was before the call.
    """

    @given(
        prior_conditions=st.lists(
            st.sampled_from(VALID_CONDITIONS), min_size=0, max_size=5, unique=True
        ),
        noise_query=noise_query_strategy,
    )
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_no_conditions_query_leaves_session_unchanged(
        self, prior_conditions, noise_query
    ):
        """
        **Validates: Requirements 6.3**

        When a noise-only query (one that produces intent.conditions == [])
        is processed, the session['chatbot_context'] must be identical to
        what it was before the call.
        """
        # Confirm the noise query actually produces no conditions
        intent = MedicalIntentExtractor().extract(noise_query)
        if intent.conditions:
            # The generated query accidentally matched a condition; skip this example
            return

        # Set up session with prior conditions (may be empty)
        session = {}
        if prior_conditions:
            session["chatbot_context"] = list(prior_conditions)

        snapshot_before = list(session.get("chatbot_context", []))

        # Run the session logic with the noise query
        session = _simulate_smart_results_api_session_logic(noise_query, session)

        snapshot_after = list(session.get("chatbot_context", []))

        self.assertEqual(
            set(snapshot_before),
            set(snapshot_after),
            msg=(
                f"Session changed after a no-conditions query! "
                f"Before: {snapshot_before!r}, After: {snapshot_after!r}, "
                f"noise_query={noise_query!r}"
            ),
        )

    @given(noise_query=noise_query_strategy)
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    def test_empty_session_stays_empty_after_noise_query(self, noise_query):
        """
        **Validates: Requirements 6.3**

        When the session is empty and a noise-only query is processed,
        the session must remain empty (no fallback tokens stored).
        """
        intent = MedicalIntentExtractor().extract(noise_query)
        if intent.conditions:
            return  # accidentally matched; skip

        session = {}
        session = _simulate_smart_results_api_session_logic(noise_query, session)

        stored = session.get("chatbot_context", [])
        self.assertEqual(
            stored,
            [],
            msg=(
                f"Expected empty session after noise query, got {stored!r}. "
                f"noise_query={noise_query!r}"
            ),
        )
