"""
RAG Pipeline Orchestrator
- Combines retrieval, conflict detection, and LLM reasoning
- Provides structured responses with confidence calibration
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import (
    LLM_MODEL,
    LLM_TEMPERATURE,
    RAG_CONFLICT_PROMPT,
)
from retriever import retrieve_with_scores, format_retrieved_context, get_unique_sources
from conflict_detector import detect_conflicts, format_conflicts_for_prompt


def build_chain(api_key: str):
    """Build the RAG LLM chain."""
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=api_key,
        temperature=LLM_TEMPERATURE,
        convert_system_message_to_human=True,
    )

    prompt = PromptTemplate(
        template=RAG_CONFLICT_PROMPT,
        input_variables=["context", "conflicts", "question"],
    )

    chain = prompt | llm | StrOutputParser()
    return chain


def calibrate_confidence(
    retrieved_chunks: list[dict],
    conflict_result: dict,
) -> dict:
    """
    Calibrate confidence based on retrieval scores and conflicts.

    Formula from Section 3.1.3b of the project report:
        relevance        = mean(chunk.similarity_score for chunk in chunks)
        conflict_penalty = conflict_result['conflict_ratio'] * 0.5
        confidence       = relevance * (1 - conflict_penalty)

    The 0.5 scaling factor ensures that even a 100% conflict rate reduces
    confidence by at most 50% — conflicting documents are still informative.

    Returns:
        Dict with 'score' (0-100), 'level' (High/Medium/Low), 'factors' list
    """
    if not retrieved_chunks:
        return {"score": 0, "level": "Low", "factors": ["No relevant documents found"]}

    # Step 1 — base relevance: mean cosine similarity of retrieved chunks
    relevance = sum(r["similarity_score"] for r in retrieved_chunks) / len(retrieved_chunks)

    # Step 2 — conflict penalty proportional to conflict_ratio, capped at 0.5
    conflict_ratio   = conflict_result.get("conflict_ratio", 0.0)
    conflict_penalty = conflict_ratio * 0.5

    # Step 3 — final calibrated score (reported as percentage 0–100)
    confidence = relevance * (1.0 - conflict_penalty)
    confidence = max(0.0, min(1.0, confidence))
    final_score = round(confidence * 100, 1)

    # Step 4 — categorise
    if final_score > 80 and not conflict_result["has_conflicts"]:
        level = "High"
    elif final_score > 60:
        level = "Medium"
    else:
        level = "Low"

    # Build human-readable factor list
    factors = [f"Avg retrieval similarity: {relevance:.2f}"]
    if conflict_result["has_conflicts"]:
        n = conflict_result["conflict_count"]
        factors.append(f"{n} conflict(s) detected (conflict_ratio = {conflict_ratio:.2f})")
        factors.append(
            f"Confidence penalty: {conflict_penalty:.2f} "
            f"(raw {relevance:.2f} → calibrated {confidence:.2f})"
        )

    return {"score": final_score, "level": level, "factors": factors}


def query_with_conflict_detection(
    chain,
    vector_store,
    question: str,
) -> dict:
    """
    Full RAG pipeline with conflict detection.

    Returns:
        Dict with answer, conflicts, sources, confidence, and reasoning.
    """
    # Step 1: Retrieve relevant chunks with scores
    retrieved = retrieve_with_scores(vector_store, question)

    if not retrieved:
        return {
            "answer": "I couldn't find any relevant information in the hospital documents to answer this question.",
            "conflicts": {"conflicts": [], "has_conflicts": False, "conflict_count": 0},
            "sources": [],
            "confidence": {"score": 0, "level": "Low", "factors": ["No relevant documents found"]},
            "retrieved_chunks": [],
        }

    # Step 2: Detect conflicts among retrieved chunks
    conflict_result = detect_conflicts(retrieved)

    # Step 3: Format context and conflicts for LLM
    context_str = format_retrieved_context(retrieved)
    conflicts_str = format_conflicts_for_prompt(conflict_result)

    # Step 4: Invoke LLM
    answer = chain.invoke({
        "context": context_str,
        "conflicts": conflicts_str,
        "question": question,
    })

    # Step 5: Calibrate confidence
    confidence = calibrate_confidence(retrieved, conflict_result)

    # Step 6: Extract unique sources
    sources = get_unique_sources(retrieved)

    return {
        "answer": answer,
        "conflicts": conflict_result,
        "sources": sources,
        "confidence": confidence,
        "retrieved_chunks": retrieved,
    }
