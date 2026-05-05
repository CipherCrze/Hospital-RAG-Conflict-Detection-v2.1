import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse

# ==============================================================================
# GLOBAL CONFIGURATION & HELPER FUNCTIONS
# ==============================================================================
plt.rcParams['font.family'] = 'DejaVu Sans'

# Color Palette
NAVY   = '#0D1B2A'
TEAL   = '#028090'
MINT   = '#02C39A'
SEAFOM = '#00A896'
PURP   = '#5C6BC0'
WARN   = '#F59E0B'
DANGER = '#E53935'
WHITE  = '#FFFFFF'
LIGHT  = '#E0F4F1'
OFFWH  = '#F4F9F9'
LGRAY  = '#CBD5E1'
GRAY   = '#64748B'

def setup_fig(figsize, title):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(OFFWH)
    ax.set_facecolor(OFFWH)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    # Title intentionally removed per user request
    return fig, ax

def save_fig(fig, filename):
    plt.savefig(f'./figures/{filename}', dpi=200, bbox_inches='tight', facecolor=OFFWH)
    plt.close(fig)

def draw_box(ax, x, y, w, h, text, bg, fg=WHITE, fontsize=9, fontweight='normal', italic=False, align='center'):
    # x, y is bottom-left of the EXACT outer bounding box
    pad = 0.012
    style = f"round,pad={pad}"
    box = FancyBboxPatch((x+pad, y+pad), w-2*pad, h-2*pad, boxstyle=style, facecolor=bg, edgecolor='none', zorder=2)
    ax.add_patch(box)
    fontstyle = 'italic' if italic else 'normal'
    ax.text(x + w/2, y + h/2, text, color=fg, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, fontstyle=fontstyle, clip_on=False, zorder=3)

def draw_arrow(ax, start, end, color=GRAY, lw=1.5, ls='solid', connectionstyle=None):
    arrow = FancyArrowPatch(start, end, color=color, linewidth=lw, arrowstyle='-|>',
                            mutation_scale=10, linestyle=ls, connectionstyle=connectionstyle, zorder=2)
    ax.add_patch(arrow)

def draw_diamond(ax, cx, cy, hw, hh, text, bg, fg=WHITE, fontsize=8.5):
    pts = [[cx, cy+hh], [cx+hw, cy], [cx, cy-hh], [cx-hw, cy]]
    poly = patches.Polygon(pts, closed=True, facecolor=bg, edgecolor='none', zorder=2)
    ax.add_patch(poly)
    ax.text(cx, cy, text, color=fg, ha='center', va='center', fontsize=fontsize, fontweight='bold', clip_on=False, zorder=3)

# ==============================================================================
# FIGURE GENERATORS
# ==============================================================================

def fig1_1():
    fig, ax = setup_fig((14, 5), "Figure 1.1  —  High-Level System Overview Architecture")
    
    xs = [0.02, 0.205, 0.390, 0.575, 0.760]
    w, h, y_c = 0.155, 0.38, 0.45
    y_bl = y_c - h/2
    
    boxes = [
        ("Document Store\n\nPDF · TXT\nHospital Reports", NAVY, WHITE),
        ("Embedding Model\n\nall-MiniLM-L6-v2\n384-dim", TEAL, WHITE),
        ("ChromaDB\nVector Store\n\nHNSW Cosine\nSearch", SEAFOM, WHITE),
        ("NLI Conflict\nDetector\n\nDeBERTa-v3-small\n28 Pairs", WARN, WHITE),
        ("Gemini 2.5\nFlash\n\nLLM Answer\nGeneration", MINT, NAVY)
    ]
    
    for i, (text, bg, fg) in enumerate(boxes):
        draw_box(ax, xs[i], y_bl, w, h, text, bg, fg=fg)
        if i < len(boxes) - 1:
            draw_arrow(ax, (xs[i]+w+0.005, 0.60), (xs[i+1]-0.005, 0.60), color=GRAY)
            
    # Output box
    draw_box(ax, 0.945, 0.49, 0.048, 0.30, "Answer\n+\nAlert", DANGER, fontsize=8)
    draw_arrow(ax, (xs[-1]+w+0.005, 0.60), (0.945-0.005, 0.60), color=GRAY)
    
    # User query
    draw_arrow(ax, (xs[1]+w/2, 0.92), (xs[1]+w/2, y_bl+h+0.005), color=TEAL, lw=2)
    ax.text(xs[1]+w/2, 0.95, "User Query", fontsize=9, color=TEAL, fontweight='bold', ha='center', va='center')
    
    # Conflict report
    y_feed = 0.18
    ax.plot([xs[3]+w/2, xs[4]+w/2], [y_feed, y_feed], ls='--', color=DANGER, zorder=1)
    ax.plot([xs[3]+w/2, xs[3]+w/2], [y_bl-0.005, y_feed], ls='--', color=DANGER, zorder=1)
    ax.plot([xs[4]+w/2, xs[4]+w/2], [y_bl-0.005, y_feed], ls='--', color=DANGER, zorder=1)
    
    ax.text((xs[3]+xs[4]+w)/2, 0.10, "Conflict Report injected into LLM prompt", 
            fontsize=8, color=DANGER, fontstyle='italic', ha='center')
            
    ax.text(0.5, 0.04, "Streamlit Dashboard  ·  Hospital Administrator", 
            ha='center', fontsize=9, color=GRAY, fontstyle='italic')
    save_fig(fig, "fig1_1.png")

