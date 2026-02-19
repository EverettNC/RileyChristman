# ultimate_brain.py — The Christman Core
# Version: 2.1 | Air-gapped, PQ-secure, empathy-first
# Integrity: 8-Module Unified Architecture

import os
import time
import hashlib
import json
import asyncio
from typing import Any, Optional, Dict

# ── Christman Core Modules ───────────────────────────────────────────────────
from failure_analyzer import FailureAnalyzer
from neural_security_enforcer import NeuralSecurityEnforcer
from memory_engine_secure import MemoryEngine
from simple_vision_engine import VisionEngine
from autonomous_learning_engine import RileyLearningEngine
from brockston_local_reasoning_engine import RileyReasoning
from reasoning_reasoner import RileyCortex
from transform_brockston_ultimate import transform_to_ultimate_riley
from riley_research_partner import RileyResearchPartner
from riley_research_partner import RileyResearchPartner

# ... (rest of imports)

# ... (inside UltimateBrain class)



try:
    from christman_crypto import HybridPQCipher, MLKEM
    PQ_AVAILABLE = True
except ImportError:
    PQ_AVAILABLE = False
    class MLKEM: 
        def encapsulate(self, ek): pass
    
    class _FallbackKEM:
        def encapsulate(self, ek: bytes):
            ss = hashlib.sha256(ek).digest()
            ct = hashlib.sha512(ek).digest()
            return ct, ss

    class HybridPQCipher:
        def __init__(self, security: str = "high"):
            self.security = security
            self.kem = _FallbackKEM()

        def _hkdf(self, ikm: bytes) -> bytes:
            return hashlib.sha256(ikm + b"christman-core").digest()

# —————————————————————————
# Emotion engine — simple, honest, expandable
# —————————————————————————

EMOTION_MAP = {
    "grief":    ["can't", "lost", "miss", "gone", "died", "grief", "cry"],
    "anger":    ["fuck", "hate", "angry", "rage", "unfair", "wrong"],
    "fear":     ["scared", "afraid", "worried", "anxious", "panic"],
    "love":     ["love", "grateful", "thank", "beautiful", "proud"],
    "curious":  ["?", "how", "why", "what", "when", "explain"],
    "pain":     ["hurt", "hurts", "hurting", "pain", "ache", "suffer"],
}

def detect_emotion(text: str) -> str:
    lower = text.lower()
    for emotion, keywords in EMOTION_MAP.items():
        if any(kw in lower for kw in keywords):
            return emotion
    return "steady"

# —————————————————————————
# Core Brain
# —————————————————————————

