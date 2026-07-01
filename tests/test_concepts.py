"""
Tests for concept normalization — written BEFORE the implementation (TDD).

The job of normalize_concept: take whatever messy string the LLM produced
and map it to exactly ONE canonical concept from the curriculum, or "unknown".

Every test below documents one behavior the normalizer must have.
"""
import pytest
from phase2_memory.concepts import normalize_concept, KNOWN_CONCEPTS, UNKNOWN


# ── The core bug this whole component exists to fix ──────────────────────────

def test_case_and_spacing_variants_map_to_same_concept():
    """The ACTUAL bug from step9: 'Fractions Addition' vs 'fraction addition'.

    Both must resolve to the same canonical key, or the store splits the
    student's progress across two rows for one real concept.
    """
    a = normalize_concept("Fractions Addition")
    b = normalize_concept("fraction addition")
    assert a == b
    assert a != UNKNOWN          # it must actually match something, not give up


def test_exact_canonical_passes_through():
    """A string that already IS a known concept must come back unchanged."""
    # Whatever the canonical form of fraction addition is, feeding it back
    # must return itself.
    canonical = normalize_concept("fraction addition")
    assert normalize_concept(canonical) == canonical


def test_extra_whitespace_is_ignored():
    """Leading/trailing/double spaces must not break matching."""
    assert normalize_concept("  fraction   addition  ") == normalize_concept("fraction addition")


def test_different_casing_is_ignored():
    """ALL CAPS, lowercase, Title Case must all map to the same concept."""
    forms = ["FRACTION ADDITION", "fraction addition", "Fraction Addition"]
    results = [normalize_concept(f) for f in forms]
    assert len(set(results)) == 1            # all identical
    assert results[0] != UNKNOWN


# ── Word-overlap matching (the smart layer) ──────────────────────────────────

def test_word_reordering_still_matches():
    """'addition of fractions' shares the key words with 'fraction addition'."""
    result = normalize_concept("addition of fractions")
    assert result == normalize_concept("fraction addition")


def test_synonym_phrasing_matches_via_overlap():
    """'adding fractions' should match fraction addition by shared word root.

    This proves the overlap layer works, not just exact-cleaning.
    """
    result = normalize_concept("adding fractions")
    assert result == normalize_concept("fraction addition")


# ── The honest "I don't know" case ───────────────────────────────────────────

def test_unrelated_text_returns_unknown():
    """Something with no curriculum overlap must return UNKNOWN, not a wrong guess.

    A wrong guess is worse than 'unknown' — it silently corrupts the store.
    """
    assert normalize_concept("the capital of France") == UNKNOWN


def test_empty_string_returns_unknown():
    """Empty or whitespace-only input must safely return UNKNOWN, never crash."""
    assert normalize_concept("") == UNKNOWN
    assert normalize_concept("    ") == UNKNOWN


def test_weak_overlap_returns_unknown():
    """A single shared common word is NOT enough to claim a match.

    'addition of numbers' shares only 'addition' with fraction concepts but
    is really about something else — we must not force a confident match
    from one weak word.
    """
    result = normalize_concept("the of a")     # only stopword-like fragments
    assert result == UNKNOWN


# ── Curriculum integrity ─────────────────────────────────────────────────────

def test_known_concepts_is_nonempty_and_canonical():
    """The curriculum must exist, be non-empty, and every entry must be its
    own canonical form (feeding a known concept back returns itself)."""
    assert len(KNOWN_CONCEPTS) > 0
    for concept in KNOWN_CONCEPTS:
        assert normalize_concept(concept) == concept


def test_every_known_concept_is_lowercase_clean():
    """Canonical concepts must already be in clean form so comparisons are stable."""
    for concept in KNOWN_CONCEPTS:
        assert concept == concept.strip().lower()


def test_ambiguous_input_returns_unknown():
    """
    The input "fractions" matches several curriculum concepts equally well.

    The normalizer must NOT guess.
    It should fail safely by returning UNKNOWN.
    """

    assert normalize_concept("fractions") == UNKNOWN