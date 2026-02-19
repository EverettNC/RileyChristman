"""
Vector8 Orchestrator: The Brain
Standard: 96% Quality Threshold
Real 8-dimensional truth vector via sentence-transformers embeddings.
"""
import logging
import numpy as np
from typing import Tuple, Dict

try:
    from sentence_transformers import SentenceTransformer
    _model = SentenceTransformer("all-MiniLM-L6-v2")
    _ST_AVAILABLE = True
except Exception:
    _model = None
    _ST_AVAILABLE = False

# Eight conceptual axes Riley measures truth along
AXIS_ANCHORS = {
    "truth":   "This is factually accurate and verifiable.",
    "empathy": "I understand your pain and I am with you.",
    "logic":   "The evidence and reasoning are sound.",
    "courage": "This requires bravery to face and act upon.",
    "past":    "This is rooted in memory and what has happened before.",
    "future":  "This points toward what is coming and what can be built.",
    "self":    "This is about who I am and my own identity.",
    "other":   "This is about the people around me and their needs.",
}

_axis_embeddings: Dict[str, np.ndarray] = {}

def _get_axis_embeddings():
    global _axis_embeddings
    if not _axis_embeddings and _ST_AVAILABLE:
        texts = list(AXIS_ANCHORS.values())
        embs = _model.encode(texts, normalize_embeddings=True)
        for key, emb in zip(AXIS_ANCHORS.keys(), embs):
            _axis_embeddings[key] = emb
    return _axis_embeddings


class Vector8Orchestrator:
    def __init__(self):
        if _ST_AVAILABLE:
            _get_axis_embeddings()
            logging.info("🧠 Vector8: sentence-transformers LIVE. 8-axis truth mapping active.")
        else:
            logging.warning("🧠 Vector8: sentence-transformers unavailable — fallback active.")

    def vector_out(self, user_input: str) -> Tuple[str, str, Dict[str, float]]:
        """
        Projects user_input into the 8-dimensional truth space via cosine
        similarity against conceptual anchor sentences.
        Returns (specialist, resonance, truth_vector).
        """
        if _ST_AVAILABLE:
            input_emb = _model.encode([user_input], normalize_embeddings=True)[0]
            axes = _get_axis_embeddings()
            truth_vector = {
                axis: float(np.clip(np.dot(input_emb, axes[axis]), 0.0, 1.0))
                for axis in axes
            }
        else:
            # Keyword fallback — real scoring without the model
            low = user_input.lower()
            truth_vector = {
                "truth":   0.9 if any(w in low for w in ["true","fact","verify","real","evidence"]) else 0.4,
                "empathy": 0.9 if any(w in low for w in ["feel","hurt","pain","love","miss","lost"]) else 0.4,
                "logic":   0.9 if any(w in low for w in ["because","therefore","reason","proof","calculate"]) else 0.4,
                "courage": 0.9 if any(w in low for w in ["fight","stand","brave","face","protect"]) else 0.4,
                "past":    0.9 if any(w in low for w in ["remember","before","history","was","used to"]) else 0.4,
                "future":  0.9 if any(w in low for w in ["will","plan","build","next","goal"]) else 0.4,
                "self":    0.9 if any(w in low for w in ["i am","myself","identity","who i"]) else 0.4,
                "other":   0.9 if any(w in low for w in ["they","you","family","friend","people"]) else 0.4,
            }

        # Dominant axis determines specialist
        dominant = max(truth_vector, key=lambda k: truth_vector[k])
        specialist_map = {
            "truth": "Forensic", "empathy": "AlphaWolf", "logic": "Analyst",
            "courage": "Inferno", "past": "Memory", "future": "Architect",
            "self": "Mirror", "other": "AlphaVox",
        }
        specialist = specialist_map.get(dominant, "Analyst")

        avg = float(np.mean(list(truth_vector.values())))
        resonance = "High" if avg > 0.7 else ("Stable" if avg > 0.5 else "Low")

        return specialist, resonance, truth_vector
