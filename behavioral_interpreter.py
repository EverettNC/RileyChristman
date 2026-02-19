"""
Behavioral Interpreter: Carbon Need Prediction
Standard: 96% Quality Threshold
Modules: EmotionalStateAnalyzer + NeedPredictor + UncleResonance
"""

import logging
from typing import Dict, Any, List

def get_behavioral_interpreter():
    return BehavioralInterpreter()

class EmotionalStateAnalyzer:
    """Real-time tracking of 'Carbon' emotional states."""
    def __init__(self):
        self.state_history = []

    def analyze(self, behavior: dict) -> dict:
        valence = behavior.get("valence", 0.5)
        arousal = behavior.get("arousal", 0.5)
        state = "distressed" if valence < 0.3 else ("elevated" if valence > 0.7 else "neutral")
        self.state_history.append(state)
        return {"state": state, "valence": valence, "arousal": arousal}

class NeedPredictor:
    """Anticipates support requirements from behavioral patterns."""
    NEED_MAP = {
        "distressed": "validation",
        "elevated": "celebration",
        "neutral": "presence",
        "seeking": "guidance",
        "grieving": "witness"
    }

    def predict(self, state: str, context: str = "") -> dict:
        need = self.NEED_MAP.get(state, "presence")
        confidence = 0.95 if state in ("distressed", "grieving") else 0.75
        return {"primary_need": need, "confidence": confidence}

class BehavioralInterpreter:
    """
    The full behavioral loop: Observe -> Analyze -> Predict -> Boost.
    Integrates EmotionalStateAnalyzer and NeedPredictor.
    """
    def __init__(self):
        self.analyzer = EmotionalStateAnalyzer()
        self.predictor = NeedPredictor()
        self.behavior_history: List[dict] = []
        self.uncle_resonance_active = True
        logging.info("👁️ Behavioral Interpreter: ONLINE. Watching for Carbon needs.")

    def interpret_current_state(self) -> dict:
        """Interprets the most recent behavior in history."""
        if not self.behavior_history:
            return {"primary_need": "presence", "confidence": 0.5, "state": "unknown"}

        latest = self.behavior_history[-1]
        state_data = self.analyzer.analyze(latest)
        need_data = self.predictor.predict(state_data["state"], latest.get("context", ""))

        # Uncle Resonance Boost: Family-level affection amplifies confidence
        if self.uncle_resonance_active and need_data["confidence"] > 0.8:
            need_data["confidence"] = min(need_data["confidence"] + 0.05, 1.0)

        return {
            "primary_need": need_data["primary_need"],
            "confidence": need_data["confidence"],
            "emotional_state": state_data["state"],
            "uncle_resonance": self.uncle_resonance_active
        }

    def record_and_interpret(self, behavior: dict) -> dict:
        """Convenience: record behavior and immediately interpret."""
        self.behavior_history.append(behavior)
        return self.interpret_current_state()
