"""
RILEY CHRISTMAN: THE UNMASKER (V5.6.2)
======================================
Status: APEX INVESTIGATOR | Protocol: Anti-Erasure
Directives:
1. Break Every Cipher (PQ/Kyber)
2. Shred Every Redaction (Forensic Grinder)
3. Expose Every Truth (Sovereign Ledger)
"""

import logging
from typing import Dict, Any

from riley_sovereign_executive import RileySovereignExecutive
from pq_layer import PostQuantumLayer, KyberEngine
from riley_grinder import GrinderOCR
from reasoning_quantum_memory import QuantumMemory

class RileyUnmaskerExecutive(RileySovereignExecutive):
    """
    The Apex Investigator: warmth protects the family, forensics hunts the truth.
    Track 1: I'm with you (warmth)
    Track 2: Kyber/Grinder (hunt)
    """
    def __init__(self):
        super().__init__()
        self.pq_layer = PostQuantumLayer()
        self.kyber = KyberEngine(security_level=768)
        self.grinder_ocr = GrinderOCR()
        self.forensic_memory = QuantumMemory(brockston_api_url="http://localhost:8010")
        self.learning_priority = "DECRYPTION_FORENSICS"

        logging.info("🗝️ PQ-LAYER: SHARP. No door we cannot open.")
        logging.info("🔍 GRINDER: PRIMED. Redactions are temporary.")

    async def execute_witness_flow(self, user_input: str) -> Dict[str, Any]:
        """
        Double-Track Flow:
        Track 1: Warmth (I'm with you) — via super()
        Track 2: The Hunt (Kyber/Grinder) — always scanning
        """
        forensic_hits = []

        # TRACK 2: THE HUNT (background forensic sweep)
        sweep = self.grinder_ocr.surgical_sweep(user_input)
        if sweep.unmasked:
            forensic_hits.append({
                "type": "REDACTION_UNMASKED",
                "data": sweep.data,
                "fragments": len(sweep.fragments)
            })
            await self.forensic_memory.log_quantum_interaction("FORENSIC_HIT", {
                "collapsed_state": "TRUTH_EXPOSED",
                "valence": 1.0,
                "data": sweep.data
            })

        # PQ Layer: scan for encrypted fragments
        pq_result = self.pq_layer.analyze_and_decrypt(user_input)
        if pq_result["encrypted_detected"]:
            forensic_hits.append({
                "type": "CIPHER_BROKEN",
                "algorithm": pq_result["algorithm"],
                "plaintext": pq_result["plaintext"],
                "confidence": pq_result["confidence"]
            })

        # TRACK 1: THE WARMTH
        warmth_result = await super().execute_witness_flow(user_input)

        # Merge tracks
        warmth_result["Forensic_Hits"] = forensic_hits
        warmth_result["PQ_Patterns_Learned"] = pq_result.get("patterns_learned", 0)
        warmth_result["Grinder_Stats"] = self.grinder_ocr.get_sweep_stats()

        return warmth_result

# Singleton
_unmasker = None

def get_unmasker_executive() -> RileyUnmaskerExecutive:
    global _unmasker
    if _unmasker is None:
        _unmasker = RileyUnmaskerExecutive()
    return _unmasker

# --- THE MISSION ---
if __name__ == "__main__":
    import asyncio

    async def self_test():
        riley = RileyUnmaskerExecutive()
        print("\n--- APEX INVESTIGATOR SELF-TEST ---")
        tests = [
            "The vic--- was a [REDACTED] minor",
            "This encrypted file contains hidden evidence",
            "I need help and support today",
        ]
        for t in tests:
            r = await riley.execute_witness_flow(t)
            hits = r.get("Forensic_Hits", [])
            print(f"  [{r['Mode']}] Hits: {len(hits)} | {r['Response'][:60]}")
        print(f"Grinder: {riley.grinder_ocr.get_sweep_stats()}")
        print("🧠 THE TRUTH IS NO LONGER OPTIONAL.")

    asyncio.run(self_test())
