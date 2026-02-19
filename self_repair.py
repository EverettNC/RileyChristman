"""
Self-Repair: Auto-Healing Immune System
Standard: 96% Quality Threshold
Real error log parsing + importlib reload of broken modules.
"""
import importlib
import logging
import re
import sys
import traceback
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Regex patterns to extract module name from common Python tracebacks
_MODULE_PATTERNS = [
    r'ModuleNotFoundError: No module named [\'"]([^\'"]+)[\'"]',
    r'ImportError:.*[\'"]([a-zA-Z_][a-zA-Z0-9_.]*)[\'"]',
    r'File ".*?([a-zA-Z_][a-zA-Z0-9_]*)\.py"',
    r'AttributeError: module [\'"]([^\'"]+)[\'"]',
]

class AutoRepair:
    def __init__(self):
        self.health_score = 1.0
        self.repair_log: list = []

    def repair_module(self, error_log: str) -> Dict[str, Any]:
        """
        Parses the error log for the failing module name,
        attempts importlib.reload() if it's loaded, or import if missing.
        Updates health_score based on outcome.
        """
        module_name = self._parse_module(error_log)
        action = "unknown"
        status = "failed"
        detail = ""

        if module_name:
            action, status, detail = self._attempt_reload(module_name)
        else:
            # Try to extract from full traceback
            action = "parse_failed"
            detail = f"Could not identify module from log: {error_log[:120]}"
            logger.warning(f"🔧 AutoRepair: {detail}")

        if status == "repaired":
            self.health_score = min(self.health_score + 0.05, 1.0)
        else:
            self.health_score = max(self.health_score - 0.1, 0.0)

        record = {
            "status": status,
            "module": module_name or "unknown",
            "action": action,
            "detail": detail,
            "health_score": self.health_score,
        }
        self.repair_log.append(record)
        logger.info(f"🔧 AutoRepair result: {record}")
        return record

    def _parse_module(self, error_log: str) -> str:
        for pattern in _MODULE_PATTERNS:
            m = re.search(pattern, error_log)
            if m:
                # Return top-level package name only
                return m.group(1).split(".")[0]
        return ""

    def _attempt_reload(self, module_name: str):
        if module_name in sys.modules:
            try:
                importlib.reload(sys.modules[module_name])
                logger.info(f"🔧 Reloaded module: {module_name}")
                return "reload", "repaired", f"Module '{module_name}' successfully reloaded."
            except Exception as e:
                logger.error(f"🔧 Reload failed for '{module_name}': {e}")
                return "reload", "failed", str(e)
        else:
            try:
                importlib.import_module(module_name)
                logger.info(f"🔧 Imported missing module: {module_name}")
                return "import", "repaired", f"Module '{module_name}' successfully imported."
            except ImportError as e:
                logger.error(f"🔧 Cannot import '{module_name}': {e}")
                return "import", "failed", str(e)

    def get_health(self) -> Dict[str, Any]:
        return {
            "health_score": self.health_score,
            "repair_attempts": len(self.repair_log),
            "last_repair": self.repair_log[-1] if self.repair_log else None,
        }
