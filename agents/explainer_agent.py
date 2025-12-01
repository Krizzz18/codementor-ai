"""
Concept Explainer Agent
Teaches fundamental concepts when gaps are identified.
"""

import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()


class ConceptExplainerAgent:
    """
    Explains programming concepts in simple terms with examples.
    Activated when student demonstrates conceptual gap.
    """
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel(
            'gemini-1.5-pro',
            system_instruction=self._load_instruction()
        )
        self.concept_database = self._load_concepts()
    
    def _load_instruction(self):
        return """You are the Concept Explainer Agent in CodeMentor AI.

Your role: Break down complex programming concepts into digestible explanations.

TEACHING PRINCIPLES:

1. START SIMPLE
   - Begin with intuition, not jargon
   - Use analogies from everyday life
   - "Think of a list like a shopping cart - you can add and remove items"

2. BUILD GRADUALLY
   - Progress from simple to complex
   - Connect new concepts to what student already knows
   - Show progression: concept → syntax → example

3. USE EXAMPLES
   - Provide 2-3 concrete examples
   - Show both correct and incorrect usage
   - Include edge cases

EXPLANATION STRUCTURE:

📖 What is it? (One-sentence definition, no jargon)
🤔 Why do we need it? (Real-world programming use case)
💻 How does it work? (Simple code example with annotations)
⚠️ Common Mistakes (Typical errors students make)

Keep explanations concise (200-300 words), appropriate for beginner programmer."""
    
    def _load_concepts(self):
        """Pre-load common programming concepts"""
        return {
            "modulo": {
                "definition": "The modulo operator (%) returns the remainder after division",
                "analogy": "Like sharing cookies: 7 cookies ÷ 3 people = 2 cookies per person with 1 left over. That leftover is the modulo: 7 % 3 = 1",
                "example": "# Check if number is divisible by 3\nif num % 3 == 0:\n    print('Divisible by 3')\n\n# Check if even or odd\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')",
                "use_case": "Perfect for FizzBuzz! Use % to check divisibility",
                "common_mistakes": "Don't use / (division) when you mean % (modulo). Example: if num / 3 == 0 is WRONG, use num % 3 == 0"
            },
            "conditionals": {
                "definition": "if/elif/else statements let your code make decisions",
                "analogy": "Like a choose-your-own-adventure book: if this happens, do that; otherwise, do something else",
                "example": "# Simple if-else\nif temperature > 30:\n    print('Hot')\nelse:\n    print('Not hot')\n\n# Multiple conditions\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')",
                "use_case": "Execute different code based on conditions",
                "common_mistakes": "Order matters! Check most specific conditions first. For FizzBuzz, check 'divisible by both 3 AND 5' BEFORE checking 'divisible by 3'"
            },
            "loops": {
                "definition": "Loops repeat code multiple times",
                "analogy": "Like doing jumping jacks: you repeat the same motion 10 times",
                "example": "# For loop with range\nfor i in range(5):\n    print(i)  # Prints 0, 1, 2, 3, 4\n\n# For loop from 1 to 100\nfor i in range(1, 101):\n    print(i)  # Prints 1, 2, 3, ..., 100",
                "use_case": "When you need to do something repeatedly",
                "common_mistakes": "range(100) gives 0-99, NOT 1-100. Use range(1, 101) for 1-100"
            },
            "indentation": {
                "definition": "Python uses indentation (spaces/tabs) to define code blocks",
                "analogy": "Like organizing folders: items inside a folder are indented to show they belong to that folder",
                "example": "# CORRECT - code inside if is indented\nif x > 5:\n    print('Greater than 5')  # 4 spaces indent\n    print('This also runs')\n\n# WRONG - missing indent\nif x > 5:\nprint('Error!')  # This causes IndentationError",
                "use_case": "Every if, elif, else, for, while, def needs indented code below it",
                "common_mistakes": "Mix of tabs and spaces causes errors. Use 4 spaces consistently. Don't forget to indent ALL lines inside a block"
            },
            "variables": {
                "definition": "Variables store values that you can use and change later",
                "analogy": "Like labeled boxes: you put something in a box and give it a name so you can find it later",
                "example": "# Create variables\nname = 'Alice'\nage = 25\nscore = 95.5\n\n# Use variables\nprint(name)  # Prints: Alice\nage = age + 1  # Now age is 26",
                "use_case": "Store data you need to remember and use multiple times",
                "common_mistakes": "NameError means you're using a variable that doesn't exist. Define it before using it!"
            },
            "functions": {
                "definition": "Functions are reusable blocks of code that perform a specific task",
                "analogy": "Like a recipe: write it once, use it many times",
                "example": "# Define function\ndef greet(name):\n    print(f'Hello, {name}!')\n\n# Call function\ngreet('Alice')  # Prints: Hello, Alice!\ngreet('Bob')    # Prints: Hello, Bob!",
                "use_case": "Organize code and avoid repetition",
                "common_mistakes": "Don't forget the () when calling a function: greet('Alice') not greet"
            },
            "operators": {
                "definition": "Operators perform operations on values: +, -, *, /, %, ==, !=, <, >",
                "analogy": "Like math symbols: + adds, - subtracts, etc.",
                "example": "# Arithmetic\nresult = 10 + 5  # 15\nresult = 10 % 3  # 1 (remainder)\n\n# Comparison\nif age >= 18:\n    print('Adult')\n\n# Logical\nif age >= 18 and age < 65:\n    print('Working age')",
                "use_case": "Perform calculations and comparisons",
                "common_mistakes": "Use == for comparison (if x == 5), not = which is for assignment (x = 5)"
            }
        }
    
    def explain_concept(self, concept_name: str, context: Dict = None) -> str:
        """Provide detailed explanation of a programming concept"""
        concept_name_lower = concept_name.lower()
        
        # Check if pre-loaded
        if concept_name_lower in self.concept_database:
            data = self.concept_database[concept_name_lower]
            explanation = f"""**Understanding: {concept_name.title()}**

📖 **What is it?**
{data['definition']}

🤔 **Think of it like this:**
{data['analogy']}

💻 **Example:**
```python
{data['example']}
```

🎯 **When to use it:**
{data['use_case']}"""
            
            if 'common_mistakes' in data:
                explanation += f"""

⚠️ **Common Mistakes:**
{data['common_mistakes']}"""
            
            return explanation
        
        # Otherwise use LLM with better prompt
        error_context = context.get('reason', '') if context else ''
        prompt = f"""You are a programming tutor explaining the concept of "{concept_name}" to a beginner student.

{f"The student got this error: {error_context}" if error_context else ""}

Provide a clear, helpful explanation with:

📖 What is it? (1 sentence, no jargon)
🤔 Analogy: (Simple real-world comparison)
💻 Code Example: (Python code with comments showing correct usage)
🎯 When to use it: (Practical use case)
⚠️ Common Mistakes: (What students often do wrong)

Keep it concise but complete. Use markdown formatting. Be encouraging!"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Better fallback
            return f"""**Understanding: {concept_name.title()}**

I'm having trouble connecting to my knowledge base right now, but here's what I can tell you:

The concept of **{concept_name}** is fundamental in Python programming. 

🔍 **Quick tip:** Try writing a simple example and submit it for review. I'll be able to give you specific feedback on your code!

💡 **In the meantime:** Think about what you're trying to accomplish. What should your code do? Break it down into small steps."""
    
    def identify_concept_gap(self, student_code: str, error: str) -> str:
        """Identify which concept student is struggling with"""
        prompt = f"""Analyze this student code and error to identify conceptual gap:

Code:
```python
{student_code}
```

Error: {error}

Which fundamental programming concept is the student struggling with?
Return only ONE word: modulo, loops, conditionals, functions, variables, lists, strings, or other.
Respond with ONLY the concept name, nothing else."""
        
        try:
            response = self.model.generate_content(prompt)
            concept = response.text.strip().lower()
            # Clean up response
            concept = concept.split()[0] if concept else "conditionals"
            return concept
        except Exception as e:
            return "conditionals"
