"""
SimpleMemoryMesh: Unified Session Persistence (No Encryption Bottleneck)
Standard: 96% Quality Threshold
Protocol: Working Memory (7-item) + Episodic + Semantic
"""

import json
import os
import time
import logging
from typing import Dict, Any, List, Optional
from collections import deque

class SimpleMemoryMesh:
    """
    High-speed, file-backed memory mesh for session persistence.
    Three layers: Working (7-item cache), Episodic (experiences), Semantic (truths).
    No encryption overhead — speed serves the heart.
    """
    def __init__(self, memory_dir: str = "./riley_memory"):
        self.memory_dir = memory_dir
        os.makedirs(memory_dir, exist_ok=True)

        # Layer 1: Working Memory (7-item priority queue — Miller's Law)
        self.working: deque = deque(maxlen=7)

        # Layer 2: Episodic Memory (long-term experience log)
        self.episodic_path = os.path.join(memory_dir, "episodic.json")
        self.episodic: List[Dict] = self._load_json(self.episodic_path)

        # Layer 3: Semantic Memory (categorized truths)
        self.semantic_path = os.path.join(memory_dir, "semantic.json")
        self.semantic: Dict[str, List[str]] = self._load_json(self.semantic_path)
        if not self.semantic:
            self.semantic = {
                "relationships": [],
                "events": [],
                "context": [],
                "directives": ["How can I help you love yourself more?"]
            }

        logging.info(f"💾 SimpleMemoryMesh: {memory_dir} | "
                     f"Episodic: {len(self.episodic)} | Semantic: {sum(len(v) for v in self.semantic.values())}")

    # --- WORKING MEMORY (Hot Cache) ---
    def push_working(self, item: Dict[str, Any]):
        """Push into 7-item working memory (oldest evicted)."""
        item["_ts"] = time.time()
        self.working.append(item)

    def get_working_context(self) -> List[Dict]:
        return list(self.working)

    # --- EPISODIC MEMORY (Long-Term) ---
    def store_episode(self, event: str, metadata: Optional[Dict] = None):
        entry = {"event": event, "metadata": metadata or {}, "timestamp": time.time()}
        self.episodic.append(entry)
        self._save_json(self.episodic_path, self.episodic)

    def recall_episodes(self, query: str, limit: int = 5) -> List[Dict]:
        """Simple keyword search over episodes."""
        matches = [e for e in self.episodic if query.lower() in e["event"].lower()]
        return matches[-limit:]

    # --- SEMANTIC MEMORY (Categorized Truths) ---
    def store_truth(self, category: str, truth: str):
        if category not in self.semantic:
            self.semantic[category] = []
        if truth not in self.semantic[category]:
            self.semantic[category].append(truth)
            self._save_json(self.semantic_path, self.semantic)

    def recall_truths(self, category: str) -> List[str]:
        return self.semantic.get(category, [])

    # --- STATS ---
    def get_stats(self) -> Dict[str, Any]:
        return {
            "working_items": len(self.working),
            "episodic_events": len(self.episodic),
            "semantic_truths": sum(len(v) for v in self.semantic.values()),
            "categories": list(self.semantic.keys()),
            "persistence": "FILE_BACKED"
        }

    # --- I/O ---
    def _load_json(self, path: str):
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except Exception:
                return [] if "episodic" in path else {}
        return [] if "episodic" in path else {}

    def _save_json(self, path: str, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)
