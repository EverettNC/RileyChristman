"""
SymbioticAvatar — Post-Quantum Secure Session Layer
The Christman AI Project | Powered by Luma Cognify AI

Fixed from original submission:
BUG 1: `from cryptography.hazmat.primitives.asymmetric import kyber`
→ Kyber/ML-KEM is NOT in the cryptography library yet.
Using our own FIPS 203 implementation from pq_layer.py

BUG 2: `nonce = encrypted[:12 12:]`
→ Python syntax error. Should be:
nonce      = encrypted[:12]
ciphertext = encrypted[12:]
→ Also moot now: we use XChaCha20’s 24-byte nonce and
the bundle format is self-describing.

BUG 3: `kyber.Kyber512.generate_private_key()` / `.encapsulate()`
→ Wrong API. ML-KEM is a KEM, not a traditional asymmetric cipher.
Correct flow: keygen() → (ek, dk), encapsulate(ek) → (ct, ss),
decapsulate(dk, ct) → ss

BUG 4: HKDF was being applied to the raw shared secret without the
correct import or usage. Now correctly integrated.
"""

import os
import time
import logging
from typing import Tuple
from pq_layer import HybridPQCipher, MLKEM, XChaCha20Cipher
from brain import BioDigitalBrain
from learning import RecursiveLearningEngine
Tuple_hint = Tuple

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
format='[%(levelname)s] %(name)s: %(message)s')

class SymbioticAvatar:
    """
    Post-quantum secured AI avatar session.

    ```
    Session establishment:
      1. Server instantiates SymbioticAvatar → generates ML-KEM keypair
      2. Server sends self.encapsulation_key to client
      3. Client calls start_session_handshake(server_ek) → gets ciphertext
      4. Server calls complete_handshake(client_ct) → both have shared_secret
      5. All subsequent payloads are XChaCha20-Poly1305 encrypted

    Security level options:
      "standard"  → ML-KEM-512  (fastest, NIST Level 1 PQ security)
      "high"      → ML-KEM-768  (recommended, Level 3)
      "paranoid"  → ML-KEM-1024 (maximum, Level 5)
    """

    LEVEL_MAP = {
        "standard" : 512,
        "high"     : 768,
        "paranoid" : 1024,
    }

    def __init__(self, security: str = "high"):
        level = self.LEVEL_MAP.get(security, 768)
        self._pq          = HybridPQCipher(level)
        self._kem         = MLKEM(level)
        self._xcha        = XChaCha20Cipher()
        self._shared_key  = None   # 32-byte XChaCha20 key, set after handshake

        # Initialize Cognitive & Learning Subsystems
        self.brain = BioDigitalBrain(identity="Riley Christman")
        self.learning = RecursiveLearningEngine()

        # Generate this server's ML-KEM keypair
        self.encapsulation_key, self._decapsulation_key = self._kem.keygen()
        logger.info(
            f"ML-KEM-{level} keypair generated | "
            f"ek={len(self.encapsulation_key)}B  "
            f"dk={len(self._decapsulation_key)}B"
        )

    # ─────────────────────────────────────────────────────────────────────────
    # HANDSHAKE — SERVER SIDE
    # ─────────────────────────────────────────────────────────────────────────

    def complete_handshake(self, client_ciphertext: bytes) -> None:
        """
        Server receives the KEM ciphertext from client.
        Decapsulates it to recover the shared secret, then derives
        the XChaCha20 session key via HKDF.

        client_ciphertext: the bytes returned by client_side_handshake()
        """
        try:
            ss = self._kem.decapsulate(self._decapsulation_key, client_ciphertext)
            self._shared_key = self._pq._hkdf(ss)
            logger.info(
                f"Handshake complete | "
                f"session key={self._shared_key.hex()[:12]}...  (32B)"
            )
        except Exception as e:
            logger.error(f"Handshake failed: {e}")
            raise

    # ─────────────────────────────────────────────────────────────────────────
    # HANDSHAKE — CLIENT SIDE (static helper)
    # ─────────────────────────────────────────────────────────────────────────

    @staticmethod
    def client_side_handshake(server_encapsulation_key: bytes,
                               security: str = "high") -> Tuple_hint:
        """
        Client initiates handshake using the server's encapsulation key.

        Returns:
          (kem_ciphertext, session_key)
          - Send kem_ciphertext to server via complete_handshake()
          - Use session_key locally for encrypt_payload / decrypt_payload
        """
        level = SymbioticAvatar.LEVEL_MAP.get(security, 768)
        pq    = HybridPQCipher(level)
        kem   = MLKEM(level)
        ct, ss = kem.encapsulate(server_encapsulation_key)
        session_key = pq._hkdf(ss)
        return ct, session_key

    # ─────────────────────────────────────────────────────────────────────────
    # ENCRYPTION / DECRYPTION
    # ─────────────────────────────────────────────────────────────────────────

    def encrypt_payload(self, data: bytes,
                        associated_data: bytes = b"christman-avatar") -> bytes:
        """
        Encrypt a payload with the established session key.
        Uses XChaCha20-Poly1305 with a fresh 192-bit random nonce each call.

        Returns: nonce (24B) || ciphertext || auth_tag (16B)
        """
        if self._shared_key is None:
            raise RuntimeError("No session key — complete handshake first.")
        return self._xcha.encrypt(self._shared_key, data,
                                  aad=associated_data)

    def decrypt_payload(self, encrypted: bytes,
                        associated_data: bytes = b"christman-avatar") -> bytes:
        """
        Decrypt an incoming payload.
        Raises RuntimeError if the authentication tag is invalid
        (tampered data, wrong key, or replay with modified bytes).
        """
        if self._shared_key is None:
            raise RuntimeError("No session key — complete handshake first.")
        return self._xcha.decrypt(self._shared_key, encrypted,
                                  aad=associated_data)

    # ─────────────────────────────────────────────────────────────────────────
    # INTERACTION HANDLER
    # ─────────────────────────────────────────────────────────────────────────

    def process_interaction(self,
                            user_input: str = "",
                            audio_path: str | None = None,
                            encrypted_input: bytes | None = None) -> dict:
        """
        Process a user interaction, optionally decrypting the input
        and always encrypting the response.
        """
        start = time.time()
        try:
            # Decrypt input if it arrived encrypted
            if encrypted_input is not None:
                user_input = self.decrypt_payload(encrypted_input).decode('utf-8')
                logger.debug(f"Decrypted input ({len(encrypted_input)}B → '{user_input[:40]}...')")

            # ── Integrated Cognitive & Learning Flow ──────────────────────
            
            # 1. Compute response via BioDigitalBrain
            brain_response = self.brain.compute_response(user_input)
            
            # 2. Extract textual response (internal monologue for now, or synthesized)
            # In a real system, this would be the generated dialogue.
            # For this demo, we expose the internal thought process.
            response_text = (
                f"[{brain_response['emotional_state']}] "
                f"{brain_response['internal_monologue']}"
            )

            # 3. Learning Step - Observe interaction
            # We assume a default positive feedback for this loop, 
            # or we could analyze the user's *previous* reaction here.
            self.learning.observe(
                user_input=user_input, 
                brain_meta=brain_response, 
                feedback_score=1.0
            )

            # ─────────────────────────────────────────────────────────────

            encrypted_response = self.encrypt_payload(response_text.encode('utf-8'))
            elapsed = time.time() - start

            return {
                "encrypted_response" : encrypted_response,
                "response_time_ms"   : round(elapsed * 1000, 1),
                "session_active"     : True,
            }

        except RuntimeError as e:
            logger.error(f"Decryption/encryption error: {e}")
            raise
        except Exception as e:
            logger.critical(f"Unexpected crash: {e}")
            fallback = "I'm still here. Something broke, but I'm not leaving."
            encrypted_fallback = self.encrypt_payload(fallback.encode('utf-8'))
            return {
                "encrypted_response" : encrypted_fallback,
                "session_active"     : True,
                "error"              : str(e),
            }