def fig1_2():
    fig, ax = setup_fig((10, 7), "Figure 1.2  —  Use Case Diagram")
    
    # Boundary
    boundary = FancyBboxPatch((0.25, 0.05), 0.72, 0.88, boxstyle="square,pad=0", fill=False, edgecolor=TEAL, lw=2)
    ax.add_patch(boundary)
    ax.text(0.61, 0.905, "Hospital RAG — Conflict Detection Q&A System", fontsize=9.5, fontweight='bold', color=TEAL, ha='center')
    
    # Actor
    head = plt.Circle((0.10, 0.80), radius=0.032, color=NAVY, zorder=3)
    ax.add_patch(head)
    ax.plot([0.10, 0.10], [0.768, 0.66], color=NAVY, lw=2) # Body
    ax.plot([0.055, 0.145], [0.725, 0.725], color=NAVY, lw=2) # Arms
    ax.plot([0.10, 0.065], [0.66, 0.58], color=NAVY, lw=2) # L Leg
    ax.plot([0.10, 0.135], [0.66, 0.58], color=NAVY, lw=2) # R Leg
    ax.text(0.10, 0.545, "Hospital\nAdministrator", fontsize=8.5, fontweight='bold', color=NAVY, ha='center')
    
    # Ellipses & lines
    labels = ["Submit Natural Language Query", "View Structured Answer", 
              "View Contradiction Alert", "Inspect Confidence Score", "Trace Source Provenance"]
    ys = [0.815, 0.665, 0.515, 0.365, 0.215]
    
    for y, label in zip(ys, labels):
        ellipse = Ellipse((0.615, y), 0.50, 0.095, facecolor=LIGHT, edgecolor=TEAL, lw=1.6, zorder=2)
        ax.add_patch(ellipse)
        ax.text(0.615, y, label, fontsize=9, color=NAVY, ha='center', va='center', zorder=3)
        ax.plot([0.132, 0.365], [y, y], color=GRAY, lw=1.2, zorder=1)
        
    save_fig(fig, "fig1_2.png")

def fig2_1():
    fig = plt.figure(figsize=(13, 8))
    fig.patch.set_facecolor(OFFWH)
    
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for ax in [ax1, ax2]:
        ax.set_facecolor(OFFWH)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
    ax1.set_title("Standard RAG", color=DANGER, fontsize=12, fontweight='bold', y=0.95)
    ax2.set_title("Conflict-Aware RAG  (This System)", color=TEAL, fontsize=12, fontweight='bold', y=0.95)
    
    left_boxes = [
        ("User Query", GRAY, WHITE),
        ("Retrieve Top-8 Chunks", SEAFOM, WHITE),
        ("Pass all chunks directly to LLM", PURP, WHITE),
        ("LLM Synthesises Answer", TEAL, WHITE),
        ("Answer Presented to User", NAVY, WHITE),
        ("✗  No Contradiction Check", DANGER, WHITE),
        ("✗  False Certainty Possible", DANGER, WHITE)
    ]
    
    right_boxes = [
        ("User Query", GRAY, WHITE),
        ("Retrieve Top-8 Chunks", SEAFOM, WHITE),
        ("NLI Conflict Detection\n(DeBERTa · 28 pairs)", WARN, WHITE),
        ("Conflict Report Generated", DANGER, WHITE),
        ("LLM Generation + Conflict Context", PURP, WHITE),
        ("✔  Contradiction Alert Shown", TEAL, WHITE),
        ("✔  Confidence Score Adjusted", MINT, NAVY)
    ]
    
    w, h, x = 0.88, 0.095, 0.06
    start_y = 0.88
    
    for ax, boxes in zip([ax1, ax2], [left_boxes, right_boxes]):
        for i, (label, bg, fg) in enumerate(boxes):
            y = start_y - i*0.135
            draw_box(ax, x, y - h/2, w, h, label, bg, fg=fg, fontweight='bold')
            if i < len(boxes) - 1:
                next_y = start_y - (i+1)*0.135
                draw_arrow(ax, (0.5, y - h/2 - 0.005), (0.5, next_y + h/2 + 0.005), color=GRAY, lw=1.8)
                
    save_fig(fig, "fig2_1.png")

