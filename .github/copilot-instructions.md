# CodeMentor AI - AI Agent Instructions

## Project Overview
Multi-agent educational tutoring system (Google Agents Intensive Capstone). **4 specialized teaching agents + 1 orchestrator** guide students through programming problems using Socratic methodology. Built with Google Gemini API, Streamlit UI, safe code execution sandbox.

**Core Principle**: Agents **NEVER solve problems** - they guide learning through questions, hints, and concept explanations.

## Architecture: Multi-Agent Orchestration

### Agent Routing Logic (`agents/orchestrator.py`)
The orchestrator decides which agent activates based on student state:

```python
# Decision tree:
if code_submitted:
    if execution_error:
        if concept_gap_detected (NameError, IndentationError, modulo confusion):
            → Explainer Agent (teaches concept)
        else:
            → Hint Agent (progressive guidance)
    else:  # code runs
        if attempt_count >= 2:
            → Hint Agent (push toward improvement)
        else:
            → Review Agent (first-attempt feedback)
else:  # no code yet
    → Socratic Agent (guiding questions)
```

**Critical Pattern**: After 2+ attempts, system switches from passive review to active hints - this prevents students from spinning wheels.

### Shared Context (`agents/a2a_protocol.py`)
All agents access `AgentContext` with:
- `attempt_count`: Drives hint difficulty scaling
- `concepts_covered`: Tracks learning progress (displayed in UI sidebar)
- `student_code`: Current code submission
- `session_history`: Full conversation for context

**Do NOT** create separate context per agent - context is **shared singleton** updated by orchestrator.

## Agent Implementation Patterns

### System Instructions Architecture
Each agent uses **constraint-based prompting**:

```python
# agents/socratic_agent.py
system_instruction = """
NEVER give direct answers or code solutions
Ask guiding questions that help students think
Examples of GOOD: "What's the first step?"
Examples of BAD: "Use a for loop with range(1, 101)"
"""
```

**Key Pattern**: Agents are constrained by what they **cannot** do (pedagogical guardrails). When adding features, extend constraints, don't remove them.

### Model Selection Strategy
- **Gemini 2.0 Flash**: Fast responses (Socratic questions, hints) - sub-2s latency
- **Gemini 1.5 Pro**: Deep reasoning (code review, concept explanation) - 3-5s latency

**Do NOT** use 1.5 Pro for simple text generation - costs 10x more and slower.

### Response Format Standards
Agents return consistent structure:
```python
{
    "response": str,        # Markdown-formatted text for UI
    "agent_used": str,      # "socratic"|"hint"|"reviewer"|"explainer"
    "metadata": {           # Agent-specific data
        "concept": str,     # (Explainer) concept taught
        "hint_level": int,  # (Hint) difficulty 1-4
        "review": dict      # (Reviewer) structured feedback
    }
}
```

## Code Execution Sandbox (`tools/code_executor.py`)

### Security Model
**Windows-compatible threading** (not signal-based):
```python
# CRITICAL: Windows doesn't support signal.SIGALRM
thread = threading.Thread(target=run_code)
thread.daemon = True
thread.start()
thread.join(timeout=5.0)  # Hard 5-second limit
```

### Builtins Whitelist
35+ allowed builtins including `range`, `len`, `print`, `enumerate`, etc. **Do NOT** add file I/O (`open`, `file`), network (`socket`, `urllib`), or subprocess (`os.system`, `subprocess`).

**Common Bug**: If code execution fails with "name 'X' is not defined", add `X` to `ALLOWED_BUILTINS` list, don't modify execution logic.

## Streamlit UI Patterns (`app.py`)

### Session State Initialization
**MUST initialize all session state keys** before use:
```python
if 'attempt_count' not in st.session_state:
    st.session_state.attempt_count = 0
if 'concepts_learned' not in st.session_state:
    st.session_state.concepts_learned = set()  # Note: set() not list
```

**Common Error**: `AttributeError: st.session_state has no attribute "X"` → missing initialization block.

### Two-Column Layout
```python
col_chat, col_code = st.columns([1, 1], gap="large")
with col_chat:
    # Conversation panel (left)
with col_code:
    # Code editor (right)
```

**Do NOT** modify layout structure - it's core UX. To add features, nest within existing columns.

