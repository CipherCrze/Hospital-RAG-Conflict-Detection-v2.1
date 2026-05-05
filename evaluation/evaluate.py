"""
evaluate.py — Evaluation Runner for Hospital RAG Conflict Detection System

Runs the system against:
  1. The 50-pair annotation set (annotation_set.json) — measures NLI precision & recall
  2. The 20-query evaluation set (query_set.json)      — measures end-to-end conflict detection

Usage:
    python evaluation/evaluate.py

Requires the ChromaDB vector store to be populated (run ingest.py first).
"""
import os
import sys
import json
import time

# Add project root to path
EVAL_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR  = os.path.dirname(EVAL_DIR)
sys.path.insert(0, ROOT_DIR)


# ── 1. NLI Annotation Set Evaluation ─────────────────────────────────

def evaluate_nli_annotations(threshold: float = 0.65):
    """
    Evaluate the NLI model on the 50 manually annotated pairs.
    Measures precision, recall, and F1 for contradiction detection.
    """
    from sentence_transformers import CrossEncoder

    annotation_path = os.path.join(EVAL_DIR, "annotation_set.json")
    with open(annotation_path, "r", encoding="utf-8") as f:
        pairs = json.load(f)

    print("[EVAL] Loading NLI model...")
    model = CrossEncoder("cross-encoder/nli-deberta-v3-small")
    print("[EVAL] Model loaded. Evaluating 50 annotated pairs...\n")

    inputs = [(p["premise"], p["hypothesis"]) for p in pairs]
    scores = model.predict(inputs, batch_size=50, apply_softmax=True)

    CONTRA_IDX = 2  # [entailment, neutral, contradiction]

    true_positives  = 0
    false_positives = 0
    false_negatives = 0
    true_negatives  = 0
    results = []

    for pair, score in zip(pairs, scores):
        p_contra    = float(score[CONTRA_IDX])
        predicted   = p_contra >= threshold
        ground_truth = pair["label"] == "contradiction"

        if predicted and ground_truth:
            true_positives += 1
            outcome = "TP"
        elif predicted and not ground_truth:
            false_positives += 1
            outcome = "FP"
        elif not predicted and ground_truth:
            false_negatives += 1
            outcome = "FN"
        else:
            true_negatives += 1
            outcome = "TN"

        results.append({
            "id": pair["id"],
            "label": pair["label"],
            "p_contra": round(p_contra, 4),
            "predicted_contra": predicted,
            "outcome": outcome,
        })

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall    = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print("─" * 60)
    print("NLI ANNOTATION SET EVALUATION RESULTS")
    print(f"Threshold: {threshold}")
    print("─" * 60)
    print(f"True Positives  (TP): {true_positives}")
    print(f"False Positives (FP): {false_positives}")
    print(f"False Negatives (FN): {false_negatives}")
    print(f"True Negatives  (TN): {true_negatives}")
    print("─" * 60)
    print(f"Precision : {precision:.4f}  ({precision*100:.1f}%)")
    print(f"Recall    : {recall:.4f}  ({recall*100:.1f}%)")
    print(f"F1 Score  : {f1:.4f}  ({f1*100:.1f}%)")
    print("─" * 60)

    # Log false positives and false negatives for analysis
    print("\nFalse Positives (model flagged as contradiction, but neutral/entailment):")
    for r in results:
        if r["outcome"] == "FP":
            print(f"  [{r['id']}] p_contra={r['p_contra']:.4f} | true label: {r['label']}")

    print("\nFalse Negatives (model missed a true contradiction):")
    for r in results:
        if r["outcome"] == "FN":
            print(f"  [{r['id']}] p_contra={r['p_contra']:.4f} | true label: contradiction")

    return {"precision": precision, "recall": recall, "f1": f1}


# ── 2. End-to-End Query Set Evaluation ───────────────────────────────

def evaluate_query_set():
    """
    Run the full RAG pipeline on the 20 evaluation queries.
    Measures conflict detection accuracy and end-to-end latency.
    """
    from ingest import load_collection
    from retriever import retrieve
    from conflict_detector import detect_conflicts

    query_path = os.path.join(EVAL_DIR, "query_set.json")
    with open(query_path, "r", encoding="utf-8") as f:
        queries = json.load(f)

    print("\n[EVAL] Loading vector store...")
    try:
        collection = load_collection()
    except Exception as e:
        print(f"[ERROR] Vector store not found. Run ingest.py first.\n{e}")
        return

    correct = 0
    latencies = []

    print("[EVAL] Running 20 evaluation queries...\n")
    print("─" * 80)

    for q in queries:
        t0 = time.perf_counter()

        chunks    = retrieve(q["query"], collection, top_k=8)
        conf_res  = detect_conflicts([c.__dict__ for c in chunks])
        predicted = conf_res["has_conflicts"]
        expected  = q["expected_conflict"]

        elapsed = time.perf_counter() - t0
        latencies.append(elapsed)

        match   = "✓" if predicted == expected else "✗"
        correct += int(predicted == expected)

        print(f"{match} [{q['id']}] {q['category']:<25} | conflict={predicted} (expected={expected}) | {elapsed:.2f}s")
        print(f"    Q: {q['query'][:70]}")
        if predicted != expected:
            print(f"    !! MISMATCH — check query and document coverage")
        print()

    accuracy = correct / len(queries)
    avg_lat  = sum(latencies) / len(latencies)

    print("─" * 80)
    print(f"Conflict Detection Accuracy : {correct}/{len(queries)} ({accuracy*100:.1f}%)")
    print(f"Average Query Latency       : {avg_lat:.2f}s (retrieval + NLI only, no LLM)")
    print("─" * 80)


# ── Main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("HOSPITAL RAG — CONFLICT DETECTION EVALUATION")
    print("=" * 60)

    print("\n[PHASE 1] NLI Annotation Set (50 pairs, threshold=0.65)\n")
    evaluate_nli_annotations(threshold=0.65)

    print("\n[PHASE 2] End-to-End Query Set (20 queries)\n")
    evaluate_query_set()