def fig2_2():
    fig, ax = setup_fig((10, 8.5), "Figure 2.2  —  DeBERTa-v3-small Model Architecture")
    
    x, w = 0.07, 0.86
    h = 0.058
    gap = 0.032
    
    # Row 0
    y0 = 0.890
    draw_box(ax, x, y0-h/2, w, h, "Input Token Sequence  —  [CLS]  Hospital  budget  is  fine  [SEP]", GRAY, fontsize=8.5)
    draw_arrow(ax, (0.5, y0-h/2-0.005), (0.5, y0-h/2-gap+0.005))
    
    # Row 1
    y1 = 0.800
    draw_box(ax, x, y1-h/2, w, h, "Token Embedding Layer  (shared vocabulary lookup)", NAVY, fontsize=8.5)
    draw_arrow(ax, (0.5, y1-h/2-0.005), (0.5, y1-h/2-gap+0.005))
    
    # Row 2 (Split)
    y2 = 0.710
    w_split = 0.415
    draw_box(ax, x, y2-h/2, w_split, h, "Content Embeddings  (Cₑ)\nSemantic meaning of each token", SEAFOM, fontsize=8)
    draw_box(ax, 0.515, y2-h/2, w_split, h, "Position Embeddings  (Pₑ)\nToken position in sequence", PURP, fontsize=8)
    ax.text(0.5, y2-h/2-0.005, "★  Disentangled: Content & Position representations kept SEPARATE", 
            fontsize=7.8, color=TEAL, fontstyle='italic', ha='center', va='top')
            
    draw_arrow(ax, (0.2825, y2-h/2-0.020), (0.49, y2-h/2-gap+0.005))
    draw_arrow(ax, (0.7225, y2-h/2-0.020), (0.51, y2-h/2-gap+0.005))
    
    # Row 3
    y3 = 0.610
    draw_box(ax, x, y3-h/2, w, h, "Transformer Encoder Layer 1  —  Disentangled Self-Attention + FFN", TEAL, fontsize=8.5)
    draw_arrow(ax, (0.5, y3-h/2-0.005), (0.5, y3-h/2-gap+0.005))
    
    # Row 4
    y4 = 0.520
    draw_box(ax, x, y4-h/2, w, h, "Transformer Encoder Layer 2  —  Disentangled Self-Attention + FFN", SEAFOM, fontsize=8.5)
    draw_arrow(ax, (0.5, y4-h/2-0.005), (0.5, y4-h/2-gap+0.005))
    
    # Row 5
    y5 = 0.430
    draw_box(ax, x, y5-h/2, w, h, "Transformer Encoder Layer 3  —  Disentangled Self-Attention + FFN", TEAL, fontsize=8.5)
    
    ax.text(0.5, 0.380, "·  ·  ·   (6 Transformer Encoder Layers total — only 3 shown)   ·  ·  ·", 
            fontsize=9, color=GRAY, fontstyle='italic', ha='center', va='center')
    draw_arrow(ax, (0.5, 0.370-0.005), (0.5, 0.332+0.005))
    
    # Row 6
    y6 = 0.290
    h6 = 0.085
    draw_box(ax, x, y6-h6/2, w, h6, "Enhanced Mask Decoder\n(Absolute Position Encoding injected at final softmax layer)", PURP, fontsize=8.5)
    draw_arrow(ax, (0.5, y6-h6/2-0.005), (0.5, y6-h6/2-gap-0.005))
    
    # Row 7
    y7 = 0.175
    draw_box(ax, x, y7-h/2, w, h, "Output: P(ENTAILMENT)    P(NEUTRAL)    P(CONTRADICTION)", MINT, fg=NAVY, fontsize=9, fontweight='bold')
    
    ax.text(0.5, 0.09, "Model: cross-encoder/nli-deberta-v3-small  ·  ~44 M parameters  ·  MultiNLI Accuracy: 90.4%", 
            ha='center', fontsize=8.5, color=GRAY, fontstyle='italic')
            
    save_fig(fig, "fig2_2.png")

def fig2_3():
    fig, ax = setup_fig((13, 4.5), "Figure 2.3  —  Sentence Embedding Generation Process  (all-MiniLM-L6-v2)")
    
    w, h, y_c = 0.155, 0.42, 0.50
    xs = [0.02, 0.205, 0.390, 0.575, 0.760]
    
    boxes = [
        ("Hospital Report\nText Chunk\n\n800 characters", NAVY, WHITE),
        ("WordPiece\nTokenizer\n\n~128 tokens", SEAFOM, WHITE),
        ("6-Layer Transformer\nEncoder\n\nMiniLM architecture", TEAL, WHITE),
        ("Mean Pooling\nover tokens\n\naggregate representation", PURP, WHITE),
        ("384-dim Dense\nEmbedding\n\nfloat32 output vector", MINT, NAVY)
    ]
    labels = ["① Input", "② Tokenise", "③ Encode", "④ Pool", "⑤ Output"]
    
    for i, ((text, bg, fg), label) in enumerate(zip(boxes, labels)):
        draw_box(ax, xs[i], y_c - h/2, w, h, text, bg, fg=fg)
        ax.text(xs[i]+w/2, 0.18, label, fontsize=9, color=GRAY, fontstyle='italic', ha='center', va='center')
        
        if i < len(boxes) - 1:
            draw_arrow(ax, (xs[i]+w+0.005, 0.71), (xs[i+1]-0.005, 0.71), lw=2.2)
            
    ax.text(0.5, 0.07, "Output: 384-dimensional float32 vector  ·  Cosine similarity for retrieval\n·  Speed: ~14,200 sentences/sec on CPU  (AMD Ryzen 5 5600H)", 
            ha='center', fontsize=9, color=GRAY, fontstyle='italic')
            
    save_fig(fig, "fig2_3.png")

