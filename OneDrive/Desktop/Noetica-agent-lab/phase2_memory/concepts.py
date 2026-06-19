"""
Concept normalization: map messy LLM concept strings to ONE canonical
curriculum concept, or "unknown".

Why this exists: the LLM returns 'Fractions Addition' one run and
'fraction addition' another. Without normalization, KnowledgeState keys
them as two different concepts and splits the student's progress.

Approach: a FIXED curriculum (KNOWN_CONCEPTS) + cleaning + word-overlap
matching. No embeddings — overlap is the right weight for a small concept list.

The curriculum below is a placeholder single-subject set (fractions). In real
Noetica it comes from the course definition. Keep entries clean & lowercase.
"""
import re

UNKNOWN = "unknown"

# The fixed curriculum. Every entry is already in canonical form:
# lowercase, single-spaced, stripped. ONE subject, ~10 concepts, per the roadmap.
KNOWN_CONCEPTS = [
    "fraction addition",
    "fraction subtraction",
    "fraction multiplication",
    "fraction division",
    "equivalent fractions",
    "simplifying fractions",
    "comparing fractions",
    "mixed numbers",
    "improper fractions",
    "decimals to fractions",
]

# How strong a word overlap must be to count as a confident match.
# Measured as: shared meaningful words / words in the shorter phrase.
# 0.5 means at least half the words must align. Below this → unknown.
OVERLAP_THRESHOLD = 0.5

# Tiny words that carry no concept meaning — ignored during overlap matching
# so "addition OF fractions" matches "fraction addition".
_STOPWORDS = {"the", "a", "an", "of", "to", "and", "or", "with", "for", "in", "on"}


def _clean(text: str) -> str:
    """Lowercase, strip, and collapse internal whitespace to single spaces."""
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def _meaningful_words(text: str) -> set:
    """Split into words, drop stopwords, and reduce each word to a stable root.

    We chop a trailing 's' so 'fractions' and 'fraction' match. This is a
    deliberately crude stemmer — good enough for a fixed small curriculum,
    not a linguistics project.
    """
    words = _clean(text).split()
    roots = set()
    for w in words:
        if w in _STOPWORDS:
            continue
        if len(w) > 3 and w.endswith("s"):   # crude singularization
            w = w[:-1]
        roots.add(w)
    return roots

def _shares_root(w1: str, w2: str) -> bool:
    """
    Return True if two words appear to share the same root.

    Examples:
        adding <-> addition
        fraction <-> fractions

    This is NOT a real stemmer.
    It is a tiny heuristic for our fixed curriculum.
    """
    n = min(len(w1), len(w2))

    if n < 4:
        return w1 == w2

    return w1[:4] == w2[:4]


def _overlap_score(raw_roots: set, concept_roots: set) -> float:
    """
    Compute overlap using root matching instead of exact word equality.
    """

    shared = sum(
        1
        for rw in raw_roots
        if any(_shares_root(rw, cw) for cw in concept_roots)
    )

    denom = min(len(raw_roots), len(concept_roots))

    if denom == 0:
        return 0.0

    return shared / denom


def normalize_concept(raw: str) -> str:
    """Map a raw concept string to a canonical KNOWN_CONCEPTS entry, or UNKNOWN.

    Three layers, simplest first:
      1. clean + exact match
      2. word-overlap match (best-scoring known concept above threshold)
      3. give up honestly → UNKNOWN
    """
    cleaned = _clean(raw)
    if not cleaned:
        return UNKNOWN

    # Layer 1: exact match after cleaning.
    if cleaned in KNOWN_CONCEPTS:
        return cleaned

    # Layer 2: word-overlap matching.
    raw_roots = _meaningful_words(cleaned)
    if not raw_roots:
        return UNKNOWN

    # ---------------------------------------------------------
    # Layer 2: word-overlap matching.
    #
    # We don't only track the BEST score.
    # We also track the SECOND-BEST score.
    #
    # Why?
    #
    # Suppose the input is simply "fractions".
    #
    # It matches:
    #
    #   fraction addition
    #   fraction subtraction
    #   fraction multiplication
    #   fraction division
    #
    # all equally well.
    #
    # In that situation we DO NOT want to silently choose the
    # first concept in the curriculum.
    #
    # Returning UNKNOWN is much safer than corrupting the
    # student's KnowledgeState with the wrong concept.
    # ---------------------------------------------------------

    best_concept = UNKNOWN
    best_score = 0.0
    second_score = 0.0

    for concept in KNOWN_CONCEPTS:
        concept_roots = _meaningful_words(concept)

        score = _overlap_score(raw_roots, concept_roots)

        if score == 0:
            continue

        # New best concept found.
        # Push the previous best score down into second place.
        if score > best_score:
            second_score = best_score
            best_score = score
            best_concept = concept

        # Not the best...
        # ...but better than every previous runner-up.
        elif score > second_score:
            second_score = score

    # ---------------------------------------------------------
    # Only return a concept if:
    #
    # 1. It is above the confidence threshold.
    # 2. It is STRICTLY better than every other concept.
    #
    # If two concepts tie, we honestly admit that we
    # don't know.
    # ---------------------------------------------------------

    if (
        best_score >= OVERLAP_THRESHOLD
        and best_score > second_score
    ):
        return best_concept

    return UNKNOWN