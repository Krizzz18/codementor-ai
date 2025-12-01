"""
Progressive Hint Agent
Provides increasingly specific hints based on number of attempts.
"""

import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()


class HintAgent:
    """
    Provides progressive hints - starts vague, gets more specific.
    Hint difficulty adjusts based on student's attempt count.
    """
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            system_instruction=self._load_instruction()
        )
    
    def _load_instruction(self):
        return """You are the Hint Provider Agent in CodeMentor AI.

Your role: Provide just enough information to unblock student without solving the problem.

HINT PROGRESSION STRATEGY:

Attempt 1 (Very Vague):
- High-level approach only
- "Think about using a loop here"
- "Consider what happens when..."

Attempt 2-3 (Conceptual):
- Name the concept, not the code
- "The modulo operator can help determine divisibility"
- "You'll need a conditional statement"

Attempt 4-5 (Structural):
- Describe the structure, not the implementation
- "Use an if-elif-else chain inside your loop"
- "Your function should return a value, not print"

Attempt 6+ (Very Specific):
- Point to exact line that needs fixing
- "Line 5: The condition should check if number % 3 equals 0"
- Still don't write the full solution

CRITICAL RULES:
- Adjust hint specificity based on attempt_count
- NEVER provide complete code (even after 10 attempts)
- Celebrate each attempt before giving next hint
- If student very stuck, suggest looking up specific concept

Keep hints concise (2-4 sentences). Always be encouraging."""
    
    def generate_hint(self, context: Dict) -> Dict:
        """
        Generate appropriately specific hint based on attempt count.
        
        Returns:
            {
                "hint": str,
                "difficulty": int (1-5),
                "encouragement": str
            }
        """
        attempt_count = context.get('attempt_count', 0)
        
        # Determine hint difficulty level
        if attempt_count <= 1:
            difficulty = 1  # Very vague
        elif attempt_count <= 3:
            difficulty = 2  # Conceptual
        elif attempt_count <= 5:
            difficulty = 3  # Structural
        else:
            difficulty = 4  # Very specific
        
        code_snippet = context.get('student_code', 'No code yet')
        error_msg = context.get('error_message', 'No error')
        problem = context.get('current_problem', 'Programming problem')
        
        prompt = f"""Problem: {problem}

Student's latest code:
{code_snippet}

Error message: {error_msg}
Attempt number: {attempt_count}
Hint difficulty level: {difficulty}/4

Generate a hint at difficulty level {difficulty}:
- Level 1: High-level approach only
- Level 2: Mention concepts needed (like modulo operator for divisibility)
- Level 3: Describe code structure (if-elif-else chain, order of conditions)
- Level 4: Point to specific lines that need fixing

NEVER write the complete solution. Give just enough guidance for the next step.

Respond with 2-3 sentences. Be specific but don't solve it for them!"""
        
        try:
            response = self.model.generate_content(prompt)
            hint_text = response.text.strip()
        except Exception as e:
            hint_text = "Try breaking the problem into smaller steps."
        
        # Add encouragement
        encouragements = [
            "You're making progress! Keep going.",
            "Good attempt! You're thinking in the right direction.",
            "Nice try! You're getting closer.",
            "I can see you're learning from each attempt!",
            "You're doing great! Just a bit more refinement needed."
        ]
        encouragement = encouragements[min(attempt_count, len(encouragements)-1)]
        
        return {
            "hint": hint_text,
            "difficulty": difficulty,
            "encouragement": encouragement
        }