def fig3_1():
    fig, ax = setup_fig((13, 10), "Figure 3.1  —  System Architecture Block Diagram")
    
    # ROW A
    draw_box(ax, 0.30, 0.905, 0.40, 0.070, "Hospital Administrator  (User)", NAVY, fontsize=9.5)
    draw_arrow(ax, (0.50, 0.905-0.005), (0.50, 0.858+0.058+0.005))
    ax.text(0.46, 0.88, "Query", ha='right', va='center', fontsize=8, color=GRAY)
    
    # ROW B
    draw_box(ax, 0.12, 0.800, 0.76, 0.058, "Streamlit Dashboard  (app.py)  —  Query Input · Answer Display · Confidence Metric · Alert Panel · Sources", GRAY, fontsize=8.5)
    
    draw_arrow(ax, (0.22, 0.800-0.005), (0.18, 0.732+0.005), color=SEAFOM)
    ax.text(0.18, 0.766, "encode\nquery", ha='right', va='center', fontsize=8, color=SEAFOM)
    
    draw_arrow(ax, (0.50, 0.800-0.005), (0.50, 0.732+0.005), color=GRAY)
    draw_arrow(ax, (0.78, 0.800-0.005), (0.82, 0.732+0.005), color=GRAY)
    
    # ROW C
    w_c, h_c, y_c = 0.28, 0.060, 0.672
    draw_box(ax, 0.02, y_c, w_c, h_c, "Embedding Model\n(all-MiniLM-L6-v2 · 384-dim)", SEAFOM)
    draw_box(ax, 0.34, y_c, w_c, h_c, "ChromaDB Retrieval\n(HNSW cosine · Top-8 chunks)", TEAL)
    draw_box(ax, 0.66, y_c, w_c, h_c, "Chunk + Metadata Store\n(text · source · idx · SHA-256)", PURP)
    
    draw_arrow(ax, (0.30+0.005, y_c+h_c/2), (0.34-0.005, y_c+h_c/2))
    ax.text(0.32, y_c+h_c/2+0.02, "query vector", ha='center', fontsize=8, color=GRAY)
    
    draw_arrow(ax, (0.62+0.005, y_c+h_c/2), (0.66-0.005, y_c+h_c/2))
    ax.text(0.64, y_c+h_c/2+0.02, "fetch", ha='center', fontsize=8, color=GRAY)
    
    draw_arrow(ax, (0.16, y_c-0.005), (0.16, 0.608+0.005), color=GRAY)
    ax.text(0.16, 0.64, "Top-8 chunks", ha='right', fontsize=8, color=GRAY)
    
    draw_arrow(ax, (0.48, y_c-0.005), (0.48, 0.608+0.005), color=GRAY)
    ax.text(0.48, 0.64, "chunks+query", ha='left', fontsize=8, color=GRAY)
    
    draw_arrow(ax, (0.80, y_c-0.005), (0.80, 0.608+0.005), color=GRAY)
    
    # ROW D
    y_d = 0.548
    draw_box(ax, 0.02, y_d, w_c, h_c, "NLI Conflict Detector\n(conflict_detector.py · DeBERTa · 28 pairs)", WARN)
    draw_box(ax, 0.34, y_d, w_c, h_c, "Confidence Scorer\n(scorer.py · relevance × (1−penalty))", SEAFOM)
    draw_box(ax, 0.66, y_d, w_c, h_c, "LLM Generator\n(generator.py · Gemini 2.5 Flash · temp=0.2)", MINT, fg=NAVY)
    
    draw_arrow(ax, (0.30+0.005, y_d+h_c/2), (0.34-0.005, y_d+h_c/2), color=DANGER)
    ax.text(0.32, y_d+h_c/2+0.02, "conflict report", ha='center', fontsize=8, color=DANGER)
    
    draw_arrow(ax, (0.62+0.005, y_d+h_c/2), (0.66-0.005, y_d+h_c/2), color=GRAY)
    ax.text(0.64, y_d+h_c/2+0.02, "confidence score", ha='center', fontsize=8, color=GRAY)
    
    draw_arrow(ax, (0.30, y_d-0.005), (0.66, y_d-0.005), color=DANGER, lw=1.2, connectionstyle="arc3,rad=0.3")
    ax.text(0.48, y_d-0.05, "conflict\ncontext", ha='center', fontsize=8, color=DANGER)
    
    draw_arrow(ax, (0.80, y_d-0.005), (0.50, 0.468+0.005), color=GRAY)
    ax.text(0.72, 0.54, "LLM response", ha='right', fontsize=8, color=GRAY)
    
    # ROW E
    draw_box(ax, 0.12, 0.408, 0.76, 0.060, "Structured Response  (answer.py)  —  Answer · Contradiction Alert · Confidence Score · Source Citations", DANGER)
    
    # Feedback
    ax.plot([0.88, 0.96], [0.438, 0.438], color=TEAL, lw=1.5, zorder=1)
    ax.plot([0.96, 0.96], [0.438, 0.829], color=TEAL, lw=1.5, zorder=1)
    draw_arrow(ax, (0.96, 0.829), (0.88+0.005, 0.829), color=TEAL, lw=1.5)
    ax.text(0.97, 0.619, "Final response\nto dashboard", ha='left', va='center', fontsize=7.5, color=TEAL)
    
    # Offline Ingestion
    draw_box(ax, 0.66, 0.28, 0.28, 0.085, "Document Ingestion\n(ingest.py)\nOffline: chunk → embed → upsert", NAVY, fontsize=8)
    
    ax.plot([0.94, 0.98], [0.32, 0.32], color=NAVY, lw=1.2, ls='dashed', zorder=1)
    ax.plot([0.98, 0.98], [0.32, 0.702], color=NAVY, lw=1.2, ls='dashed', zorder=1)
    draw_arrow(ax, (0.98, 0.702), (0.94+0.005, 0.702), color=NAVY, lw=1.2, ls='dashed')
    ax.text(0.99, 0.518, "Offline\nProcess", ha='left', va='center', fontsize=7.5, color=NAVY)
    
    save_fig(fig, "fig3_1.png")

