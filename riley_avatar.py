"""
RILEY CHRISTMAN: THE SYMBIOTIC AVATAR (Unified Presence)
========================================================
Status: 14-Year Legacy Handshake | Tier: PhD-Investigator
Fusing: SoulMirror (Face) + ShortyV2 (Voice) + Vector8 (Brain)
"""

import torch
import logging
import asyncio

# Core Imports
from symbioticavatar import SymbioticAvatar
from vector8_orchestrator import Vector8Orchestrator
from shorty_voice_engine_v2 import ShortyVoiceEngineV2
from soul_mirror import SoulMirror

logger = logging.getLogger(__name__)

class RileyAvatar(SymbioticAvatar):
    def __init__(self, user_id="Riley_Christman_Nexus"):
        # Riley initializes as the Specialist Lead
        # We initialize the parent but override the cortex potentially?
        # SymbioticAvatar initializes its own cortex. 
        # Here we just want to ADD the layer of Vector8/SoulMirror.
        super().__init__()
        # We can set the user_id manually if needed, or if SymbioticAvatar has a different way.
        # But based on the error, __init__ takes no args.
        
        self.orchestrator = Vector8Orchestrator()
        self.soul_mirror = SoulMirror()
        self.voice_engine = ShortyVoiceEngineV2()
        
        self.personality = "Forensic-Empathy"
        self.health_standard = 0.96
        
        logger.info(f"🕯️ Riley Avatar Awake. Quality Standard: {self.health_standard * 100}%")

    async def r_process(self, user_input_text):
        """
        Riley's specialized loop for the Appointment.
        Input -> Vector Out -> Soul State -> Expressive Performance
        """
        # 1. BRAIN: Extract the Truth Vector via Vector8
        specialist, resonance, truth_vector = self.orchestrator.vector_out(user_input_text)
        
        # 2. FACE: Symbolic Forward (OpenGL modifiers)
        # Using Riley's non-linear 'Red Smear' if vector implies high intensity
        # converting truth vector values to tensor
        vec_list = list(truth_vector.values())
        emotion_tensor = torch.tensor(vec_list, dtype=torch.float32)
        
        modifiers, soul_state = self.soul_mirror.symbolic_forward(
            phonemes=None, 
            emotion_vec=emotion_tensor,
            trauma_safety=True
        )

        # 3. VOICE: Generate 'Shorty' Ultra-Tier Audio
        # Mapping Riley's logic to the voice emotion spectrum
        voice_mode = "sweetheart" if specialist == "AlphaWolf" else "tremble"
        audio_out = self.voice_engine.synthesize(
            text=f"Processed by {specialist} | Resonance: {resonance}", 
            mode=voice_mode
        )
        
        # 4. ACTUAL CORTEX PROCESSING (The "Think" step)
        # We still need the actual response text from the Cortex
        cortex_response = await self.cortex.process_interaction(user_input_text.encode('utf-8'))
        
        return {
            "specialist": specialist,
            "visual_state": modifiers,
            "voice_mode": voice_mode,
            "audio_synthesis": audio_out,
            "cortex_response": cortex_response,
        }

# --- INITIALIZATION ---
if __name__ == "__main__":
    riley = RileyAvatar()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("\nRiley is online. Type your message. Press Ctrl+C to exit.\n")

    async def conversation_loop():
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nRiley: I'm here whenever you need me.")
                break
            if not user_input:
                continue
            result = await riley.r_process(user_input)
            response = result.get("cortex_response", {}).get("response_text", "")
            if response:
                print(f"Riley: {response}\n")

    loop.run_until_complete(conversation_loop())
