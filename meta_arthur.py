"""
Meta Arthur (Omni-Router)
Standard: 96% Quality Threshold
Integrates: Real FFT Signal Triage + Specialist Routing
"""

import logging
import numpy as np
from typing import Dict, Any

try:
    from sentence_transformers import SentenceTransformer, util as st_util
    _st_model = SentenceTransformer("all-MiniLM-L6-v2")
    _ST_AVAILABLE = True
except Exception:
    _st_model = None
    _ST_AVAILABLE = False

# Specialist routing anchors for semantic vortex prediction
_SPECIALIST_ANCHORS = {
    "Inferno":  "Trauma, crisis, suicide risk, dissociation, acute distress.",
    "AlphaVox": "Non-verbal cues, tone of voice, paralinguistic signals.",
    "Vector8":  "Logic, strategy, analysis, data, reasoning, calculation.",
    "Quantum":  "Emotional collapse, grief, identity, love, deep loss.",
}
_specialist_embs: Dict[str, Any] = {}

def _load_specialist_embs():
    global _specialist_embs
    if not _specialist_embs and _ST_AVAILABLE:
        for name, text in _SPECIALIST_ANCHORS.items():
            _specialist_embs[name] = _st_model.encode(text, normalize_embeddings=True)
    return _specialist_embs


class NeuroSymbolicOrchestrator:
    def __init__(self):
        if _ST_AVAILABLE:
            _load_specialist_embs()
        logging.info("🧠 NeuroSymbolic Orchestrator: Online.")
        self.specialists = {
            "Inferno":  "Trauma/Response",
            "AlphaVox": "Non-verbal/Truth",
            "Vector8":  "Logic/Strategy",
            "Quantum":  "Emotional Collapse",
        }

    def signal_triage(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Real FFT analysis of raw PCM audio bytes.
        Computes dominant frequency band and RMS energy to determine routing.
        """
        if not audio_data:
            return {"signal_level": 0, "mode": "silence", "dominant_hz": 0, "rms": 0.0}

        # Convert raw bytes → float32 waveform
        audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        if audio_array.size == 0:
            return {"signal_level": 0, "mode": "empty", "dominant_hz": 0, "rms": 0.0}

        audio_array /= 32768.0
        sample_rate = 16000  # assumed PCM 16kHz

        # RMS energy
        rms = float(np.sqrt(np.mean(audio_array ** 2)))

        # FFT — find dominant frequency
        fft_mag = np.abs(np.fft.rfft(audio_array))
        freqs = np.fft.rfftfreq(len(audio_array), d=1.0 / sample_rate)
        dominant_hz = float(freqs[np.argmax(fft_mag)])

        # Signal level 0–100 scaled from RMS
        signal_level = int(min(rms * 200, 100))

        # Route based on energy and dominant frequency
        if rms < 0.01:
            mode = "silence"
        elif dominant_hz < 150:
            mode = "low_rumble"
        elif dominant_hz < 500:
            mode = "speech"
        elif dominant_hz < 2000:
            mode = "elevated_speech"
        else:
            mode = "noise"

        return {
            "signal_level": signal_level,
            "mode": mode,
            "dominant_hz": round(dominant_hz, 1),
            "rms": round(rms, 4),
        }

    def make_vortex_prediction(self, user_input: str) -> Dict[str, Any]:
        """
        Semantic routing: embed user_input, compare to specialist anchors,
        route to the most aligned specialist.
        """
        if _ST_AVAILABLE:
            anchors = _load_specialist_embs()
            input_emb = _st_model.encode(user_input, normalize_embeddings=True)
            scores = {
                name: float(st_util.cos_sim(input_emb, emb))
                for name, emb in anchors.items()
            }
            routing = max(scores, key=scores.get)
            valence = scores[routing]
        else:
            # Keyword fallback
            low = user_input.lower()
            scores = {
                "Inferno":  sum(1 for w in ["crisis","suicid","dissociat","danger","hurt"] if w in low),
                "AlphaVox": sum(1 for w in ["voice","tone","sound","heard","listen"] if w in low),
                "Vector8":  sum(1 for w in ["calculate","reason","logic","data","fact"] if w in low),
                "Quantum":  sum(1 for w in ["love","grief","miss","broken","legacy","family"] if w in low),
            }
            routing = max(scores, key=scores.get) if any(scores.values()) else "Vector8"
            valence = 0.95 if scores.get(routing, 0) > 1 else 0.5

        return {
            "prediction": "resonance",
            "score": float(np.clip(valence, 0.0, 1.0)),
            "routing": routing,
            "specialist_scores": {k: round(float(v), 3) for k, v in scores.items()},
        }