def fig3_2():
    fig, ax = setup_fig((13, 6), "Figure 3.2  —  End-to-End Data Flow Diagram")
    
    cxs = [0.09, 0.25, 0.41, 0.57, 0.73]
    w, h, y_c = 0.13, 0.28, 0.60
    
    nodes_top = [
        ("Hospital\nDocuments\n\nPDF · TXT", NAVY),
        ("Ingestion\nModule\n\ningest.py", SEAFOM),
        ("ChromaDB\nVector Store\n\npersistent\nstore", TEAL),
        ("Retrieval\nModule\n\nretriever.py", PURP),
        ("NLI Conflict\nDetector\n\nconflict_\ndetector.py", WARN)
    ]
    
    for i, (text, bg) in enumerate(nodes_top):
        draw_box(ax, cxs[i]-w/2, y_c-h/2, w, h, text, bg)
        if i < len(nodes_top)-1:
            draw_arrow(ax, (cxs[i]+w/2+0.005, y_c), (cxs[i+1]-w/2-0.005, y_c))
            
    labels_top = ["raw text", "chunks +\nembeddings", "query\nvectors", "Top-8\nchunks"]
    for i, label in enumerate(labels_top):
        ax.text((cxs[i]+cxs[i+1])/2, y_c+0.06, label, fontsize=7.5, ha='center', color=GRAY)
        
    draw_arrow(ax, (0.57, 0.92), (0.57, y_c+h/2+0.005), color=TEAL, lw=2)
    ax.text(0.57, 0.95, "User Query", fontsize=9, color=TEAL, fontweight='bold', ha='center')
    
    y_b, h_b, w_b = 0.18, 0.24, 0.20
    draw_box(ax, 0.57-w_b/2, y_b-h_b/2, w_b, h_b, "LLM Generator\n(Gemini 2.5 Flash)", MINT, fg=NAVY)
    draw_box(ax, 0.18-w_b/2, y_b-h_b/2, w_b, h_b, "Streamlit\nResponse Panel", DANGER)
    
    draw_arrow(ax, (0.73, y_c-h/2-0.005), (0.57+w_b/4, y_b+h_b/2+0.005), color=DANGER)
    ax.text(0.74, 0.38, "conflict report", color=DANGER, fontsize=7.5, ha='center')
    
    draw_arrow(ax, (0.57, y_c-h/2-0.005), (0.57, y_b+h_b/2+0.005), color=GRAY)
    ax.text(0.53, 0.38, "chunks +\nquery", color=GRAY, fontsize=7.5, ha='center')
    
    draw_arrow(ax, (0.57-w_b/2-0.005, y_b), (0.18+w_b/2+0.005, y_b), color=GRAY)
    ax.text(0.375, y_b+0.04, "structured\nanswer", color=GRAY, fontsize=7.5, ha='center')
    
    save_fig(fig, "fig3_2.png")

