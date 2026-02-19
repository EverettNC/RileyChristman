"""
AlphaVox Knowledge Engine: Continuous Knowledge & Discovery
Standard: 96% Quality Threshold
Real crawl via Wikipedia API + fact graph persistence.
"""
import threading
import logging
import json
import os
from typing import Dict, Any, List

try:
    import wikipediaapi
    _WIKI = wikipediaapi.Wikipedia(
        language="en",
        user_agent="RileyChristman/1.0 (christmanai@proton.me)"
    )
    _WIKI_AVAILABLE = True
except Exception:
    _WIKI = None
    _WIKI_AVAILABLE = False

KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "brockston_memory", "knowledge.json")

class KnowledgeGraph:
    def __init__(self):
        self.topic_concepts: Dict[str, List[str]] = {}
        self.edges: List[tuple] = []
        self._load()

    def _load(self):
        if os.path.exists(KNOWLEDGE_FILE):
            try:
                with open(KNOWLEDGE_FILE) as f:
                    data = json.load(f)
                    self.topic_concepts = data.get("topics", {})
                    self.edges = [tuple(e) for e in data.get("edges", [])]
            except Exception:
                pass

    def save(self):
        os.makedirs(os.path.dirname(KNOWLEDGE_FILE), exist_ok=True)
        with open(KNOWLEDGE_FILE, "w") as f:
            json.dump({"topics": self.topic_concepts, "edges": self.edges}, f, indent=2)

    def add_fact(self, subject: str, predicate: str, object_: str):
        self.edges.append((subject, predicate, object_))

    def add_topic(self, topic: str, concepts: List[str]):
        self.topic_concepts[topic] = concepts


class KnowledgeEngine:
    def __init__(self):
        self.graph = KnowledgeGraph()
        self.learning_active = False
        self.facts_learned = len(self.graph.edges)
        self.topics_explored = len(self.graph.topic_concepts)
        self.crawler_status: Dict[str, Any] = {"current_topic": "Idle"}
        self._thread = None
        self._lock = threading.Lock()

    def start_learning(self, topics: List[str] = None):
        if not self.learning_active:
            self.learning_active = True
            default_topics = [
                "Post-quantum cryptography", "Family therapy",
                "Alzheimer's disease", "Autism spectrum disorder",
                "Artificial intelligence ethics", "Trauma informed care",
            ]
            self._topics = topics or default_topics
            self._thread = threading.Thread(target=self._learning_loop, daemon=True)
            self._thread.start()
            logging.info(f"📚 KnowledgeEngine: Started crawling {len(self._topics)} topics.")

    def stop_learning(self):
        self.learning_active = False
        if self._thread:
            self._thread.join(timeout=2.0)

    def _learning_loop(self):
        idx = 0
        while self.learning_active:
            topic = self._topics[idx % len(self._topics)]
            self._crawl_topic(topic)
            idx += 1

    def _crawl_topic(self, topic: str):
        self.crawler_status["current_topic"] = f"Crawling: {topic}"
        logging.info(f"📚 Crawling: {topic}")

        if not _WIKI_AVAILABLE:
            logging.warning("📚 Wikipedia API unavailable.")
            return

        try:
            page = _WIKI.page(topic)
            if not page.exists():
                logging.warning(f"📚 No Wikipedia page for '{topic}'")
                return

            # Extract first 5 sections as concepts
            summary = page.summary[:1000]
            concepts = [s.strip() for s in summary.split(".") if len(s.strip()) > 20][:5]

            with self._lock:
                self.graph.add_topic(topic, concepts)
                for concept in concepts:
                    self.graph.add_fact(topic, "contains_concept", concept)
                self.facts_learned = len(self.graph.edges)
                self.topics_explored = len(self.graph.topic_concepts)
                self.graph.save()

            logging.info(f"📚 Learned {len(concepts)} concepts from '{topic}'.")
        except Exception as e:
            logging.error(f"📚 Crawl error for '{topic}': {e}")

    def get_learning_metrics(self) -> Dict[str, Any]:
        return {
            "facts_learned": self.facts_learned,
            "topics_explored": self.topics_explored,
            "crawler_status": self.crawler_status,
            "wiki_available": _WIKI_AVAILABLE,
        }

    def query(self, topic: str) -> List[str]:
        """Return known concepts for a topic."""
        with self._lock:
            return self.graph.topic_concepts.get(topic, [])
