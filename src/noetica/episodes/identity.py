"""Episode content-hash identity (§11.7, D21).

Purpose: compute the reproducible content hash of an Episode — a function of its
    identity inputs only (task, grounded verdict outcome, environment), EXCLUDING volatile
    provenance (timing, cost) and measurement-quality signals (verdict.detail / flaky).
Owner: Noetica (Layer 2).
Consumer: Episode Store; Memory (PE-14); Evaluation (PE-17).
Constitution: §7.5; §11.7 (identity vs provenance); D16.1/D21 (hash excludes volatile).
Future implementation owner: Noetica.

No Memory/Knowledge/Context/Reasoning/Planning/Runtime logic; no domain content.
"""
from __future__ import annotations

from typing import Any

from noetica.interfaces.episode import Episode
from noetica.provenance.identity import canonical_sha256

# Fields that form the reproducible identity of an episode (inside the hash).
# Excluded (outside the hash): cost, provenance, verdict.detail, content_hash itself.
HASH_INCLUDED_FIELDS = ("task_id", "verdict_status", "verdict_confidence", "environment",
                        "schema_version")


def _identity_payload(episode: Episode) -> dict[str, Any]:
    return {
        "task_id": episode.task_id,
        "verdict_status": episode.verdict.status.value,
        "verdict_confidence": episode.verdict.confidence,
        "environment": dict(episode.environment),
        "schema_version": episode.schema_version,
    }


def episode_content_hash(episode: Episode) -> str:
    """Reproducible SHA-256 identity of an episode (excludes volatile provenance/cost)."""
    return canonical_sha256(_identity_payload(episode))