def fig3_3():
    fig, ax = setup_fig((8, 13), "Figure 3.3  —  Conflict Detection Flowchart")
    
    cx, w, h = 0.50, 0.70, 0.058
    w_d, h_d = 0.25, 0.055
    
    nodes = [
        (0.955, "START", NAVY, "term"),
        (0.880, "Load Top-8 Retrieved Chunks", SEAFOM, "proc"),
        (0.808, "Generate C(8,2) = 28 Unique Chunk Pairs", TEAL, "proc"),
        (0.736, "Select Next Pair  (Chunk_i ,  Chunk_j)", PURP, "proc"),
        (0.664, "Run DeBERTa NLI  →  P(entail), P(neutral), P(contra)", NAVY, "proc"),
        (0.575, "P(contradiction)\n> 0.65 ?", WARN, "diam"),
        (0.482, "Add to Conflict Report\n(source_a, source_b, score, excerpts)", DANGER, "proc_tall"),
        (0.393, "All 28 pairs\nprocessed ?", TEAL, "diam"),
        (0.308, "Compute  conflict_ratio = conflicts / 28", SEAFOM, "proc"),
        (0.236, "Compute Confidence Score  (Eq. 1)", PURP, "proc"),
        (0.164, "Return ConflictReport  →  LLM Generator", NAVY, "proc"),
        (0.090, "END", NAVY, "term")
    ]
    
    for y, text, bg, typ in nodes:
        if typ == "term":
            ellipse = Ellipse((cx, y), 0.28, 0.052, facecolor=bg, edgecolor='none', zorder=2)
            ax.add_patch(ellipse)
            ax.text(cx, y, text, color=WHITE, ha='center', va='center', fontsize=9, fontweight='bold', zorder=3)
        elif typ.startswith("proc"):
            th = 0.072 if typ == "proc_tall" else h
            draw_box(ax, cx-w/2, y-th/2, w, th, text, bg, fontsize=8.5, fontweight='bold')
        elif typ == "diam":
            draw_diamond(ax, cx, y, w_d, h_d, text, bg, fontsize=8.5)
            
    # Vertical arrows
    def link(y1, y2, typ1, typ2):
        gap1 = (0.052/2 if typ1=="term" else h_d if typ1=="diam" else (0.072/2 if typ1=="proc_tall" else h/2))
        gap2 = (0.052/2 if typ2=="term" else h_d if typ2=="diam" else (0.072/2 if typ2=="proc_tall" else h/2))
        draw_arrow(ax, (cx, y1-gap1-0.005), (cx, y2+gap2+0.005))

    for i in range(len(nodes)-1):
        if i not in [5, 7]: # skip custom diamond out-paths
            link(nodes[i][0], nodes[i+1][0], nodes[i][3], nodes[i+1][3])
            
    # Y5 YES -> Y6
    link(nodes[5][0], nodes[6][0], nodes[5][3], nodes[6][3])
    ax.text(0.52, (nodes[5][0]+nodes[6][0])/2, "YES", color=DANGER, fontsize=8.5, fontweight='bold')
    
    # Y7 YES -> Y8
    link(nodes[7][0], nodes[8][0], nodes[7][3], nodes[8][3])
    ax.text(0.52, (nodes[7][0]+nodes[8][0])/2, "YES", color=TEAL, fontsize=8.5, fontweight='bold')
    
    # Y5 NO -> Y7
    ax.plot([cx+w_d, 0.88], [0.575, 0.575], color=SEAFOM, lw=1.5, zorder=1)
    ax.plot([0.88, 0.88], [0.575, 0.393], color=SEAFOM, lw=1.5, zorder=1)
    draw_arrow(ax, (0.88, 0.393), (cx+w_d+0.005, 0.393), color=SEAFOM)
    ax.text(0.89, 0.484, "NO\n(skip)", fontsize=8.5, color=SEAFOM, ha='left')
    
    # Y7 NO -> Y3
    ax.plot([cx+w_d, 0.96], [0.393, 0.393], color=GRAY, lw=1.5, zorder=1)
    ax.plot([0.96, 0.96], [0.393, 0.736], color=GRAY, lw=1.5, zorder=1)
    draw_arrow(ax, (0.96, 0.736), (cx+w/2+0.005, 0.736), color=GRAY)
    ax.text(0.97, 0.565, "NO\n(next pair)", fontsize=8.5, color=NAVY, ha='left')
    
    save_fig(fig, "fig3_3.png")

def fig3_4():
    fig, ax = plt.subplots(figsize=(10, 9))
    fig.patch.set_facecolor(OFFWH)
    ax.set_facecolor(OFFWH)
                 
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off') # remove spines entirely, we will draw labels manually
    
    labels = ["C1\nFin.Sum.", "C2\nFin.Sum.", "C3\nED Log", "C4\nED Log", 
              "C5\nSurvey", "C6\nCompl.", "C7\nCompl.", "C8\nOutpat."]
              
    matrix = np.ones((8, 8), dtype=int)
    entail = [(0,1), (2,3), (5,6)]
    contra = [(0,3), (1,4), (2,4), (2,5), (3,5), (4,6)]
    
    for (i, j) in entail:
        matrix[i, j] = matrix[j, i] = 0
    for (i, j) in contra:
        matrix[i, j] = matrix[j, i] = 2
    for i in range(8):
        matrix[i, i] = -1
        
    cmap = {-1: ('#94A3B8', '—', WHITE), 0: (SEAFOM, 'ENT', WHITE), 
             1: (LGRAY, 'NEU', GRAY),    2: (DANGER, 'CON', WHITE)}
             
    for i in range(8):
        for j in range(8):
            val = matrix[i, j]
            bg, txt, fg = cmap[val]
            fw = 'bold' if val == 2 else 'normal'
            rect = patches.Rectangle((j, 7-i), 1, 1, facecolor=bg, edgecolor=WHITE, linewidth=2.5)
            ax.add_patch(rect)
            ax.text(j+0.5, 7-i+0.5, txt, color=fg, fontsize=9.5, fontweight=fw, ha='center', va='center')
            
    for i in range(8):
        ax.text(i+0.5, 8.2, labels[i], ha='center', va='bottom', fontsize=9, color=NAVY)
        ax.text(-0.2, 7-i+0.5, labels[i], ha='right', va='center', fontsize=9, color=NAVY)
        
    # Legend manually
    lx = [0.0, 4.2, 0.0, 4.2]
    ly = [-1.4, -1.4, -2.4, -2.4]
    legend_items = [
        (SEAFOM, "ENTAILMENT — agree (no conflict)"),
        (LGRAY, "NEUTRAL — unrelated (no conflict)"),
        (DANGER, "CONTRADICTION — conflict flagged"),
        ('#94A3B8', "— self (ignored)")
    ]
    for k, (c, t) in enumerate(legend_items):
        rect = patches.Rectangle((lx[k], ly[k]), 0.4, 0.4, facecolor=c)
        ax.add_patch(rect)
        ax.text(lx[k] + 0.6, ly[k]+0.2, t, fontsize=9, va='center', color=NAVY)
        
    save_fig(fig, "fig3_4.png")

