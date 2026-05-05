"""
resolution.py — AI-powered conflict resolution suggestions via Gemini 2.5 Flash.
"""
import os
import google.generativeai as genai


RESOLUTION_PROMPT = """You are a senior hospital administrator's AI advisor.

Two hospital documents contain conflicting information:

Document A — {source_a}:
"{excerpt_a}"

Document B — {source_b}:
"{excerpt_b}"

Contradiction score: {score:.0%}

Provide a concise, actionable response with exactly these three sections:

**Root Cause**
One sentence explaining the most likely reason for this discrepancy (e.g. different accounting methods, different time windows, different measurement instruments, departmental perspective bias).

**Resolution Steps**
3 numbered, specific actions the hospital administrator should take to resolve this conflict.

**Authoritative Source**
One sentence stating which document is more likely to be authoritative for this topic and why.
"""

SUMMARY_PROMPT = """You are a hospital intelligence analyst.

A user asked: "{question}"

The RAG system retrieved {n_chunks} document chunks and detected {n_conflicts} contradiction(s).
Here is the conflict report:
{conflict_summary}

Here is the generated answer:
{answer}

Write a 2-3 sentence executive summary suitable for a hospital board brief. Be factual, mention any unresolved contradictions, and recommend one clear next step.
"""


def suggest_resolution(conflict: dict, api_key: str) -> str:
    """Return Gemini's resolution suggestion for a single conflict dict."""
    try:
        genai.configure(api_key=api_key or os.environ.get("GOOGLE_API_KEY", ""))
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config=genai.GenerationConfig(temperature=0.3, max_output_tokens=512),
        )
        doc_a = conflict.get("doc_a", {})
        doc_b = conflict.get("doc_b", {})
        prompt = RESOLUTION_PROMPT.format(
            source_a=doc_a.get("source", "Source A"),
            excerpt_a=doc_a.get("snippet", "")[:300],
            source_b=doc_b.get("source", "Source B"),
            excerpt_b=doc_b.get("snippet", "")[:300],
            score=conflict.get("contradiction_score", 0),
        )
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return f"⚠ Could not generate resolution: {e}"


def executive_summary(question: str, answer: str, conflict_result: dict,
                      n_chunks: int, api_key: str) -> str:
    """Return a short executive summary of the query result."""
    try:
        genai.configure(api_key=api_key or os.environ.get("GOOGLE_API_KEY", ""))
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config=genai.GenerationConfig(temperature=0.2, max_output_tokens=256),
        )
        n_conflicts = conflict_result.get("conflict_count", 0)
        conflict_lines = []
        for c in conflict_result.get("conflicts", []):
            conflict_lines.append(
                f"- {c['doc_a']['source']} vs {c['doc_b']['source']} "
                f"(score {c['contradiction_score']:.2f})"
            )
        conflict_summary = "\n".join(conflict_lines) if conflict_lines else "None"
        prompt = SUMMARY_PROMPT.format(
            question=question, n_chunks=n_chunks, n_conflicts=n_conflicts,
            conflict_summary=conflict_summary, answer=answer[:1000],
        )
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return f"⚠ Could not generate summary: {e}"