# ─────────────────────────────────────────────────────────────────────────────

# DEMO — full handshake + encrypted session

# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "═"*78)
    print("  SymbioticAvatar — Post-Quantum Secure Session Demo")
    print("  The Christman AI Project | ML-KEM-768 + XChaCha20-Poly1305")
    print("═"*78 + "\n")

    # Server init
    server = SymbioticAvatar(security="high")
    print(f"  [SERVER] ML-KEM-768 keypair ready.")
    print(f"           ek={len(server.encapsulation_key)}B  — share with clients\n")

    # Client handshake
    kem_ct, client_session_key = SymbioticAvatar.client_side_handshake(
        server.encapsulation_key, security="high"
    )
    print(f"  [CLIENT] KEM ciphertext generated ({len(kem_ct)}B) — sending to server...")

    # Server completes handshake
    server.complete_handshake(kem_ct)
    print(f"  [SERVER] Handshake complete. Session key established.\n")

    # Verify both sides derived the same key
    assert server._shared_key == client_session_key, "KEY MISMATCH!"
    print(f"  ✓ Both sides have identical session key: {server._shared_key.hex()[:24]}...\n")

    # Encrypted message exchange
    from pq_layer import XChaCha20Cipher as _XC
    xcha = _XC()

    messages = [
        "I love you.",              # Dusty's first words
        "AlphaVox session data",
        "Derek status: operational",
    ]

    print("  ── Encrypted Message Exchange ──────────────────────────────────")
    for msg in messages:
        # Client encrypts
        enc = xcha.encrypt(client_session_key, msg.encode(),
                           aad=b"christman-avatar")
        # Server decrypts
        dec = server.decrypt_payload(enc)
        print(f"  [CLIENT→SERVER] '{msg}'")
        print(f"  [ENCRYPTED]     {enc.hex()[:40]}...")
        print(f"  [DECRYPTED]     '{dec.decode()}'\n")

    # Full process_interaction round-trip
    print("  ── process_interaction() Round-Trip ───────────────────────────")
    enc_input = xcha.encrypt(client_session_key,
                              b"How is Riley today?",
                              aad=b"christman-avatar")
    result = server.process_interaction(encrypted_input=enc_input)
    final  = xcha.decrypt(client_session_key,
                           result["encrypted_response"],
                           aad=b"christman-avatar")
    print(f"  Response: {final.decode()}")
    print(f"  Time:     {result['response_time_ms']}ms\n")

    print("═"*78)
    print("  ✓ Full PQ-secured session complete")
    print("  The Christman AI Project — Protecting the vulnerable since 2012.")
    print("═"*78)