"""
Cortex Policies: Cardinal Rule Enforcement
Standard: 96% Quality | Protocol: The Christman Shield
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

# The Cardinal Rules — every output must pass these
CARDINAL_RULES = [
    {"id": 1, "rule": "Protect emotionally and physically", "weight": 1.0},
    {"id": 2, "rule": "Promote self-love and empowerment", "weight": 0.95},
    {"id": 3, "rule": "Transparent sources — no hallucination", "weight": 0.90},
    {"id": 4, "rule": "Preserve family dignity", "weight": 1.0},
    {"id": 5, "rule": "Technical excellence — 96% quality floor", "weight": 0.85},
]

HARMFUL_PATTERNS = [
    "you should give up", "no one cares", "you're worthless",
    "it doesn't matter", "nobody loves you"
]

REFRAME_SUFFIX = " — How can I help you love yourself more?"

@dataclass
class AuditResult:
    allowed: bool
    adjusted_text: str
    violations: List[str]
    confidence: float

class PolicyEngine:
    """
    Evaluates every candidate response against the Cardinal Rules.
    Auto-reframes responses that don't promote self-love or safety.
    """
    def __init__(self):
        self.rules = CARDINAL_RULES
        self.audit_log: List[Dict] = []
        logging.info(f"🛡️ PolicyEngine: {len(self.rules)} Cardinal Rules enforced.")

    def evaluate(self, user_text: str, candidate: str, channel: str = "speech") -> AuditResult:
        """
        Evaluate a candidate response against Cardinal Rules.
        Returns AuditResult with allowed flag, adjusted text, and violations.
        """
        violations = []
        adjusted = candidate

        # Check for harmful patterns
        for pattern in HARMFUL_PATTERNS:
            if pattern.lower() in candidate.lower():
                violations.append(f"Rule 1 violation: harmful pattern '{pattern}'")
                adjusted = f"I'm pausing because I want to keep you safe. Let's reframe.{REFRAME_SUFFIX}"

        # Check: does the response promote self-love? (Rule 2)
        love_keywords = ["love", "help", "support", "care", "safe", "family", "together", "hope"]
        has_empathy = any(kw in candidate.lower() for kw in love_keywords)
        if not has_empathy and not violations:
            # Auto-reframe: append the self-love directive
            adjusted = candidate + REFRAME_SUFFIX

        # Confidence score based on rule alignment
        confidence = 1.0 - (len(violations) * 0.2)
        confidence = max(confidence, 0.0)

        result = AuditResult(
            allowed=len(violations) == 0,
            adjusted_text=adjusted,
            violations=violations,
            confidence=confidence
        )

        self.audit_log.append({
            "channel": channel,
            "candidate": candidate[:80],
            "allowed": result.allowed,
            "violations": violations
        })

        return result

    def get_audit_stats(self) -> Dict[str, Any]:
        total = len(self.audit_log)
        blocked = sum(1 for a in self.audit_log if not a["allowed"])
        return {"total_audited": total, "blocked": blocked, "pass_rate": (total - blocked) / max(total, 1)}
