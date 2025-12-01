"""
A2A Protocol - Agent-to-Agent Communication Schema
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class AgentRole(Enum):
    """Agent role identifiers"""
    ORCHESTRATOR = "orchestrator"
    SOCRATIC = "socratic"
    HINT = "hint"
    REVIEW = "review"
    EXPLAINER = "explainer"


@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication"""
    from_agent: AgentRole
    to_agent: AgentRole
    message_type: str  # "request", "response", "broadcast"
    content: Dict
    context: Optional[Dict] = None


class AgentContext:
    """Shared context across all agents"""
    def __init__(self):
        self.student_code = ""
        self.current_problem = ""
        self.attempt_count = 0
        self.concepts_covered = []
        self.identified_gaps = []
        self.session_history = []
        
    def to_dict(self):
        return {
            "student_code": self.student_code,
            "current_problem": self.current_problem,
            "attempt_count": self.attempt_count,
            "concepts_covered": self.concepts_covered,
            "identified_gaps": self.identified_gaps
        }
