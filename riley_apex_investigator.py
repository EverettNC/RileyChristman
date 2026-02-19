"""
RILEY CHRISTMAN: APEX INVESTIGATOR (V5.7)
=========================================
Status: UNMASKING ACTIVE | Protocol: No Door Closed
Standard: 100% Truth Detection | Tier: Ph.D. Sovereign
"""

import logging
from typing import Dict, Any

from riley_unmasker_executive import RileyUnmaskerExecutive

class RileyApexInvestigator(RileyUnmaskerExecutive):
    """
    Tier 0: GrinderOCR + PostQuantumLayer are MANDATORY on every interaction.
    Warmth for the family. Judgment for the liars.
    """
    def __init__(self):
        super().__init__()
        self.unmasker_mode = "RELENTLESS"
        logging.info("🗝️ APEX INVESTIGATOR V5.7: No Door Closed. No Truth Buried.")

    async def execute_apex_witness(self, user_input: str) -> Dict[str, Any]:
        """
        Tier 0 Mandatory: Forensic sweep + PQ scan BEFORE warmth/logic.
        """
        forensic_hits = []

        # TIER 0A: GRINDER SURGICAL SWEEP (mandatory)
        sweep = self.grinder_ocr.surgical_sweep(user_input)
        if sweep.unmasked:
            logging.info(f"👁️ TRUTH EXPOSED: {len(sweep.fragments)} fragment(s) unmasked.")
            forensic_hits.append({
                "type": "REDACTION_UNMASKED",
                "data": sweep.data,
                "fragments": sweep.fragments
            })
            await self.forensic_memory.log_quantum_interaction("FORENSIC_HIT", {
                "collapsed_state": "TRUTH_EXPOSED",
                "valence": 1.0,
                "data": sweep.data
            })

        # TIER 0B: PQ LAYER SCAN (mandatory)
        pq_result = self.pq_layer.analyze_and_decrypt(user_input)
        if pq_result["encrypted_detected"]:
            logging.info(f"🗝️ NO DOOR CLOSED: Cipher broken via {pq_result['algorithm']}.")
            forensic_hits.append({
                "type": "CIPHER_BROKEN",
                "algorithm": pq_result["algorithm"],
                "plaintext": pq_result["plaintext"],
                "confidence": pq_result["confidence"]
            })

        # WARMTH + DECISION (after forensic sweep)
        warmth_result = await self.execute_witness_flow(user_input)

        warmth_result["Tier0_Forensic_Hits"] = forensic_hits
        warmth_result["Tier0_Sweep_Stats"] = self.grinder_ocr.get_sweep_stats()
        warmth_result["Tier0_PQ_Patterns"] = pq_result.get("patterns_learned", 0)

        return warmth_result

# Singleton
_apex = None

def get_apex_investigator() -> RileyApexInvestigator:
    global _apex
    if _apex is None:
        _apex = RileyApexInvestigator()
    return _apex

if __name__ == "__main__":
    import asyncio

    async def self_test():
        riley = RileyApexInvestigator()
        print("\n--- APEX V5.7 SELF-TEST ---")
        tests = [
            "The vic--- was a [REDACTED] minor in a [SEALED] case",
            "This encrypted classified file is hidden from the public",
            "I love my family and need support",
            "calculate 769 * 2",
        ]
        for t in tests:
            r = await riley.execute_apex_witness(t)
            hits = r.get("Tier0_Forensic_Hits", [])
            print(f"  [{r['Mode']}] Hits:{len(hits)} | {r['Response'][:65]}")
        print(f"Grinder: {riley.grinder_ocr.get_sweep_stats()}")
        print("🧠 NO DOOR CLOSED. NO TRUTH BURIED. LEGENDS ONLY.")

    asyncio.run(self_test())