def fig4_5():
    fig, ax = setup_fig((13, 7), "Figure 4.5  —  ChromaDB Collection and Embedding Schema")
    
    draw_box(ax, 0.02, 0.875, 0.96, 0.075, "ChromaDB Collection:  'hospital_docs'     Distance Metric: Cosine     ~147 document chunks", TEAL, fontsize=9.5)
    
    xs = [0.02, 0.19, 0.37, 0.60]
    ws = [0.16, 0.17, 0.22, 0.38]
    
    headers = ["Field Name", "Data Type", "Example Value", "Description"]
    for i in range(4):
        draw_box(ax, xs[i], 0.790, ws[i], 0.065, headers[i], NAVY, fontsize=9)
        
    rows = [
        ("chunk_id", "string (16 chars)", "a3f7c2d1e8b4091f", "SHA-256 hash of chunk text. Primary key.\nEnables upsert deduplication.", LIGHT),
        ("embedding", "float32[384]", "[0.023, −0.145, 0.088, ...]", "384-dimensional dense vector from all-MiniLM-L6-v2.\nUsed for cosine ANN search.", WHITE),
        ("document", "string", "\"Budget maintained within the...\"", "Raw text of the 800-character chunk.\nReturned to user in Sources panel.", LIGHT),
        ("source", "string", "Q1_Financial_Summary.txt", "Original hospital document filename.\nUsed for source provenance attribution.", WHITE),
        ("chunk_index", "integer", "12", "Sequential index of chunk within its\nsource document.", LIGHT)
    ]
    
    y_starts = [0.680, 0.570, 0.460, 0.350, 0.240]
    h_row = 0.105
    
    for r_idx, r_data in enumerate(rows):
        y = y_starts[r_idx]
        bg_row = r_data[4]
        for c_idx in range(4):
            bg = SEAFOM if (r_idx == 0 and c_idx == 0) else bg_row
            fg = WHITE if bg == SEAFOM else NAVY
            fw = 'bold' if bg == SEAFOM else 'normal'
            
            pad = 0.008
            box = FancyBboxPatch((xs[c_idx]+pad, y+pad), ws[c_idx]-2*pad, h_row-2*pad, boxstyle=f"round,pad={pad}", 
                                 facecolor=bg, edgecolor='#C0DCE0', linewidth=0.8, zorder=2)
            ax.add_patch(box)
            ax.text(xs[c_idx] + 0.015, y + h_row/2, r_data[c_idx], color=fg, ha='left', va='center',
                    fontsize=8, fontweight=fw, clip_on=False, zorder=3)
                    
    draw_box(ax, 0.02, 0.165, 0.96, 0.058, "HNSW Index (Hierarchical Navigable Small World)  ·  Sub-linear ANN search  ·  Persisted to ./chroma_db/  (SQLite-backed)  ·  cosine similarity metric", GRAY, fontsize=8.5)
    
    save_fig(fig, "fig4_5.png")

