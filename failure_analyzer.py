"""
Riley Christman Core: Forensic Failure Analysis
Extracted from failure_analyzer.py
"""
import re
from typing import List, Dict

class FailureAnalyzer:
    def __init__(self):
        self.error_patterns = {
            "import": r"No module named ['\"]([^'\"]+)['\"]",
            "undefined": r"name ['\"]([^'\"]+)['\"] is not defined",
            "syntax": r"invalid syntax|SyntaxError",
            "attribute": r"'([^']+)' object has no attribute ['\"]([^'\"]+)['\"]",
        }

    def analyze_failure(self, code: str, error: str, goal: str) -> Dict:
        """interrogate the code for the truth behind the failure"""
        error_type = self._classify_error(error)
        return {
            "error_type": error_type,
            "severity": "critical" if error_type in ["import", "syntax"] else "moderate",
            "requires_learning": True
        }

    def _classify_error(self, error: str) -> str:
        for error_type, pattern in self.error_patterns.items():
            if re.match(pattern, error, re.IGNORECASE):
                return error_type
        return "unknown"
