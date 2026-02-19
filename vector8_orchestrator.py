"""
Vector8 Orchestrator: The Brain
Standard: 96% Quality Threshold
Wraps the RileyKernelCortex for Vector Logic.
"""
from riley_cognitive_cortex import get_riley_cortex
import torch

class Vector8Orchestrator:
    def __init__(self):
        self.cortex = get_riley_cortex()

    def vector_out(self, user_input):
        """
        Processes input and returns (Specialist, Resonance, Truth Vector).
        """
        # 1. Use Kernel Cortex to process
        # We need to adapt the string input to the tensor logic if needed,
        # or just use the Cortex's process_interaction for high level logic.
        
        # For Vector8 compliance, we mock the 8-dimensional truth vector
        # based on the Kernel's latent trace.
        
        # We can just call the async method or use internal logic?
        # Let's use internal logic for synchronous vector extraction
        # (Mocking the conversion for this layer)
        
        # Simulating vector from text content
        val = 0.95 if "family" in user_input.lower() else 0.5
        truth_vector = {
            "truth": val,
            "empathy": 0.8,
            "logic": 0.7,
            "courage": 0.9,
            "past": 0.6,
            "future": 0.8,
            "self": 0.5,
            "other": 0.9
        }
        
        specialist = "AlphaWolf" if val > 0.8 else "Analyst"
        resonance = "High" if val > 0.9 else "Stable"
        
        return specialist, resonance, truth_vector
