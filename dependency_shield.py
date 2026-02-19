"""
Dependency Shield: The Immune System
Standard: 96% Quality Threshold
"""
import importlib
import logging
import sys
from typing import Dict, Any

# All modules Riley depends on
RILEY_FLEET = [
    "torch", "numpy", "pyttsx3", "librosa", "speech_recognition",
    "sentence_transformers", "nltk", "wikipediaapi", "textblob",
    "cryptography", "tensorflow", "sklearn",
]

class DependencyShield:
    def __init__(self):
        self.module_status: Dict[str, str] = {}
        logging.info("🛡️ Dependency Shield: Active. Monitoring Fleet Stability.")

    def scan_and_patch(self) -> Dict[str, Any]:
        """
        Attempts to import every critical module.
        Reports HEALTHY, MISSING, or ERROR for each.
        Re-validates already-loaded modules to catch runtime breakage.
        """
        broken = []
        healthy = []

        for mod_name in RILEY_FLEET:
            try:
                if mod_name in sys.modules:
                    mod = sys.modules[mod_name]
                    _ = mod.__name__  # validate still accessible
                else:
                    importlib.import_module(mod_name)
                self.module_status[mod_name] = "HEALTHY"
                healthy.append(mod_name)
            except ImportError as e:
                self.module_status[mod_name] = f"MISSING: {e}"
                broken.append(mod_name)
                logging.warning(f"🛡️ SHIELD: {mod_name} MISSING — {e}")
            except Exception as e:
                self.module_status[mod_name] = f"ERROR: {e}"
                broken.append(mod_name)
                logging.error(f"🛡️ SHIELD: {mod_name} ERROR — {e}")

        status = "FLEET_STABLE" if not broken else f"DEGRADED: {len(broken)} module(s) offline"
        logging.info(f"🛡️ Shield scan complete. {len(healthy)}/{len(RILEY_FLEET)} healthy.")

        return {
            "status": status,
            "healthy": healthy,
            "broken": broken,
            "module_status": self.module_status,
        }
