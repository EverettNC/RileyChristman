"""
Derek Knowledge: Local RAG System
Standard: 96% Quality Threshold
"""
import logging

class KnowledgeStore:
    def __init__(self):
        # Mock Knowledge Base for Autism & Neurodivergency
        self.documents = [
            {"id": 1, "content": "Autism is a spectrum of neurodevelopmental conditions characterized by challenges with social skills, repetitive behaviors, and speech.", "tags": ["autism", "neurodivergency"]},
            {"id": 2, "content": "Neurodivergency covers a wide range of conditions including ADHD, Autism, Dyslexia, and Dyspraxia.", "tags": ["neurodivergency", "adhd"]},
            {"id": 3, "content": "Stimming is a self-regulatory behavior involving repetitive movements or sounds.", "tags": ["stimming", "autism", "regulation"]},
            {"id": 4, "content": "Offline RAG ensures truth access without internet dependency.", "tags": ["rag", "offline", "truth"]},
            {"id": 5, "content": "Advanced coding requires understanding algorithms, data structures, and system architecture.", "tags": ["coding", "programming"]}
        ]

    def get_all_docs(self):
        return self.documents

class HybridIndexer:
    def __init__(self):
        pass

    def search(self, query, documents):
        """
        Hybrid Search: Keyword matching + Semantic approximation.
        """
        results = []
        query_words = set(query.lower().split())
        
        for doc in documents:
            # Keyword Match
            content_words = set(doc["content"].lower().split())
            intersection = query_words.intersection(content_words)
            
            # Weighted Score (Mock Semantic)
            score = len(intersection)
            if any(tag in query.lower() for tag in doc["tags"]):
                score += 2 # Boost for tag match
                
            if score > 0:
                results.append({"doc": doc, "score": score})
                
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["doc"] for r in results]

class LocalRAG:
    def __init__(self, store, indexer):
        self.store = store
        self.indexer = indexer

    def query(self, query_str):
        docs = self.store.get_all_docs()
        return self.indexer.search(query_str, docs)
