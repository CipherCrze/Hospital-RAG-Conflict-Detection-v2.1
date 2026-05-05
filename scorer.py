"""
scorer.py — Confidence Calibration Module

Computes the final confidence score for each query response using the
formula from Section 3.1.3b of the project report:

    confidence = mean(similarity_scores) × (1 − conflict_ratio × 0.5)

The conflict_ratio penalty is capped so that even a 100% conflict rate
reduces confidence by at most 50% — conflicting documents are still
informative and should not be treated the same as a retrieval failure.
"""
from models import RetrievedChunk, ConflictReport


def compute_confidence(
    chunks: list,           # List[RetrievedChunk]
    conflict_report,        # ConflictReport
) -> dict:
    """
    Calibrate confidence based on retrieval relevance and conflict ratio.

    Algorithm 2 from the project report (Section 3.1.3b):
        1. relevance        = mean(chunk.similarity_score for chunk in chunks)
        2. conflict_penalty = conflict_report.conflict_ratio * 0.5
        3. confidence       = relevance * (1 - conflict_penalty)

    Args:
        chunks:          List of RetrievedChunk objects with similarity_score.
        conflict_report: ConflictReport from conflict_detector.py

    Returns:
        Dict with keys: 'score' (float 0–1), 'level' (str), 'factors' (list)
    """
    if not chunks:
        return {
            "score": 0.0,
            "level": "Low",
            "factors": ["No relevant documents found"],
        }

    # Step 1 — base relevance from mean cosine similarity of retrieved chunks
    relevance = sum(c.similarity_score for c in chunks) / len(chunks)

    # Step 2 — conflict penalty: proportional to conflict ratio, max 0.5
    conflict_penalty = conflict_report.conflict_ratio * 0.5

    # Step 3 — final calibrated score
    confidence = relevance * (1.0 - conflict_penalty)
    confidence = max(0.0, min(1.0, confidence))

    # Step 4 — categorise
    if confidence > 0.80:
        category = "High"
    elif confidence > 0.60:
        category = "Medium"
    else:
        category = "Low"

    # Build human-readable factor list for UI display
    factors = [f"Avg retrieval similarity: {relevance:.2f}"]
    if conflict_report.has_conflicts:
        factors.append(
            f"{conflict_report.conflict_count} conflict(s) detected "
            f"(conflict_ratio = {conflict_report.conflict_ratio:.2f})"
        )
        factors.append(
            f"Conflict penalty applied: {conflict_penalty:.2f} "
            f"(raw score reduced from {relevance:.2f} → {confidence:.2f})"
        )

    return {
        "score": round(confidence, 4),
        "level": category,
        "factors": factors,
    }
