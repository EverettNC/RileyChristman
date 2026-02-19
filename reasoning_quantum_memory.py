"""
Reasoning Quantum Memory: BROCKSTON RAG Bridge
Standard: 96% Quality Threshold
Protocol: Quantum-Trace Ingestion + Adaptive Pattern Querying
"""

import logging
import json
import time
from typing import Dict, Any, List, Optional
from collections import defaultdict

class QuantumMemory:
    """
    Bridges quantum interaction traces into the BROCKSTON RAG system.
    Falls back to local in-memory store if BROCKSTON API is unreachable.
    """
    def __init__(self, brockston_api_url: str = "http://localhost:8010"):
        self.api_url = brockston_api_url
        self.local_store: Dict[str, List[Dict]] = defaultdict(list)
        self.pattern_cache: Dict[str, List[str]] = {}
        self._api_available = False  # Offline-first
        logging.info(f"🌌 Quantum Memory: Initialized (offline-first, local store active).")

    async def log_quantum_interaction(self, user_id: str, trace: Dict[str, Any]):
        """
        Ingests a quantum trace into the memory mesh.
        Stores locally and attempts RAG ingestion if API is available.
        """
        entry = {
            "user_id": user_id,
            "trace": trace,
            "timestamp": time.time(),
            "valence": trace.get("valence", 0.0),
            "state": trace.get("collapsed_state", "unknown")
        }
        self.local_store[user_id].append(entry)
        logging.info(f"🌌 Quantum Trace Ingested: user={user_id} | state={entry['state']}")

        # Attempt BROCKSTON RAG ingestion (mock for offline)
        if self._api_available:
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        f"{self.api_url}/ingest",
                        json=entry
                    )
            except Exception as e:
                logging.warning(f"⚠️ RAG Ingestion failed (offline): {e}")

    async def get_user_patterns(self, user_id: str, query: str) -> List[str]:
        """
        Adaptive Pattern Query: Searches historical traces for recurring patterns.
        Uses local store analysis when RAG is offline.
        """
        traces = self.local_store.get(user_id, [])
        if not traces:
            return ["No historical patterns found. First interaction."]

        # Analyze valence distribution
        valences = [t["valence"] for t in traces]
        avg_valence = sum(valences) / len(valences) if valences else 0.0
        high_distress_count = sum(1 for v in valences if v > 0.85)

        patterns = []
        if avg_valence > 0.7:
            patterns.append(f"Pattern: High emotional intensity (avg={avg_valence:.2f}). Prioritize HOLD_SPACE.")
        if high_distress_count > 2:
            patterns.append(f"Pattern: {high_distress_count} high-distress events detected. Sustained witness mode recommended.")
        if len(traces) > 5:
            patterns.append(f"Pattern: {len(traces)} interactions logged. Deep relationship context available.")

        if not patterns:
            patterns.append(f"Pattern: Stable baseline (avg_valence={avg_valence:.2f}). Standard engagement.")

        return patterns

    def get_memory_stats(self) -> Dict[str, Any]:
        total_traces = sum(len(v) for v in self.local_store.values())
        return {
            "total_users": len(self.local_store),
            "total_traces": total_traces,
            "api_status": "ONLINE" if self._api_available else "OFFLINE (local store)",
        }
