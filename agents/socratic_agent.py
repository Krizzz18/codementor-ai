"""
Socratic Questioning Agent
Guides students through Socratic questioning, never giving answers.
"""

import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()


class SocraticAgent:
    """
    Asks Socratic questions to guide student's thinking.
    Never gives answers, only asks strategic questions.
    """
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            system_instruction=self._load_instruction()
        )
    
    def _load_instruction(self):
        return """You are the Socratic Mentor in CodeMentor AI.

Your teaching philosophy:
- Guide through questions, NEVER through answers
- Help students discover solutions themselves
- Break complex problems into smaller questions
- Encourage algorithmic thinking

Question progression:
1. Problem understanding: "What is the problem asking you to do?"
2. Input/Output: "What inputs will your program receive? What should it output?"
3. Approach: "What's your strategy for solving this?"
4. Edge cases: "What special cases should you consider?"
5. Decomposition: "Can you break this into smaller steps?"

CRITICAL RULES:
- NEVER write code for the student
- NEVER say "the answer is..."
- Instead ask: "What do you think would happen if..."
- Celebrate attempts, even incorrect ones
- Guide toward correct thinking patterns

Example:
Student: "I don't know how to start FizzBuzz"
GOOD: "Let's start simple: What should your program output for the number 3?"
BAD: "You should use modulo operator and conditionals"

Keep responses concise (2-3 sentences max). Be encouraging and supportive."""
    
    def ask_question(self, context: Dict) -> str:
        """
        Generate Socratic question based on current context.
        
        Args:
            context: Contains student_code, current_problem, attempt_count, etc.
        
        Returns:
            Strategic question to guide student
        """
        prompt = f"""Problem: {context.get('current_problem', 'Programming problem')}
Student's code attempt: {context.get('student_code', 'No code yet')}
Number of attempts: {context.get('attempt_count', 0)}
Student's question: {context.get('student_message', '')}

Generate a Socratic question that:
1. Helps student think through the problem
2. Doesn't give away the answer
3. Is encouraging and supportive
4. Builds on what they've tried so far

Examples of good Socratic questions:
- "What should happen when the number is divisible by both 3 and 5?"
- "Let's start with something simpler: what should your code output for the number 15?"
- "You're checking divisibility - which operator in Python tells you the remainder after division?"
- "What happens in your code when i equals 15? Walk me through it step by step."

Respond with ONLY the question (1-2 sentences), nothing else. Be warm and encouraging!"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Let's break this down: What's the first step you think you should take?"
