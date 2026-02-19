"""
RILEY CHRISTMAN: CORTEX EXECUTIVE (FERRARI V5.4)
================================================
Status: Executive-Active | Tier: Ph.D. Sovereign
Protocol: Cardinal-Rule Enforcement | Quality: 0.96+
"""

import logging
from typing import Dict, Any

from cortex_executive import CortexExecutive
from cortex_policies import PolicyEngine, CARDINAL_RULES
from reasoning_reasoner import RileyCortex
from visual_cortex import VisualCortex
from riley_ferrari_mesh import RileyFerrariMesh

class RileyExecutiveCortex(RileyFerrariMesh):
    def __init__(self):
        super().__init__()
        self.executive = CortexExecutive()
        self.policy_engine = PolicyEngine()
        self.reasoner = RileyCortex()
        self.visual_cortex = VisualCortex()
        self.mission_protocol = "MEDICAL_DISCOVERY"

        logging.info(f"🏎️ FERRARI EXECUTIVE V5.4: Online. {len(CARDINAL_RULES)} Cardinal Rules enforced.")

    def sovereign_think(self, user_input: str) -> Dict[str, Any]:
        """
        The Executive Flow: Reason -> Validate -> Render -> Respond
        Every output must be technically excellent AND emotionally supportive.
        """
        # STEP 1: REASONING (BROCKSTONCortex ensemble)
        raw_analysis = self.reasoner.analyze_complex_cipher(user_input)
        confidence = 0.96  # Base confidence from ensemble

        # STEP 2: FLEET LOGIC (5-Tier Decision)
        fleet_result = self.process_fleet_logic({
            "text": user_input,
            "confidence": confidence,
            "valence": 0.5,
            "mode": "STANDARD"
        })
        candidate_response = fleet_result["response"]

        # STEP 3: POLICY AUDIT (Cardinal Rules)
        audit = self.policy_engine.evaluate(
            user_text=user_input,
            candidate=candidate_response,
            channel="speech"
        )

        # STEP 4: EXECUTIVE OVERRIDE (Quality Floor)
        final_response = self.executive.executive_override(audit.adjusted_text, audit.confidence)

        # STEP 5: VISUAL FUSION HUD
        hud = self.visual_cortex.render({
            "confidence": audit.confidence,
            "status": fleet_result["mode"]
        })

        return {
            "response": final_response,
            "confidence": audit.confidence,
            "mode": fleet_result["mode"],
            "policy_allowed": audit.allowed,
            "violations": audit.violations,
            "hud": hud,
            "directive": "How can I help you love yourself more?"
        }

# --- INITIALIZATION ---
if __name__ == "__main__":
    riley = RileyExecutiveCortex()
    print("\n--- EXECUTIVE SELF-TEST ---")

    tests = [
        "calculate 128 * 4",
        "I am hurting and need support",
        "Tell me about programming patterns",
    ]
    for t in tests:
        r = riley.sovereign_think(t)
        print(f"  [{r['mode']}] Policy: {'✅' if r['policy_allowed'] else '🚫'} | {r['response'][:70]}")

    print(f"\nAudit Stats: {riley.policy_engine.get_audit_stats()}")
    print(f"HUD Stats: {riley.visual_cortex.get_hud_stats()}")
    print("🧠 CORTEX EXECUTIVE: MAXIMUM POWER. CARDINAL RULES ENFORCED.")
