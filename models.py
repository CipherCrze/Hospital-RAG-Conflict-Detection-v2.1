"""
models.py — Shared dataclass definitions for the Hospital RAG system.
Referenced in: ingest.py, retriever.py, conflict_detector.py, generator.py, scorer.py
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RetrievedChunk:
    """A single document chunk returned by the retrieval engine."""
    text: str
    source: str          # Original hospital document filename
    chunk_id: str        # SHA-256 hash of chunk text (16 chars)
    chunk_index: int     # Sequential index within the source document
    similarity_score: float  # Cosine similarity to the query vector


@dataclass
class ConflictEntry:
    """A single pairwise contradiction flagged by the NLI model."""
    source_a: str
    source_b: str
    score: float         # P(contradiction) from DeBERTa NLI model
    text_a: str          # First 120 chars of chunk A
    text_b: str          # First 120 chars of chunk B

    def to_prompt_string(self) -> str:
        return (
            f"- {self.source_a} vs {self.source_b}: CONTRADICTION score {self.score:.2f} "
            f"| Excerpt A: '{self.text_a[:80]}...' | Excerpt B: '{self.text_b[:80]}...'"
        )


@dataclass
class ConflictReport:
    """Aggregated output of the conflict detection phase."""
    conflicts: List[ConflictEntry] = field(default_factory=list)
    conflict_ratio: float = 0.0   # conflicting_pairs / total_pairs
    total_pairs: int = 0

    @property
    def has_conflicts(self) -> bool:
        return len(self.conflicts) > 0

    @property
    def conflict_count(self) -> int:
        return len(self.conflicts)

    def to_prompt_string(self) -> str:
        if not self.has_conflicts:
            return "No contradictions detected among retrieved sources."
        lines = [f"⚠ {self.conflict_count} contradiction(s) detected across {self.total_pairs} pairs:\n"]
        for c in self.conflicts:
            lines.append(c.to_prompt_string())
        return "\n".join(lines)


@dataclass
class AnswerResult:
    """Structured output returned by generator.py."""
    answer: str
    sources_section: str
    contradiction_alert: Optional[str]  # None when no conflicts
    raw_response: str


@dataclass
class QueryResult:
    """Complete result from a single query through the RAG pipeline."""
    question: str
    answer: str
    retrieved_chunks: List[RetrievedChunk]
    conflict_report: ConflictReport
    confidence_score: float
    confidence_level: str            # "High" | "Medium" | "Low"
    sources: List[str]               # Unique source filenames used
