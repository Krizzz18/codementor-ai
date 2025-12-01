"""
Multi-Agent Orchestrator
Coordinates all teaching agents using A2A protocol.
"""

from typing import Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.socratic_agent import SocraticAgent
from agents.hint_agent import HintAgent
from agents.review_agent import CodeReviewAgent
from agents.explainer_agent import ConceptExplainerAgent
from agents.a2a_protocol import AgentContext
from tools.memory_manager import StudentMemoryManager
from tools.code_executor import SafeCodeExecutor


class MultiAgentOrchestrator:
    """
    Root orchestrator coordinates 4 teaching agents.
    Implements A2A protocol for inter-agent communication.
    """
    
    # Default FizzBuzz problem for testing and demo
    DEFAULT_PROBLEM = """Write a function fizzbuzz() that prints numbers from 1 to 100.
- For multiples of 3, print "Fizz"
- For multiples of 5, print "Buzz"
- For multiples of both 3 and 5, print "FizzBuzz"
- Otherwise, print the number"""
    
    def __init__(self):
        # Initialize all specialist agents
        self.socratic = SocraticAgent()
        self.hint_provider = HintAgent()
        self.code_reviewer = CodeReviewAgent()
        self.explainer = ConceptExplainerAgent()
        
        # Memory and tools
        self.memory = StudentMemoryManager(project_id="demo", location="us-central1")
        self.executor = SafeCodeExecutor()
        
        # Shared context across agents
        self.context = AgentContext()
        # Set default problem
        self.context.current_problem = self.DEFAULT_PROBLEM
    
    def process_student_input(self, student_message: str, code_attempt: str = "") -> Dict:
        """
        Main orchestration logic:
        1. Update context
        2. Decide which agent(s) to activate
        3. Coordinate agent responses
        4. Return unified response to student
        
        Returns:
            {
                "response": str,
                "agent_used": str,
                "metadata": Dict
            }
        """
        # Update shared context
        self.context.student_code = code_attempt
        self.context.attempt_count += 1
        self.context.session_history.append({
            "message": student_message,
            "code": code_attempt,
            "attempt": self.context.attempt_count
        })
        
        response_data = {}
        
        # Decision logic: Which agent to activate?
        
        # 1. If student has code, review it first
        if code_attempt.strip():
            execution = self.executor.execute(code_attempt)
            review = self.code_reviewer.review_code({
                **self.context.to_dict(),
                "execution_result": execution
            })
            
            if not execution["success"] and execution.get("error"):
                # Code has syntax or runtime error - check if it's a concept gap
                error_msg = execution["error"].lower()
                
                # Only explain concepts for specific error types
                needs_explanation = False
                concept_gap = None
                
                if "nameerror" in error_msg or "not defined" in error_msg:
                    concept_gap = "variables"
                    needs_explanation = True
                elif "syntaxerror" in error_msg and "%" in code_attempt and "/" in code_attempt:
                    concept_gap = "modulo"
                    needs_explanation = True
                elif "indentationerror" in error_msg:
                    concept_gap = "indentation"
                    needs_explanation = True
                
                if needs_explanation and concept_gap:
                    # Activate Explainer Agent
                    explanation = self.explainer.explain_concept(
                        concept_gap,
                        context={"reason": f"Error: {execution['error']}"}
                    )
                    self.context.identified_gaps.append(concept_gap)
                    
                    # Track concept mastery
                    if concept_gap not in self.context.concepts_covered:
                        self.context.concepts_covered.append(concept_gap)
                    
                    response_data = {
                        "response": f"I noticed you might need help with **{concept_gap}**. Let me explain:\n\n{explanation}\n\n**Now try fixing your code!**",
                        "agent_used": "explainer",
                        "metadata": {
                            "concept": concept_gap,
                            "review": review,
                            "execution": execution
                        }
                    }
                else:
                    # No clear concept gap - provide hint
                    hint = self.hint_provider.generate_hint({
                        **self.context.to_dict(),
                        "error_message": execution["error"],
                        "student_code": code_attempt
                    })
                    response_data = {
                        "response": f"{hint['encouragement']}\n\n**💡 Hint (Level {hint['difficulty']}/4):**\n{hint['hint']}\n\n**Error details:** {execution['error']}",
                        "agent_used": "hint",
                        "metadata": {
                            "review": review,
                            "hint_level": hint['difficulty'],
                            "execution": execution
                        }
                    }
            else:
                # Code runs without errors
                has_issues = review["issues"] and len(review["issues"]) > 0
                
                # Check if code is COMPLETE (MUST produce FizzBuzz output for FizzBuzz problem)
                output = execution.get("output", "")
                # For FizzBuzz, require ALL three outputs to be present
                is_fizzbuzz_complete = (
                    "FizzBuzz" in output and 
                    output.count("Fizz") > 1 and  # Multiple Fizz outputs
                    output.count("Buzz") > 1      # Multiple Buzz outputs
                )
                # Mark as complete only if FizzBuzz is done correctly
                is_complete_solution = is_fizzbuzz_complete
                
                # Static analysis for FizzBuzz-specific issues
                fizzbuzz_issues = []
                if "fizzbuzz" in self.context.current_problem.lower():
                    # Check for common FizzBuzz mistakes
                    if "/" in code_attempt and "%" not in code_attempt:
                        fizzbuzz_issues.append({
                            "issue": "Using division (/) instead of modulo (%) for divisibility check",
                            "hint": "Remember: To check if a number is divisible, use the modulo operator %"
                        })
                        # Trigger explainer for modulo concept
                        if "modulo" not in self.context.concepts_covered:
                            self.context.concepts_covered.append("modulo")
                    
                    if "%" in code_attempt:
                        # Has modulo but missing FizzBuzz case?
                        if "FizzBuzz" not in output and ("% 15" not in code_attempt and "% 3" in code_attempt and "% 5" in code_attempt):
                            # Checking 3 and 5 separately but not 15 (or 3 and 5 together)
                            if "and" not in code_attempt and "% 15" not in code_attempt:
                                fizzbuzz_issues.append({
                                    "issue": "Missing the FizzBuzz case (divisible by both 3 AND 5)",
                                    "hint": "What should happen when a number is divisible by BOTH 3 and 5?"
                                })
                    
                    if "Fizz" not in output and "Buzz" not in output:
                        fizzbuzz_issues.append({
                            "issue": "Code doesn't output Fizz or Buzz yet",
                            "hint": "Your loop is working! Now add conditions to check divisibility."
                        })
                
                # Override has_issues if we found FizzBuzz-specific problems
                if fizzbuzz_issues:
                    has_issues = True
                    # Add to review issues
                    for fi in fizzbuzz_issues:
                        review["issues"].append({"line": "?", "issue": fi["issue"], "explanation": fi["hint"]})
                
                # After 2+ attempts, provide hints UNLESS code is complete
                if self.context.attempt_count >= 2 and has_issues and not is_complete_solution:
                    hint = self.hint_provider.generate_hint({
                        **self.context.to_dict(),
                        "error_message": "Code runs but may need improvement",
                        "student_code": code_attempt,
                        "review_issues": review.get("issues", [])
                    })
                    response_data = {
                        "response": f"{hint['encouragement']}\n\n**💡 Hint (Level {hint['difficulty']}/4):**\n{hint['hint']}" + (
                            "\n\n⚠️ **Issues found:**\n" + "\n".join(f"- Line {issue.get('line', '?')}: {issue.get('issue', '')}" for issue in review["issues"][:2])
                            if has_issues else ""
                        ),
                        "agent_used": "hint",
                        "metadata": {
                            "review": review,
                            "hint_level": hint['difficulty'],
                            "execution": execution
                        }
                    }
                elif is_complete_solution:
                    # SUCCESS! Code is complete - celebrate with reviewer
                    response_parts = ["🎉 **Excellent work! Your solution is correct!**\n"]
                    
                    if review["working_well"]:
                        response_parts.append("✅ **What's working well:**\n" + "\n".join(f"- {item}" for item in review["working_well"]))
                    
                    if review["suggestions"]:
                        response_parts.append("\n💡 **Optional improvements:**\n" + "\n".join(f"- {sug}" for sug in review["suggestions"]))
                    
                    response_parts.append("\n\n🏆 **Congratulations on solving the problem!**")
                    
                    response_data = {
                        "response": "\n".join(response_parts),
                        "agent_used": "reviewer",
                        "metadata": {
                            "review": review,
                            "execution": execution,
                            "success": True
                        }
                    }
                else:
                    # First attempt with incomplete code - provide review feedback
                    response_parts = []
                    
                    if review["working_well"]:
                        response_parts.append("✅ **What's working well:**\n" + "\n".join(f"- {item}" for item in review["working_well"]))
                    
                    if review["issues"]:
                        response_parts.append("\n⚠️ **Areas to improve:**")
                        for issue in review["issues"]:
                            response_parts.append(f"- Line {issue.get('line', '?')}: {issue.get('issue', 'Check this')} - {issue.get('explanation', '')}")
                    
                    if review["suggestions"]:
                        response_parts.append("\n💡 **Suggestions:**\n" + "\n".join(f"- {sug}" for sug in review["suggestions"]))
                    
                    if not response_parts:
                        response_parts.append("Good start! Your code runs successfully. Keep refining!")
                    
                    response_data = {
                        "response": "\n".join(response_parts),
                        "agent_used": "reviewer",
                        "metadata": {
                            "review": review,
                            "execution": execution
                        }
                    }
        
        # 2. If no code yet, or student asking question
        else:
            # Activate Socratic Agent
            question = self.socratic.ask_question({
                **self.context.to_dict(),
                "student_message": student_message
            })
            
            response_data = {
                "response": question,
                "agent_used": "socratic",
                "metadata": {
                    "attempt_count": self.context.attempt_count
                }
            }
        
        # Update memory system
        self.memory.store_session(
            session_id=f"session_{self.context.attempt_count}",
            student_data=self.context.to_dict()
        )
        
        return response_data
