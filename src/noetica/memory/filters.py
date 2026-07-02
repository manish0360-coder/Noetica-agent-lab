"""Constitutional Write Filters — the only gate controlling durable memory (§6.4, D7).

Purpose: decide what verified experience becomes durable memory. The write filter is the
    SINGLE manipulated variable of the compounding experiment (D6-D8): with the retriever
    held identical, the ONLY legal difference between arms is which filter is used.
Owner: Noetica (Layer 2).
Consumer: MemoryStore; Evaluation Harness (PE-17) configures arms; Velith runs the experiment.
Constitution: §6.4; D7 (A1/A2/A4 arms); §7.6 (compounding experiment); §11.10 (integrity test).
Future implementation owner: Noetica.

These are constitutional GATES, not learning policies or heuristics: each is a fixed
predicate over the episode's grounded verdict status.
"""
from __future__ import annotations

from noetica.interfaces.episode import Episode
from noetica.interfaces.verification import VerdictStatus

# Grounded verification outcomes that constitute VERIFIED learning (D7): a passing
# solution (PASSED) and a verified failure signature (FAILED). Upstream/non-grounded
# states (NO_PATCH, PATCH_APPLY_FAILED, INFRA_ERROR) are not verified learning.
_VERIFIED_STATUSES = frozenset({VerdictStatus.PASSED, VerdictStatus.FAILED})


class UnfilteredWriteFilter:
    """A1 (unverified control): retain every attempt regardless of verdict (RAG/null)."""

    def admit(self, episode: Episode) -> bool:
        return True


class VerifiedWriteFilter:
    """A2 (treatment): retain only verification-passing solutions and verified failure
    signatures — the verified-vs-unverified distinction (D7)."""

    def admit(self, episode: Episode) -> bool:
        return episode.verdict.status in _VERIFIED_STATUSES


class VerifiedSuccessOnlyWriteFilter:
    """A4 (ablation): retain only verification-passing solutions — isolates the value of
    grounded-failure learning (D7)."""

    def admit(self, episode: Episode) -> bool:
        return episode.verdict.status is VerdictStatus.PASSED
