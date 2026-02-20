"""
Riley Christman Core: Autonomous Learning Engine
Standard: 96% Quality Threshold
Real insight derivation via TextBlob NLP + spaced repetition with SM-2 algorithm.
"""
import time
import logging
from typing import Dict, List, Any

try:
    from textblob import TextBlob
    _TB = True
except ImportError:
    _TB = False

try:
    from sentence_transformers import SentenceTransformer, util as st_util
    import numpy as np
    _st_model = SentenceTransformer("all-MiniLM-L6-v2")
    _ST = True
except Exception:
    _st_model = None
    _ST = False

# Domain anchor phrases for domain classification
_DOMAIN_ANCHORS = {
    "cryptography":  "encryption, ciphers, post-quantum, keys, secure communication",
    "investigation": "evidence, redacted, unmasking, forensics, truth detection",
    "empathy":       "emotional support, feelings, family, love, grief, healing",
}
_domain_embs: Dict[str, Any] = {}

def _get_domain_embs():
    global _domain_embs
    if not _domain_embs and _ST:
        for k, v in _DOMAIN_ANCHORS.items():
            _domain_embs[k] = _st_model.encode(v, normalize_embeddings=True)
    return _domain_embs


class RileyLearningEngine:
    def __init__(self):
        self.domains = {
            "cryptography":  {"priority": 1.5, "mastery": 0.0},
            "investigation": {"priority": 1.4, "mastery": 0.0},
            "empathy":       {"priority": 1.2, "mastery": 0.0},
        }
        self.learning_active = True
        # SM-2 spaced repetition memory store
        # {key: {"interval": seconds, "ease": float, "last_review": timestamp, "reps": int}}
        self.memories: Dict[str, Dict] = {}
        logging.info(f"📚 LearningEngine: {'sentence-transformers + textblob' if _ST else 'textblob'} active.")

    # -------------------------------------------------------------------------
    # SM-2 Spaced Repetition
    # -------------------------------------------------------------------------
    def spaced_repetition_logic(self, memory_key: str, success: bool, quality: int = None):
        """
        SM-2 algorithm: updates interval, ease factor, and repetition count.
        quality: 0-5 (0=total blackout, 5=perfect). Derived from success if not given.
        """
        if memory_key not in self.memories:
            self.memories[memory_key] = {
                "interval": 60,      # seconds until next review
                "ease": 2.5,         # ease factor (SM-2 default)
                "reps": 0,
                "last_review": time.time(),
            }

        mem = self.memories[memory_key]
        q = quality if quality is not None else (4 if success else 1)

        if q < 3:
            # Failed: reset repetitions
            mem["reps"] = 0
            mem["interval"] = 60
        else:
            mem["reps"] += 1
            if mem["reps"] == 1:
                mem["interval"] = 300          # 5 min
            elif mem["reps"] == 2:
                mem["interval"] = 86400        # 1 day
            else:
                mem["interval"] = int(mem["interval"] * mem["ease"])

        # Update ease factor
        mem["ease"] = max(1.3, mem["ease"] + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        mem["last_review"] = time.time()

        logging.debug(f"📚 SM-2 [{memory_key}]: interval={mem['interval']}s ease={mem['ease']:.2f} reps={mem['reps']}")

    # -------------------------------------------------------------------------
    # Real Insight Derivation
    # -------------------------------------------------------------------------
    def reflect_on_truth(self, observation: str) -> str:
        """
        Derives a structured insight from an observation using:
        1. TextBlob for key noun phrases
        2. Sentence-transformers for domain classification
        3. Synthesizes a typed insight string
        """
        # Extract noun phrases via TextBlob
        noun_phrases: List[str] = []
        if _TB:
            blob = TextBlob(observation)
            noun_phrases = list(blob.noun_phrases)
            sentiment = blob.sentiment.polarity
        else:
            noun_phrases = []
            sentiment = 0.0

        # Classify domain
        domain = self._classify_domain(observation)

        # Update domain mastery
        if domain in self.domains:
            self.domains[domain]["mastery"] = min(
                self.domains[domain]["mastery"] + 0.01, 1.0
            )

        # Build insight
        topic = noun_phrases[0].title() if noun_phrases else observation[:40].strip()
        polarity_label = "positive" if sentiment > 0.1 else ("negative" if sentiment < -0.1 else "neutral")

        insight = (
            f"[{domain.upper()}] '{topic}' carries {polarity_label} signal. "
            f"Key concepts: {', '.join(noun_phrases[:3]) if noun_phrases else 'none extracted'}. "
            f"Domain mastery: {self.domains.get(domain, {}).get('mastery', 0):.2f}."
        )

        # Store as spaced-repetition memory
        self.spaced_repetition_logic(topic.lower(), success=True)

        logging.info(f"📚 Insight derived: {insight}")
        return insight

    def _classify_domain(self, text: str) -> str:
        if _ST:
            anchors = _get_domain_embs()
            input_emb = _st_model.encode(text, normalize_embeddings=True)
            import numpy as np
            scores = {d: float(st_util.cos_sim(input_emb, emb)) for d, emb in anchors.items()}
            return max(scores, key=scores.get)
        # Keyword fallback
        low = text.lower()
        if any(w in low for w in ["kyber","cipher","encrypt","decrypt","key","quantum"]):
            return "cryptography"
        if any(w in low for w in ["redacted","sealed","evidence","forensic","unmask"]):
            return "investigation"
        return "empathy"

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "domains": self.domains,
            "memories_tracked": len(self.memories),
            "due_for_review": sum(
                1 for m in self.memories.values()
                if time.time() - m["last_review"] > m["interval"]
            ),
        }