### Agent Color Coding
```python
agent_names = {
    "socratic": "🤔 Socratic Mentor",
    "hint": "💡 Hint Provider",
    "reviewer": "✅ Code Reviewer",
    "explainer": "📚 Concept Explainer"
}
```

UI uses CSS classes `.socratic`, `.hint`, `.reviewer`, `.explainer` with distinct colors. Maintain visual consistency when adding agents.

## Testing Strategy (`tests/test_critical_features.py`)

### Strict Testing Philosophy
Tests use **isolated orchestrators** to prevent state leakage:
```python
def test_hint_agent():
    orchestrator1 = MultiAgentOrchestrator()  # Fresh instance
    response1 = orchestrator1.process_student_input(...)
    
    orchestrator2 = MultiAgentOrchestrator()  # New instance for next test
    response2 = orchestrator2.process_student_input(...)
```

**Anti-pattern**: Reusing single orchestrator across tests - `attempt_count` bleeds between tests.

### Test Assertions
Tests verify **agent routing**, not content quality:
```python
assert response["agent_used"] == "hint"  # ✅ Correct routing
# NOT: assert "modulo" in response["response"]  # ❌ Fragile LLM output check
```

## Development Workflows

### Local Testing
```bash
# 1. Test code execution sandbox
python -c "from tools.code_executor import SafeCodeExecutor; print(SafeCodeExecutor().execute('print(range(5))'))"

# 2. Run full test suite
pytest tests/test_critical_features.py -v

# 3. Launch UI
streamlit run app.py
```

### Debugging Agent Responses
Create `debug_test.py` scripts:
```python
from agents.orchestrator import MultiAgentOrchestrator
orch = MultiAgentOrchestrator()
result = orch.process_student_input("test message", "print('hi')")
print(f"Agent: {result['agent_used']}")
print(f"Response: {result['response'][:100]}")
```

**Do NOT** debug by launching full Streamlit app - too slow for iteration.

### Environment Setup
API key **MUST** be in `.env` file:
```bash
GOOGLE_API_KEY=your_actual_key_here
```

**Never** commit `.env` file. Check `.gitignore` includes it.

## Common Pitfalls

1. **Modifying orchestrator logic without updating tests**: Tests have strict assertions about which agent activates when. Update `test_critical_features.py` if routing changes.

2. **Adding CSS that breaks layout**: Streamlit's native column system is fragile. Test on `localhost:8501` after CSS changes, not just code editor preview.

3. **F-strings with triple-quoted strings**: Cannot nest triple quotes in f-strings. Extract variables first:
   ```python
   # ❌ WRONG
   prompt = f"""Problem: {problem}
   Code: {student_code.replace('\n', '<br>')}"""
   
   # ✅ CORRECT
   code_html = student_code.replace('\n', '<br>')
   prompt = f"""Problem: {problem}
   Code: {code_html}"""
   ```

4. **Forgetting attempt counter increments**: Orchestrator increments on EVERY call. Don't manually increment in UI code - leads to double-counting.

## File Organization Conventions

- `agents/`: One agent per file, no utility functions
- `tools/`: Reusable utilities (code execution, memory)
- `demo/`: Presentation scripts (not production code)
- `tests/`: Unit tests mirror `agents/` structure

**Do NOT** create `utils/` or `helpers/` directories - keep flat structure for hackathon simplicity.

## Key Files Reference

- **`agents/orchestrator.py`**: Lines 67-170 = routing decision tree (read this first)
- **`tools/code_executor.py`**: Lines 38-63 = builtins whitelist (modify for new features)
- **`app.py`**: Lines 192-290 = two-column layout (UI core, touch carefully)
- **`agents/explainer_agent.py`**: Lines 28-95 = concept database (extend for new topics)

## Questions for Clarification

1. **Memory Integration**: Current `memory_manager.py` is stubbed for Vertex AI Vector Search. Should production use Firebase, Postgres, or stick with in-memory for demo?

2. **Multi-Language Support**: Architecture assumes Python execution. To add JavaScript/Java, should we create separate `JSCodeExecutor` classes or abstract `BaseExecutor`?

3. **Agent Expansion**: If adding 5th teaching agent (e.g., "Debugging Detective"), should it fit existing routing logic or require orchestrator refactor?

4. **Deployment Strategy**: Streamlit Cloud vs. Cloud Run? Impacts session state persistence approach.
