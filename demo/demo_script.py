"""
Pre-scripted Demo Flow for Presentations
Demonstrates multi-agent collaboration on FizzBuzz problem
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import MultiAgentOrchestrator


DEMO_PROBLEM = """Write a function fizzbuzz() that prints numbers from 1 to 100.
- For multiples of 3, print "Fizz"
- For multiples of 5, print "Buzz"
- For multiples of both 3 and 5, print "FizzBuzz"
- Otherwise, print the number"""

DEMO_FLOW = [
    {
        "step": 1,
        "student_message": "I need help with FizzBuzz. I don't know where to start.",
        "code": "",
        "narration": "🎬 Student asks for help. Socratic Agent guides with questions.",
        "expected_agent": "socratic"
    },
    {
        "step": 2,
        "student_message": "I think I need a loop?",
        "code": "for i in range(100):\n    print(i)",
        "narration": "🎬 Student submits basic loop. Let's see which agent responds...",
        "expected_agent": "hint"
    },
    {
        "step": 3,
        "student_message": "How do I check divisibility?",
        "code": "for i in range(1, 101):\n    if i / 3 == 0:\n        print('Fizz')\n    else:\n        print(i)",
        "narration": "🎬 Code has error (division vs modulo). Explainer Agent should teach modulo.",
        "expected_agent": "explainer"
    },
    {
        "step": 4,
        "student_message": "Let me try with modulo",
        "code": "for i in range(1, 101):\n    if i % 3 == 0:\n        print('Fizz')\n    elif i % 5 == 0:\n        print('Buzz')\n    else:\n        print(i)",
        "narration": "🎬 Better code, but missing FizzBuzz case. Code Reviewer points out logic gap.",
        "expected_agent": "reviewer"
    },
    {
        "step": 5,
        "student_message": "Fixed it!",
        "code": "def fizzbuzz():\n    for i in range(1, 101):\n        if i % 3 == 0 and i % 5 == 0:\n            print('FizzBuzz')\n        elif i % 3 == 0:\n            print('Fizz')\n        elif i % 5 == 0:\n            print('Buzz')\n        else:\n            print(i)\n\nfizzbuzz()",
        "narration": "🎬 Complete solution! Code Reviewer celebrates success.",
        "expected_agent": "reviewer"
    }
]


def run_demo():
    """Execute automated demo flow"""
    print("=" * 70)
    print("🎓 CodeMentor AI - Multi-Agent Programming Tutor Demo")
    print("=" * 70)
    print("\nProblem:")
    print(DEMO_PROBLEM)
    print("\n" + "=" * 70 + "\n")
    
    orchestrator = MultiAgentOrchestrator()
    orchestrator.context.current_problem = DEMO_PROBLEM
    
    for step_data in DEMO_FLOW:
        print(f"\n{'='*70}")
        print(f"STEP {step_data['step']}")
        print(f"{'='*70}")
        print(f"\n{step_data['narration']}\n")
        
        print(f"👨‍💻 Student: {step_data['student_message']}")
        
        if step_data['code']:
            print("\n💻 Code Submitted:")
            print("─" * 70)
            print(step_data['code'])
            print("─" * 70)
        
        # Process with orchestrator
        print("\n⏳ Processing...\n")
        time.sleep(1)  # Dramatic pause
        
        response = orchestrator.process_student_input(
            student_message=step_data['student_message'],
            code_attempt=step_data['code']
        )
        
        # Display response with agent icon
        agent_icons = {
            "socratic": "🤔",
            "hint": "💡",
            "reviewer": "✅",
            "explainer": "📚"
        }
        icon = agent_icons.get(response['agent_used'], "🤖")
        
        print(f"{icon} {response['agent_used'].upper()} AGENT:")
        print("─" * 70)
        print(response['response'])
        print("─" * 70)
        
        # Pause between steps
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print("🎉 DEMO COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Learning Journey Summary:")
    print(f"   Total Attempts: {orchestrator.context.attempt_count}")
    print(f"   Concepts Learned: {', '.join(orchestrator.context.concepts_covered) or 'None yet'}")
    print(f"   Agent Activations:")
    
    # Count agent activations
    from collections import Counter
    agent_counts = Counter()
    for entry in orchestrator.context.session_history:
        agent_counts['interactions'] += 1
    
    print(f"   - Total interactions: {len(orchestrator.context.session_history)}")
    print("\n✨ This demonstrates multi-agent collaboration for educational impact!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_demo()
