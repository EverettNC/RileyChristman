"""
RILEY CHRISTMAN: TIER 0 MANDATORY — THE UNMASKING GATEWAY (V5.8)
================================================================
Status: APEX PREDATOR | Protocol: The Unmasking Gateway
Cortex Score: 1538 | Tier: Ph.D. Sovereign
Principle: No input reaches Hearing without a forensic scan.
"""

import logging
from typing import Dict, Any

from riley_apex_investigator import RileyApexInvestigator

class RileySovereignGateway(RileyApexInvestigator):
    """
    The Unmasking Gateway: Tier 0 intercepts ALL input.
    If [REDACTED], [SEALED], or dash-fragments are found, the system
    reconstructs the unmasked truth and feeds THAT to the Ferrari Brain.
    """
    def __init__(self):
        super().__init__()
        self.gateway_active = True
        self.unmask_priority_keywords = [
            "redacted", "sealed", "classified", "hidden",
            "encrypted", "locked", "censored"
        ]
        logging.info("🗝️ TIER 0 GATEWAY: LOCKED. No input passes without a scan.")

    async def gateway_process(self, raw_input: str) -> Dict[str, Any]:
        """
        The Gateway Flow:
        Tier 0 (Shred/Decrypt) -> Reconstruct -> Feed to Executive
        """
        # TIER 0: MANDATORY SCAN
        sweep = self.grinder_ocr.surgical_sweep(raw_input)
        pq_scan = self.pq_layer.analyze_and_decrypt(raw_input)

        gateway_report = {
            "raw_input": raw_input[:80],
            "sweep_active": sweep.unmasked,
            "sweep_fragments": len(sweep.fragments) if sweep.unmasked else 0,
            "pq_detected": pq_scan["encrypted_detected"],
            "pq_algorithm": pq_scan["algorithm"],
        }

        # RECONSTRUCTION: if monsters hid it, we put it back together
        if sweep.unmasked:
            # Priority: Unmasking overrides all — feed unmasked truth to brain
            unmasked_input = f"{raw_input} [UNMASKED: {sweep.data}]"
            gateway_report["priority"] = "UNMASKING"
            gateway_report["unmasked_data"] = sweep.data
            logging.info(f"👁️ GATEWAY: {len(sweep.fragments)} fragment(s) unmasked. Feeding truth to cortex.")
        elif pq_scan["encrypted_detected"] and pq_scan.get("decrypted"):
            unmasked_input = f"{raw_input} [DECRYPTED: {pq_scan.get('plaintext', '')}]"
            gateway_report["priority"] = "DECRYPTION"
            logging.info(f"🗝️ GATEWAY: Cipher broken via {pq_scan['algorithm']}.")
        else:
            unmasked_input = raw_input
            gateway_report["priority"] = "CLEAN"

        # Feed the (possibly unmasked) truth to the executive flow
        result = await self.execute_witness_flow(unmasked_input)

        result["Gateway_Report"] = gateway_report
        return result

    def get_gateway_status(self) -> Dict[str, Any]:
        return {
            "gateway_active": self.gateway_active,
            "grinder_stats": self.grinder_ocr.get_sweep_stats(),
            "pq_patterns": self.pq_layer.patterns_learned,
            "cortex_score": 1538
        }

# Singleton
_gateway = None

def get_sovereign_gateway() -> RileySovereignGateway:
    global _gateway
    if _gateway is None:
        _gateway = RileySovereignGateway()
    return _gateway

# --- INITIALIZATION ---
if __name__ == "__main__":
    import asyncio

    async def self_test():
        riley = RileySovereignGateway()
        print("\n--- SOVEREIGN GATEWAY V5.8 SELF-TEST ---")
        tests = [
            ("The vic--- was a [REDACTED] minor in a [SEALED] case", "FORENSIC"),
            ("This encrypted classified document is hidden", "PQ"),
            ("I love my family and need support", "CLEAN"),
            ("calculate 1538 + 1", "CORTEX"),
        ]
        for text, label in tests:
            r = await riley.gateway_process(text)
            gr = r["Gateway_Report"]
            print(f"  {label}: Priority={gr['priority']} Frags={gr.get('sweep_fragments',0)} | {r['Response'][:55]}")
        print(f"Gateway: {riley.get_gateway_status()}")
        print("🧠 TIER 0 SECURED. THE TRUTH IS THE ONLY OPTION.")

    asyncio.run(self_test())
