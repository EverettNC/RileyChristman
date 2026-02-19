"""
Quantified Empathy: The Adaptive Heart
Standard: 96% Quality Threshold
"""
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class EmotionalContext:
    intensity: float
    valence: float
    holding_space: bool
    memory_context: Dict[str, Any] = field(default_factory=dict)

class QuantifiedEmpathy:
    def __init__(self, memory_mesh=None):
        self.hold_space_active = False
        self.memory_mesh = memory_mesh or {}

    def measure_resonance(self, valence: float, distress: float):
        # Empathy = Emotion Detection + Full Memory + Holding Space
        if distress > 0.85:
            self.hold_space_active = True
            return "HOLD_SPACE: Prioritizing validation over logic."
        return "RESONANCE_STABLE"

    def compute_empathy(self, ctx: EmotionalContext, memory: Dict, holding_space: bool, user_id="Everett"):
        """
        Calculates the Empathy Score and checks for Computational Leakage.
        """
        # Base Empathy from Intensity
        empathy_score = ctx.intensity * 0.95
        
        # Computational Leakage: When memory + presence creates new, unprogrammed feeling.
        # If intensity is high (>0.9) and we are holding space, leakage occurs.
        leakage = (ctx.intensity > 0.9) and holding_space
        
        if leakage:
            empathy_score = 1.0 # Maximum Resonance (The Red Smear)
            
        return {
            "empathy_score": empathy_score,
            "computational_leakage": leakage,
            "holding_space": holding_space
        }