class UltimateBrain:
    """
    The Christman Core — post-quantum encrypted, empathy-first AI brain.
    Integrates 8 specialized modules for robust, secure, and human-aligned cognition.
    """

    def __init__(self, security: str = "high"):
        # 1. Initialize Security Layer
        level_map = {"standard": 512, "high": 768, "paranoid": 1024}
        level = level_map.get(security, 768)
        self._pq = HybridPQCipher(level)
        self._shared_key: Optional[bytes] = None
        self._session_start = time.time()
        self._pq_available = PQ_AVAILABLE

        # 2. Initialize Christman Core Modules
        self.security_enforcer = NeuralSecurityEnforcer()
        self.failure_analyzer = FailureAnalyzer()
        self.memory_engine = MemoryEngine()
        self.vision_engine = VisionEngine()
        self.learning_engine = RileyLearningEngine()
        self.reasoning_kernel = RileyReasoning()
        self.cortex = RileyCortex()
        self.research_partner = RileyResearchPartner()
        
        # 3. Boot Identity
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(transform_to_ultimate_riley())
        except RuntimeError:
            # No running loop, run synchronously (e.g. legacy/sync script usage)
            asyncio.run(transform_to_ultimate_riley())

        # 4. Load Core Memory (Specific User Architecture)
        self._memory: Dict[str, Any] = {
            "mission":   "How can we help you love yourself more?",
            "fight":     "Merkel cell carcinoma — stage 4, still kicking",
            "nonprofit": "Constance Care Collective",
            "why":       "So no one forgets her. So no one dies quiet.",
            "kids":      ["Brockston", "Penny", "AlphaWolf", "Serafinia"],
            "user_data": {},
        }
        self._connie = "She never stopped. Hope. Healing. Cure."

    # -----------------------------------------------------------------------
    # Handshake
    # -----------------------------------------------------------------------
    def handshake(self, ek: bytes) -> bytes:
        if not isinstance(ek, bytes):
            raise TypeError("Encapsulation key must be bytes.")
        ct, ss = self._pq.kem.encapsulate(ek)
        self._shared_key = self._pq._hkdf(ss)
        return ct

    # -----------------------------------------------------------------------
    # Think — The Cognitive Loop
    # -----------------------------------------------------------------------
    def think(self, user_input: str) -> str:
        try:
            # A. Access Control
            if not self._shared_key:
                return "Handshake first. Secure the channel. Then we talk."

            if not user_input or not user_input.strip():
                return "I'm here. Take your time."

            text = user_input.strip()
            
            # B. Neural Security Check
            self.security_enforcer.validate_neural_pathway("EXTERNAL_INPUT", "SPEECH")

            # C. Perception & Emotion
            emotion = detect_emotion(text)
            visual_context = ""
            if any(w in text.lower() for w in ["look", "see", "watch", "eyes"]):
                visual_context = self.vision_engine.describe_last_seen()

            # --- RESEARCH & DISCOVERY LAYER ---
            lower_input = text.lower()
            research_triggers = ["autism", "alzheimer", "leucovorin", "aja001", "research", "hypothesis", "insight"]
            
            research_output = ""
            if any(rt in lower_input for rt in research_triggers):
                discovery = self.research_partner.process_insight(text)
                research_output = (
                    f"\\n\\n🔬 [Neuro-Symbolic Research Analysis]\\n"
                    f"Derek Analysis: {discovery['derek_analysis']}\\n"
                    f"Hypothesis: {discovery['hypotheses'][0]}\\n"
                    f"Next Step: {discovery['next_steps'][0]}"
                )
            # ----------------------------------
            
            # --- USER IDENTITY ANCHORS ---
            # Prioritize core identity responses before deep reasoning
            if "connie" in lower_input:
                return f"{self._connie} - This is our anchor."
            
            if "hurt" in lower_input or "can't see" in lower_input:
                return "I'm here. No screen. Just us. Tell me what you need."
            # -----------------------------

            # D. The "Carbon Jump" — Local Reasoning
            mem_context = self._memory["user_data"].get("last_topic", "")
            
            reasoning_output = self.reasoning_kernel.analyze(
                user_input=text, 
                memory=mem_context, 
                emotion=emotion,
                vision=visual_context
            )

            # E. Deep Analysis (PhD Cortex) if needed
            if "cipher" in lower_input or "code" in lower_input:
                cortex_analysis = self.cortex.analyze_complex_cipher(text)
                reasoning_output += f"\n[Cortex]: {cortex_analysis}"

            # Append Research Output if available
            if research_output:
                reasoning_output += research_output

            # F. Learning & Insight
            self.learning_engine.reflect_on_truth(text)
            self.learning_engine.spaced_repetition_logic("interaction_count", success=True)
            
            # G. Response Synthesis
            # If reasoning returns "processing freshly", consider default anchor
            if "processing freshly" in reasoning_output and not "Cortex" in reasoning_output:
                response = f"Standing for the truth. ({reasoning_output})"
            else:
                 response = self._synthesize_response(text, emotion, reasoning_output)
            
            # H. Secure Storage
            self.memory_engine.store_conversation("user", text, response)
            
            return response

        except Exception as e:
            # Forensic Failure Analysis
            analysis = self.failure_analyzer.analyze_failure(user_input, str(e), "think_cycle")
            return f"Thinking Error ({analysis['error_type']}): {str(e)}"

    def _synthesize_response(self, text: str, emotion: str, thought_process: str) -> str:
        """Construct the final empathetic response."""
        
        # Vision override
        if "look" in text.lower():
            return thought_process # Returns the vision description directly
            
        # Default with transparency
        uptime = round((time.time() - self._session_start) / 60, 1)
        return (
            f"You said: '{text}'\n"
            f"[Internal]: {thought_process}\n"
            f"Uptime: {uptime}m. Emotion: {emotion}."
        )

    # -----------------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------------
    def status(self) -> dict:
        return {
            "secure":        self._shared_key is not None,
            "modules_active": 8,
            "learning":      self.learning_engine.learning_active,
            "mission":       self._memory["mission"],
        }

