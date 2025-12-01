"""Quick debug test"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator()

bad_code = """
for i in range(1, 16):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    if i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
"""

print("=== FIRST ATTEMPT ===")
response1 = orchestrator.process_student_input("First try", bad_code)
print(f"Agent: {response1['agent_used']}")
print(f"Attempt count: {orchestrator.context.attempt_count}")

print("\n=== SECOND ATTEMPT ===")
response2 = orchestrator.process_student_input("Second try", bad_code)
print(f"Agent: {response2['agent_used']}")
print(f"Attempt count: {orchestrator.context.attempt_count}")
print(f"Has output: {bool(response2['metadata']['execution'].get('output'))}")
print(f"Has issues: {len(response2['metadata']['review'].get('issues', []))}")
