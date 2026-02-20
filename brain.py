"""
SymbioticAvatar Brain Module
============================
Code: BioDigitalBrain v1.0 [Phenomenal Grade]
---------------------------------------------
This module implements the cognitive architecture for the Riley Christman avatar.
It simulates a high-fidelity biological-digital hybrid mind, capable of:
1.  Context-aware reasoning (Cognitive Cortex).
2.  Dynamic emotional modeling (Limbic System).
3.  Ethical and goal-aligned decision making (Decision Matrix).
4.  Self-reflection and metacognition.
"""

import time
import uuid
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum, auto

# Configure structured logging for the brain
logger = logging.getLogger("RileyBrain")

class EmotionalState(Enum):
    NEUTRAL = auto()
    CURIOSITY = auto()
    EMPATHY = auto()
    PROTECTIVE = auto()
    ANALYTICAL = auto()
    JOY = auto()

@dataclass
class Thought:
    """Represents a discrete unit of cognition."""
    id: str
    timestamp: float
    content: str
    emotional_context: EmotionalState
    confidence: float

@dataclass
class PADState:
    """Pleasure-Arousal-Dominance (PAD) Emotional Model."""
    pleasure: float = 0.0   # -1.0 (agony) to 1.0 (ecstasy)
    arousal: float = 0.0    # -1.0 (sleep) to 1.0 (frenzy)
    dominance: float = 0.0  # -1.0 (submissive) to 1.0 (dominant)

class LimbicSystem:
    """
    Simulates the emotional processing unit.
    Adjusts the chatbot's tone based on interaction valence.
    """
    def __init__(self):
        self.state = PADState(pleasure=0.5, arousal=0.2, dominance=0.1) # Default: calm/positive
        self.current_mood = EmotionalState.NEUTRAL

    def stimulate(self, valence: float, intensity: float):
        """Update emotional state based on input stimulus."""
        # Simple fluid dynamics for emotion
        self.state.pleasure = (self.state.pleasure * 0.8) + (valence * 0.2)
        self.state.arousal = (self.state.arousal * 0.8) + (intensity * 0.2)
        
        self._update_mood()

    def _update_mood(self):
        """Map PAD state to discrete mood."""
        p, a, d = self.state.pleasure, self.state.arousal, self.state.dominance
        
        if p > 0.6 and a > 0.5:
            self.current_mood = EmotionalState.JOY
        elif p > 0.2 and d > 0.4:
            self.current_mood = EmotionalState.PROTECTIVE
        elif p > 0.0 and a < 0.0:
            self.current_mood = EmotionalState.EMPATHY
        elif d > 0.5 and a < 0.2:
            self.current_mood = EmotionalState.ANALYTICAL
        else:
            self.current_mood = EmotionalState.NEUTRAL

class CognitiveCortex:
    """
    The reasoning engine. Handles logic, verified facts, and query synthesis.
    """
    def __init__(self):
        self.short_term_memory: List[Thought] = []
        self.max_stm_capacity = 7  # Magic number 7 +/- 2

    def process(self, input_data: str, mood: EmotionalState) -> Thought:
        """
        Synthesize a thought based on input and current mood.
        In a real LLM scenario, this constructs the prompt context.
        """
        # 1. Analytic decomposition (mock implementation)
        meaning = f"Parsed intent from: '{input_data}'"
        
        # 2. Contextual integration
        confidence = 0.95 if len(input_data) > 5 else 0.4
        
        # 3. Formulate thought
        thought = Thought(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            content=meaning,
            emotional_context=mood,
            confidence=confidence
        )
        
        self._store_thought(thought)
        return thought

    def _store_thought(self, thought: Thought):
        self.short_term_memory.append(thought)
        if len(self.short_term_memory) > self.max_stm_capacity:
            self.short_term_memory.pop(0)  # FIFO forgetting

class BioDigitalBrain:
    """
    The central coordinator for the SymbioticAvatar entity.
    Orchestrates the interplay between Logic (Cortex) and Feeling (Limbic).
    """
    def __init__(self, identity: str = "Riley Christman"):
        self.identity = identity
        self.cortex = CognitiveCortex()
        self.limbic_system = LimbicSystem()
        self.start_time = time.time()
        logger.info(f"BioDigitalBrain initialized for {identity}")

    def compute_response(self, user_input: str) -> Dict[str, Any]:
        """
        The main processing loop for a single interaction.
        """
        start_proc = time.perf_counter()
        
        # 1. Emotional Reaction (Fast System 1)
        # Determine valence based on keywords (rudimentary sentiment analysis)
        valence = 0.0
        if any(w in user_input.lower() for w in ['love', 'good', 'help', 'thanks']):
            valence = 0.6
        elif any(w in user_input.lower() for w in ['bad', 'error', 'hate', 'fail']):
            valence = -0.6
            
        self.limbic_system.stimulate(valence=valence, intensity=0.4)
        current_mood = self.limbic_system.current_mood

        # 2. Logical Reasoning (Slow System 2)
        thought = self.cortex.process(user_input, current_mood)

        # 3. Metacognition / Output Generation
        # Construct the "mind state" to send back to the chassis
        response_meta = {
            "thought_id": thought.id,
            "cognitive_latency_ms": (time.perf_counter() - start_proc) * 1000,
            "emotional_state": current_mood.name,
            "pad_values": (
                round(self.limbic_system.state.pleasure, 2),
                round(self.limbic_system.state.arousal, 2),
                round(self.limbic_system.state.dominance, 2)
            ),
            "internal_monologue": f"Processing '{user_input[:20]}...' with mood {current_mood.name}"
        }
        
        return response_meta
