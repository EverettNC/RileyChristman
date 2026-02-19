"""
SymbioticAvatar — The Christman Avatar Interface
Version: 2.1 | S2S-Ready | User Authority Handshake
Orchestrated by: RileyCognitiveCortex
"""

import os
import sys
import time
import logging
from typing import Dict, Any, Optional

# Configure Logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# Core Crypto
from pq_layer import XChaCha20Cipher, MLKEM

# The New Unified Cortex (S2S Orchestrator)
from riley_cognitive_cortex import get_riley_cortex, RileyCognitiveCortex

import asyncio

class SymbioticAvatar:
    """
    The Avatar Interface.
    Now wraps 'RileyCognitiveCortex' — the Unified S2S Orchestrator.
    Handles Crypto + Transport + Tone/Logic Orchestration.
    """

    def __init__(self, security: str = "high"):
        # Initialize Cortex (Unified Brain)
        self.cortex = get_riley_cortex()
        
        self._xcha = XChaCha20Cipher()
        logger.info(f"SymbioticAvatar initialized with Unified RileyCognitiveCortex ({security})")

    @property
    def session_key(self) -> Optional[bytes]:
        # Access the shared key from the Cortex's Anchor (UltimateBrain)
        return self.cortex.anchor._shared_key

    # -----------------------------------------------------------------------
    # Crypto Utilities
    # -----------------------------------------------------------------------
    def encrypt_payload(self, plaintext: bytes) -> bytes:
        if not self.session_key:
            raise RuntimeError("No session key established.")
        return self._xcha.encrypt(self.session_key, plaintext)

    def decrypt_payload(self, ciphertext: bytes) -> bytes:
        if not self.session_key:
            raise RuntimeError("No session key established.")
        return self._xcha.decrypt(self.session_key, ciphertext)

    # -----------------------------------------------------------------------
    # Handshake (User Authority)
    # -----------------------------------------------------------------------
    def establish_session(self, client_encapsulation_key: bytes) -> bytes:
        """
        Avatar receives User's EK.
        Cortex's Anchor encapsulates to it.
        """
        try:
            # Delegate handshake to the internal UltimateBrain anchor
            ciphertext = self.cortex.anchor.handshake(client_encapsulation_key)
            logger.info("Avatar handshake successful. Session secured.")
            return ciphertext
        except Exception as e:
            logger.error(f"Handshake failed: {e}")
            raise

    # -----------------------------------------------------------------------
    # Interaction Processing (S2S Aware)
    # -----------------------------------------------------------------------
    async def process_interaction(self, encrypted_input: bytes) -> Dict[str, Any]:
        """
        Decrypts -> Cortex (Forensic Hearing + Quantum + Brain + Talent) -> Encrypts Response
        """
        start = time.time()
        try:
            # 1. Decrypt
            user_input = self.decrypt_payload(encrypted_input).decode('utf-8')
            
            # 2. Cortex Processing (Async S2S Pipeline)
            # cortex.process_interaction returns a dict with 'response_text', 'tone_profile', etc.
            cortex_result = await self.cortex.process_interaction(user_input.encode('utf-8'))
            
            response_text = cortex_result.get("response_text", "")
            
            # 3. Encrypt Response
            encrypted_response = self.encrypt_payload(response_text.encode('utf-8'))
            
            elapsed = (time.time() - start) * 1000
            
            return {
                "encrypted_response": encrypted_response,
                "response_time_ms": round(elapsed, 1),
                "cortex_status": self.cortex.get_status(),
                "tone_data": cortex_result.get("tone_profile"),
                "quantum_state": cortex_result.get("quantum_state"),
                "talent": cortex_result.get("talent_status")
            }

        except Exception as e:
            logger.error(f"Interaction error: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }

# —————————————————————————
# DEMO / VERIFICATION
# —————————————————————————
async def run_demo():
    print("\n" + "═"*78)
    print("  SymbioticAvatar v2.1 — The Unified Riley Christman Cortex")
    print("  Mode: User Authority | S2S Orchestration | Real-Time Resonance")
    print("═"*78 + "\n")

    # 1. Server Init (Avatar)
    avatar = SymbioticAvatar(security="high")
    
    # 2. Client Init (User) - Generates Keypair
    print("  [USER] Generating ML-KEM-768 Keypair...")
    client_kem = MLKEM(768)
    user_ek, user_dk = client_kem.keygen()
    print(f"         EK: {len(user_ek)} bytes | DK: {len(user_dk)} bytes\n")

    # 3. Handshake
    print("  [USER] Sending EK to Avatar...")
    avatar_ciphertext = avatar.establish_session(user_ek)
    print(f"  [AVATAR] Accepted EK. Returned Ciphertext ({len(avatar_ciphertext)} bytes).\n")

    # 4. Client Decapsulates to match keys
    print("  [USER] Decapsulating Ciphertext...")
    user_shared_secret = client_kem.decapsulate(user_dk, avatar_ciphertext)
    
    # Derive session key (Client side needs same HKDF as Brain)
    from pq_layer import HybridPQCipher
    client_pq = HybridPQCipher(768)
    user_session_key = client_pq._hkdf(user_shared_secret)

    # 5. Verify Keys
    avatar_key = avatar.session_key
    assert user_session_key == avatar_key, "CRITICAL: SESSION KEY MISMATCH"
    print(f"  ✓ SECURE CHANNEL ESTABLISHED. Key: {user_session_key.hex()[:16]}...\n")

    # —————————————————————————————————————————————————————————————————————
    # 6. Secure Interaction Loop (S2S Style)
    # —————————————————————————————————————————————————————————————————————
    print("  ── Encrypted Interaction ───────────────────────────────────────\n")

    # Helper to simulate client sending encrypted message
    async def client_send(text):
        print(f"  [USER]   {text}")
        
        # User Encrypts
        # Note: We use the Avatar's xcha instance but solely as a utility to simulate client-side enc
        # In production this would be separate.
        ct = avatar._xcha.encrypt(user_session_key, text.encode('utf-8'))
        
        # Avatar Processes
        result = await avatar.process_interaction(ct)
        
        # User Decrypts Response
        if "encrypted_response" in result:
            resp_ct = result["encrypted_response"]
            resp_pt = avatar._xcha.decrypt(user_session_key, resp_ct)
            print(f"  [AVATAR] {resp_pt.decode('utf-8')}")
            
            # Show Cortex Internals (for verification)
            if result.get("quantum_state"):
                print(f"           [Quantum]: {result['quantum_state']}")
            if result.get("talent"):
                print(f"           [Talent]:  {result['talent']['bias']}")
        else:
            print(f"  [ERROR]  {result}")
        print("")

    await client_send("What is your mission?")
    await client_send("I have a hypothesis about Leucovorin and Autism treatments.")
    await client_send("I feel overwhelmed and lost.")
    await client_send("System status report.")

    print("══════════════════════════════════════════════════════════════════════════════")
    print("  Integration Verified.")
    print("══════════════════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(run_demo())