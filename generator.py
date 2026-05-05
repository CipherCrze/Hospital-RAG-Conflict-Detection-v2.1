"""
generator.py — LLM Answer Generator

Constructs the Gemini API prompt from the retrieved chunks and conflict
report, invokes Gemini 2.0 Flash (temperature 0.2, max_tokens 1024),
and parses the structured Markdown response into an AnswerResult.

System prompt template is defined in SYSTEM_PROMPT (Annexure A of report).
"""
import os
import google.generativeai as genai
from models import RetrievedChunk, ConflictReport, AnswerResult


# ── System prompt (Annexure A) ────────────────────────────────────────
SYSTEM_PROMPT = """
You are a Healthcare Administrative Intelligence Assistant with expertise
in analysing multi-source hospital documents. Your role is to answer
questions posed by hospital administrators based solely on the provided
source passages. You must follow these rules strictly:

1. BASE YOUR ANSWER EXCLUSIVELY on the provided source passages.
   Do not use external knowledge or make assumptions beyond the text.

2. STRUCTURE YOUR RESPONSE as follows:
   - ANSWER: A direct, factual response to the question.
   - CONFIDENCE: One sentence qualifying the certainty of this answer.
   - SOURCES: A bulleted list of filenames used, with similarity scores.
   - CONTRADICTION ALERT (if applicable): If the CONTRADICTION REPORT
     below contains any conflicts, describe each conflict prominently,
     name both source documents involved, and advise the administrator
     to investigate the discrepancy before relying on this answer.

3. If the contradiction report is empty, omit the CONTRADICTION ALERT
   section entirely.

4. If the source passages do not contain sufficient information to
   answer the question, state this clearly rather than speculating.
"""

CONTEXT_TEMPLATE = """
USER QUERY: {query}

SOURCE PASSAGES:
{formatted_chunks}

CONTRADICTION REPORT:
{conflict_report}

Please provide your structured response following the rules above.
"""


# ── Helpers ───────────────────────────────────────────────────────────

def _format_chunks(chunks: list) -> str:
    """Format retrieved chunks with source/relevance headers for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        header = f"[SOURCE {i}: {chunk.source} | Relevance: {chunk.similarity_score:.2f}]"
        parts.append(f"{header}\n{chunk.text}")
    return "\n\n---\n\n".join(parts)


# ── Main generation function ──────────────────────────────────────────

def generate_answer(
    query: str,
    chunks: list,           # List[RetrievedChunk]
    conflict_report,        # ConflictReport
    api_key: str = None,
) -> AnswerResult:
    """
    Invoke Gemini 2.0 Flash to generate a structured answer.

    Args:
        query:           The user's natural language question.
        chunks:          Top-8 retrieved document chunks.
        conflict_report: ConflictReport from conflict_detector.py.
        api_key:         Gemini API key. Falls back to GOOGLE_API_KEY env var.

    Returns:
        AnswerResult with answer text, sources section, and optional alert.
    """
    key = api_key or os.environ.get("GOOGLE_API_KEY", "")
    genai.configure(api_key=key)

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=genai.GenerationConfig(
            temperature=0.2,
            max_output_tokens=1024,
        ),
        system_instruction=SYSTEM_PROMPT,
    )

    context_block = CONTEXT_TEMPLATE.format(
        query=query,
        formatted_chunks=_format_chunks(chunks),
        conflict_report=conflict_report.to_prompt_string(),
    )

    response = model.generate_content(context_block)
    raw = response.text.strip()

    # Parse sections from the structured Markdown response
    answer_text        = _extract_section(raw, "ANSWER",             fallback=raw)
    sources_section    = _extract_section(raw, "SOURCES",            fallback="")
    contradiction_alert = _extract_section(raw, "CONTRADICTION ALERT", fallback=None)

    return AnswerResult(
        answer=answer_text,
        sources_section=sources_section,
        contradiction_alert=contradiction_alert,
        raw_response=raw,
    )


def _extract_section(text: str, heading: str, fallback=None):
    """Extract a named section from a Markdown-structured LLM response."""
    import re
    pattern = rf"(?:^|\n)(?:#{{}})?\*{{0,2}}{re.escape(heading)}[:\s*]*\*{{0,2}}\n?(.*?)(?=\n(?:#{{}})?\*{{0,2}}(?:ANSWER|CONFIDENCE|SOURCES|CONTRADICTION ALERT|$))"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return fallback
