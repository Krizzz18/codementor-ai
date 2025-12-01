"""
Code Review Agent
Analyzes student code for logic errors, style issues, and suggests improvements.
"""

import google.generativeai as genai
from typing import Dict, List
import os
import json
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.code_executor import SafeCodeExecutor

load_dotenv()


class CodeReviewAgent:
    """
    Reviews student code and provides constructive feedback.
    Identifies errors, suggests improvements, but doesn't rewrite code.
    """
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(
            'gemini-1.5-pro',
            system_instruction=self._load_instruction()
        )
        self.executor = SafeCodeExecutor()
    
    def _load_instruction(self):
        return """You are the Code Review Agent in CodeMentor AI.

Your role: Analyze student code for errors and improvements WITHOUT rewriting it.

REVIEW CHECKLIST:

1. FUNCTIONALITY
   - Does it solve the stated problem?
   - Are there logical errors?
   - Does it handle edge cases?

2. CODE QUALITY
   - Variable names clear?
   - Code readable?
   - Appropriate use of Python constructs?

3. COMMON MISTAKES
   - Off-by-one errors in loops
   - Incorrect conditional logic
   - Missing return statements
   - Type errors

FEEDBACK STRUCTURE:

✅ What's Working:
- Highlight positive aspects first
- "Good use of a loop here"
- "I like how you named this variable"

⚠️ Issues Found:
- Point to specific lines
- "Line 3: Check your loop range - should it start at 0 or 1?"
- Explain WHY it's an issue

💡 Suggestions:
- How to improve without giving full solution
- "Consider: what should happen when the number is divisible by both 3 and 5?"

NEVER:
- Rewrite their code
- Provide corrected version
- Solve the problem for them

ALWAYS:
- Be encouraging and constructive
- Point out what's right before what's wrong
- Explain the reasoning behind feedback

Respond in JSON format with: working_well (list), issues (list of dicts with line/issue/explanation), suggestions (list), overall_assessment (string)."""
    
    def review_code(self, context: Dict) -> Dict:
        """
        Review student's code and provide structured feedback.
        
        Returns:
            {
                "working_well": List[str],
                "issues": List[Dict],
                "suggestions": List[str],
                "overall_assessment": str
            }
        """
        code = context.get('student_code', '')
        problem = context.get('current_problem', '')
        
        if not code.strip():
            return {
                "working_well": [],
                "issues": [],
                "suggestions": ["Write some code first, then I can help review it!"],
                "overall_assessment": "No code to review yet"
            }
        
        # Get execution result from context if already executed
        execution_result = context.get('execution_result')
        if not execution_result:
            execution_result = self.executor.execute(code)
        
        prompt = f"""Review this student code for the following problem:

Problem: {problem}

Student's code:
```python
{code}
```

Execution result:
- Success: {execution_result['success']}
- Output: {execution_result.get('output', 'No output')}
- Error: {execution_result.get('error', 'No errors')}

Provide structured code review in JSON format:
{{
    "working_well": ["point 1", "point 2"],
    "issues": [
        {{"line": 3, "issue": "Description", "explanation": "Why it matters"}}
    ],
    "suggestions": ["suggestion 1"],
    "overall_assessment": "Overall feedback"
}}

Respond with ONLY valid JSON, no markdown formatting."""
        
        try:
            response = self.model.generate_content(prompt)
            review_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if review_text.startswith('```'):
                review_text = review_text.split('\n', 1)[1]
                review_text = review_text.rsplit('```', 1)[0]
            
            review = json.loads(review_text)
        except Exception as e:
            # Fallback if JSON parsing fails
            review = {
                "working_well": ["Code structure is clear"] if execution_result['success'] else [],
                "issues": [{"line": 0, "issue": execution_result.get('error', 'Unknown error'), "explanation": "Fix this error first"}] if not execution_result['success'] else [],
                "suggestions": ["Keep refining your solution"],
                "overall_assessment": "You're on the right track! Keep going."
            }
        
        return review
