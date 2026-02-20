"""
RILEY CHRISTMAN: CORTEX EXECUTIVE (FERRARI V5.4)
================================================
Status: Executive-Active | Tier: PhD-Investigator
Standard: 0.96 Quality | Protocol: Cardinal Rule Enforcement
"""

import logging
from typing import Dict, Any

from cortex_executive import CortexExecutive
from cortex_policies import get_policy_engine, CARDINAL_RULES
from reasoning_reasoner import BROCKSTONCortex
from visual_cortex import VisualCortex
from riley_ferrari_mesh import RileyFerrariMesh

class RileyExecutiveCortex(RileyFerrariMesh):
    def __init__(self):
        super().__init__()
        self.executive = CortexExecutive()
        self.policy_engine = get_policy_engine()
        self.reasoner = BROCKSTONCortex()
        self.visual_cortex = VisualCortex()
        self.mission_protocol = "MEDICAL_DISCOVERY"

        logging.info(f"🏎️ FERRARI EXECUTIVE V5.4: Online. {len(CARDINAL_RULES)} Cardinal Rules enforced.")

    def sovereign_think(self, user_input: str) -> Dict[str, Any]:
        """
        The Executive Flow: Reason -> Fleet Logic -> Audit -> Render -> Express
        """
        # STEP 1: REASONING (BROCKSTONCortex ensemble — 3 pipelines vote)
        outcome = self.reasoner.analyze(user_input, debug=True)

        # STEP 2: FLEET LOGIC (5-Tier Decision)
        fleet_result = self.process_fleet_logic({
            "text": user_input,
            "confidence": outcome.confidence,
            "valence": 0.5,
            "mode": "STANDARD"
        })
        candidate_response = fleet_result["response"]

        # STEP 3: POLICY AUDIT (Cardinal Rules + I'm-with-you protocol)
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
            "tools_used": outcome.used_tools,
            "hud": hud,
            "directive": "How can I help you love yourself more?"
        }

    async def execute_sovereign_loop(self, user_input: str, audio_trace=None) -> Dict[str, Any]:
        """Async wrapper for the executive flow."""
        return self.sovereign_think(user_input)

# Singleton accessor
_executive = None

def get_executive_cortex() -> RileyExecutiveCortex:
    global _executive
    if _executive is None:
        _executive = RileyExecutiveCortex()
    return _executive

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

    print(f"\nAudit: {riley.policy_engine.get_audit_stats()}")
    print(f"HUD: {riley.visual_cortex.get_hud_stats()}")
    print("🧠 CORTEX EXECUTIVE: NO MORE WEAK LOGIC.")