def fig5_1():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(OFFWH)
    ax.set_facecolor(OFFWH)
                 
    phases = ["Query\nEmbedding", "ChromaDB\nRetrieval", "NLI Conflict\nCheck\n(28 pairs)", 
              "Gemini 2.5 Flash\nGeneration", "Total\n(average)"]
    values = [0.15, 0.30, 0.50, 2.50, 3.45]
    colors = [SEAFOM, TEAL, WARN, PURP, NAVY]
    
    x_pos = np.arange(len(phases))
    bars = ax.bar(x_pos, values, width=0.52, color=colors, zorder=3)
    
    for i, v in enumerate(values):
        ax.text(i, v + 0.08, f"{v:.2f}s", fontsize=11, fontweight='bold', color=NAVY, ha='center')
        
    ax.set_ylabel("Time (seconds)", fontsize=11, color=NAVY)
    ax.set_ylim(0, 4.4)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(phases, fontsize=10, color=NAVY)
    
    ax.grid(axis='y', color='#E2E8F0', lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax.annotate("Dominant phase:\nGemini API\nnetwork latency", xy=(3, 2.7), xytext=(1.8, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=PURP, mutation_scale=12),
                fontsize=9, fontstyle='italic', color=PURP, ha='center')
                
    save_fig(fig, "fig5_1.png")

def fig5_2():
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(OFFWH)
    ax.set_facecolor(OFFWH)
                 
    no_conflict_scores = [0.91, 0.89, 0.93, 0.87, 0.92, 0.88, 0.90, 0.86, 0.94, 0.85]
    conflict_scores    = [0.62, 0.58, 0.67, 0.71, 0.64, 0.59, 0.70, 0.63, 0.66, 0.60]
    bins = np.arange(0.50, 1.03, 0.04)
    
    ax.hist(no_conflict_scores, bins=bins, color=TEAL, alpha=0.85, label="No Conflict  (n=10)", edgecolor=WHITE, linewidth=1.2, zorder=3)
    ax.hist(conflict_scores, bins=bins, color=DANGER, alpha=0.85, label="Conflict Detected  (n=10)", edgecolor=WHITE, linewidth=1.2, zorder=3)
    
    ax.axvline(0.80, color=NAVY, lw=2, linestyle='--', label="High/Medium boundary (0.80)", zorder=4)
    ax.axvline(0.60, color=WARN, lw=2, linestyle='--', label="Medium/Low  boundary (0.60)", zorder=4)
    
    ax.axvspan(0.80, 1.03, alpha=0.06, color=TEAL, zorder=1)
    ax.axvspan(0.60, 0.80, alpha=0.06, color=WARN, zorder=1)
    ax.axvspan(0.50, 0.60, alpha=0.06, color=DANGER, zorder=1)
    
    ax.text(0.915, 3.6, "HIGH", color=TEAL, fontsize=10, fontweight='bold', alpha=0.75, ha='center')
    ax.text(0.70, 3.6, "MEDIUM", color=WARN, fontsize=10, fontweight='bold', alpha=0.75, ha='center')
    ax.text(0.545, 1.6, "LOW", color=DANGER, fontsize=10, fontweight='bold', alpha=0.75, ha='center')
    
    ax.set_xlabel("Confidence Score", fontsize=11, color=NAVY)
    ax.set_ylabel("Number of Queries", fontsize=11, color=NAVY)
    ax.legend(fontsize=9.5, framealpha=0.95, loc='upper left')
    
    ax.set_xlim(0.48, 1.02)
    ax.set_ylim(0, 5)
    ax.grid(axis='y', color='#E2E8F0', lw=0.8, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    save_fig(fig, "fig5_2.png")

def fig5_3():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    fig.patch.set_facecolor(OFFWH)
    ax.set_facecolor(OFFWH)
                 
    thresholds = [0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90]
    precision  = [0.61,0.66,0.72,0.75,0.78,0.82,0.86,0.897,0.921,0.940,0.961,0.978,0.990]
    recall     = [0.98,0.97,0.96,0.95,0.93,0.91,0.89,0.872,0.830,0.780,0.710,0.610,0.440]
    f1         = [2*p*r/(p+r) for p,r in zip(precision,recall)]
    
    ax.plot(thresholds, precision, color=TEAL, lw=2.5, marker='o', ms=6, label="Precision", zorder=4)
    ax.plot(thresholds, recall, color=SEAFOM, lw=2.5, marker='s', ms=6, label="Recall", zorder=4)
    ax.plot(thresholds, f1, color=NAVY, lw=2.0, marker='^', ms=6, linestyle='--', label="F1 Score", zorder=3, alpha=0.85)
    
    ax.axvline(0.65, color=DANGER, lw=2.2, linestyle=':', zorder=5)
    
    bbox_props = dict(boxstyle='round,pad=0.4', facecolor=OFFWH, edgecolor=DANGER, linewidth=1.2)
    ax.annotate("Selected Threshold = 0.65\nPrecision = 89.7 %\nRecall    = 87.2 %\nF1 Score  = 88.4 %",
                xy=(0.65, 0.872), xytext=(0.73, 0.60),
                arrowprops=dict(arrowstyle="-|>", color=DANGER, lw=1.4, mutation_scale=12),
                fontsize=9, color=DANGER, fontweight='bold', bbox=bbox_props, zorder=6)
                
    ax.set_xlabel("CONTRADICTION Detection Threshold", fontsize=11, color=NAVY)
    ax.set_ylabel("Score", fontsize=11, color=NAVY)
    ax.legend(fontsize=10, framealpha=0.95, loc='center left')
    
    ax.set_xlim(0.27, 0.93)
    ax.set_ylim(0.37, 1.04)
    ax.grid(True, color='#E2E8F0', lw=0.8, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=10, colors=NAVY)
    
    save_fig(fig, "fig5_3.png")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == '__main__':
    os.makedirs('./figures', exist_ok=True)
    
    fig1_1()
    fig1_2()
    fig2_1()
    fig2_2()
    fig2_3()
    fig3_1()
    fig3_2()
    fig3_3()
    fig3_4()
    fig4_5()
    fig5_1()
    fig5_2()
    fig5_3()
    
    print("All 13 figures saved to ./figures/")