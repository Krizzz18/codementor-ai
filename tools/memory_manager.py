"""
Student Learning Memory Management
"""

from typing import List, Dict


class StudentMemoryManager:
    """
    Manages student learning history using vector embeddings.
    Tracks concepts learned, common mistakes, progress over time.
    
    For hackathon: Using simple in-memory storage.
    Production: Would use Vertex AI Vector Search.
    """
    def __init__(self, project_id: str = "demo", location: str = "us-central1"):
        self.memory_store = {}
        self.concept_history = []
        self.session_count = 0
        
    def store_session(self, session_id: str, student_data: Dict):
        """Store session data for long-term memory"""
        self.memory_store[session_id] = student_data
        self.session_count += 1
        
    def retrieve_similar_sessions(self, current_problem: str, top_k: int = 3):
        """Retrieve similar past learning sessions"""
        # For demo: return mock data
        # Production: embedding similarity search
        return []
    
    def track_concept_mastery(self, concept: str, mastery_level: float):
        """Track student's understanding of specific concepts"""
        self.concept_history.append({
            "concept": concept,
            "mastery": mastery_level,
            "timestamp": "now"
        })
        
    def get_concept_mastery(self, concept: str) -> float:
        """Get current mastery level for a concept"""
        relevant = [h for h in self.concept_history if h["concept"] == concept]
        if not relevant:
            return 0.0
        return relevant[-1]["mastery"]
