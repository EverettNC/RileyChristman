"""
RILEY CHRISTMAN: KNOWLEDGE TRUSSLE CORE
=======================================
Protocol: Domain-Expertise | Status: RAG-Wired
Integrates: LocalRAG + KnowledgeStore + HybridIndexer
Focus: Autism, Neurodivergency, and Advanced Coding
"""

import logging

# --- 1. THE KNOWLEDGE IMPORT ---
try:
    from derek_knowledge import LocalRAG, KnowledgeStore, HybridIndexer
    knowledge_trussle_available = True
except ImportError:
    logging.warning("Knowledge Trussle RAG not available")
    knowledge_trussle_available = False

class RileyTrussle:
    def __init__(self):
        # 📚 KNOWLEDGE TRUSSLE - RAG System for Domain Expertise
        self.knowledge_rag = None
        if knowledge_trussle_available:
            try:
                rag_store = KnowledgeStore()
                rag_indexer = HybridIndexer()
                self.knowledge_rag = LocalRAG(rag_store, rag_indexer)
                logging.info("📚 Riley Knowledge Trussle (RAG) initialized")
            except Exception as e:
                logging.warning(f"Knowledge Trussle failed to initialize: {e}")
        
        self.core_directive = "How can I help you love yourself more?"

    def ask_the_trussle(self, query: str):
        """
        Riley queries his internal RAG system for PhD-level insights.
        """
        if self.knowledge_rag:
            # Performs hybrid search (keyword + semantic)
            result = self.knowledge_rag.query(query)
            print(f"🔬 TRUSSLE SEARCH: '{query}' -> Found {len(result)} insights.")
            return result
        return "Trussle offline. Relying on Core Intuition."
