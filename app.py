"""
CodeMentor AI - Main Streamlit Application
Multi-Agent Programming Tutor
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# API Key Validation - Fail fast if missing
if not os.getenv('GOOGLE_API_KEY'):
    st.error("⚠️ **Missing API Key!** Please add your Google API key to the `.env` file.")
    st.info("📝 Create a `.env` file in the project root with:\n```\nGOOGLE_API_KEY=your_key_here\n```")
    st.stop()

from agents.orchestrator import MultiAgentOrchestrator
from tools.code_executor import SafeCodeExecutor
from visualization.learning_journey import create_learning_journey_graph, create_concept_mastery_chart

# Page configuration
st.set_page_config(
    page_title="CodeMentor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dark/Light mode compatible styling
st.markdown("""
<style>
/* Agent cards - high contrast, works on any background */
.agent-card {
    padding: 16px 20px;
    border-radius: 12px;
    margin: 12px 0;
    border-left: 5px solid;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.agent-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}

/* Socratic Agent - Red theme */
.socratic { 
    border-color: #FF6B6B;
    background: rgba(255, 107, 107, 0.15);
    color: #FF8A8A;
}
.socratic strong { color: #FF6B6B; }

/* Hint Agent - Teal theme */
.hint { 
    border-color: #4ECDC4;
    background: rgba(78, 205, 196, 0.15);
    color: #6EE7DE;
}
.hint strong { color: #4ECDC4; }

/* Reviewer Agent - Yellow/Gold theme */
.reviewer { 
    border-color: #FFD93D;
    background: rgba(255, 217, 61, 0.15);
    color: #FFE066;
}
.reviewer strong { color: #FFD93D; }

/* Explainer Agent - Green theme */
.explainer { 
    border-color: #95E1D3;
    background: rgba(149, 225, 211, 0.15);
    color: #A8F0E4;
}
.explainer strong { color: #95E1D3; }

/* Student messages - Blue/Green theme */
.student-msg {
    text-align: right;
    padding: 14px 18px;
    margin: 12px 0;
    background: rgba(76, 175, 80, 0.15);
    border-radius: 12px;
    color: #81C784;
    border-right: 5px solid #4CAF50;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
}
.student-msg strong { color: #4CAF50; }

/* Concept badges with glow effect */
.concept-badge {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-size: 12px;
    font-weight: 600;
    box-shadow: 0 3px 10px rgba(102, 126, 234, 0.4);
    transition: transform 0.2s;
}
.concept-badge:hover {
    transform: scale(1.05);
}

/* Buttons with gradient */
.stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 20px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    transition: all 0.3s;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

/* Code editor - transparent to inherit theme */
.stTextArea textarea {
    border: 2px solid rgba(102, 126, 234, 0.5) !important;
    border-radius: 10px !important;
    font-family: 'Fira Code', 'Consolas', 'Monaco', monospace !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
}

/* Sidebar section headers */
.sidebar-header {
    color: #E0E0E0;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
}

/* Make metrics more visible */
[data-testid="stMetric"] {
    background: rgba(102, 126, 234, 0.1);
    padding: 10px;
    border-radius: 8px;
}

/* Fix expander styling */
.streamlit-expanderHeader {
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = MultiAgentOrchestrator()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'code_history' not in st.session_state:
    st.session_state.code_history = []
if 'current_code' not in st.session_state:
    st.session_state.current_code = ""
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = """Write a function fizzbuzz() that prints numbers from 1 to 100.
- For multiples of 3, print "Fizz"
- For multiples of 5, print "Buzz"
- For multiples of both 3 and 5, print "FizzBuzz"
- Otherwise, print the number"""
if 'attempt_count' not in st.session_state:
    st.session_state.attempt_count = 0
if 'concepts_learned' not in st.session_state:
    st.session_state.concepts_learned = set()

# Header
# Header with animated banner
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 40px; border-radius: 20px; text-align: center; 
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3); margin-bottom: 30px;">
    <h1 style="color: white; font-size: 3.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
        🎓 CodeMentor AI
    </h1>
    <p style="color: rgba(255,255,255,0.9); font-size: 1.3rem; margin: 10px 0 0 0;">
        Multi-Agent Programming Tutor • Powered by Google Gemini 2.0
    </p>
    <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 10px 0 0 0;">
        🤔 Socratic Questions • 💡 Progressive Hints • 📝 Code Reviews • 📚 Concept Explanations
    </p>
</div>
""", unsafe_allow_html=True)

# Display current problem
with st.expander("📝 Current Problem", expanded=True):
    st.markdown(st.session_state.current_problem)

# Main layout - Two-column side-by-side
col_chat, col_code = st.columns([1, 1], gap="large")

with col_chat:
    st.subheader("💬 Conversation with AI Mentors")
    
    # Chat container
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            agent = msg.get("agent", "student")
            
            if agent == "student":
                content = msg['content']
                st.markdown(f"""
                <div class="student-msg">
                <strong>You:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                agent_names = {
                    "socratic": "🤔 Socratic Mentor",
                    "hint": "💡 Hint Provider",
                    "reviewer": "✅ Code Reviewer",
                    "explainer": "📚 Concept Explainer"
                }
                name = agent_names.get(agent, "AI Mentor")
                content_html = msg['content'].replace('\n', '<br>')
                
                st.markdown(f"""
                <div class="agent-card {agent}">
                <strong>{name}:</strong><br>
                {content_html}
                </div>
                """, unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    user_input = st.text_input("💭 Ask a question or describe what you're stuck on:", key="user_input")
    
    col_send, col_reset = st.columns([3, 1])
    with col_send:
        send_btn = st.button("📨 Send Message", key="send_btn", type="primary")
    with col_reset:
        reset_btn = st.button("🔄 Reset", key="reset_btn")
    
    if send_btn and user_input:
        # Add user message
        st.session_state.messages.append({
            "agent": "student",
            "content": user_input
        })
        
        # Update orchestrator context with current problem
        st.session_state.orchestrator.context.current_problem = st.session_state.current_problem
        
        # Process with orchestrator
        with st.spinner("🤖 AI Mentors are thinking..."):
            response = st.session_state.orchestrator.process_student_input(
                student_message=user_input,
                code_attempt=st.session_state.current_code
            )
        
        # Add agent response
        st.session_state.messages.append({
            "agent": response["agent_used"],
            "content": response["response"]
        })
        
        # Save code to history if exists
        if st.session_state.current_code.strip():
            st.session_state.code_history.append({
                "attempt": len(st.session_state.code_history) + 1,
                "code": st.session_state.current_code,
                "agent_feedback": response["agent_used"]
            })
            # Update attempt counter
            st.session_state.attempt_count = len(st.session_state.code_history)
        
        # Update concepts learned
        if "metadata" in response and "concept" in response.get("metadata", {}):
            concept = response["metadata"]["concept"]
            st.session_state.concepts_learned.add(concept)
        
        st.rerun()
    
    if reset_btn:
        # Complete reset of all session state
        st.session_state.attempt_count = 0
        st.session_state.concepts_learned = set()
        st.session_state.messages = []
        st.session_state.code_history = []
        st.session_state.orchestrator = MultiAgentOrchestrator()
        st.session_state.current_code = ""
        # Reset orchestrator context properly
        st.session_state.orchestrator.context.attempt_count = 0
        st.session_state.orchestrator.context.concepts_covered = []
        st.session_state.orchestrator.context.session_history = []
        st.rerun()

with col_code:
    st.subheader("💻 Your Code Editor")
    
    # Code editor
    code_input = st.text_area(
        "Write your Python code here:",
        value=st.session_state.current_code,
        height=300,
        key="code_editor",
        placeholder="# Write your solution here\ndef fizzbuzz():\n    # Your code\n    pass"
    )
    st.session_state.current_code = code_input
    
    # Buttons
    col_run, col_submit = st.columns(2)
    with col_run:
        run_btn = st.button("▶️ Run Code", key="run_btn")
    with col_submit:
        submit_btn = st.button("📤 Submit for Review", key="submit_btn", type="primary")
    
    if run_btn and code_input:
        executor = SafeCodeExecutor()
        result = executor.execute(code_input)
        
        st.markdown("**Output:**")
        if result["success"]:
            st.success("✅ Code executed successfully!")
            if result["output"]:
                st.code(result["output"], language="text")
            else:
                st.info("No output produced")
        else:
            st.error(f"❌ Error: {result['error']}")
    
    if submit_btn and code_input:
        # Update orchestrator context
        st.session_state.orchestrator.context.current_problem = st.session_state.current_problem
        
        # Process with orchestrator
        with st.spinner("🤖 Reviewing your code..."):
            response = st.session_state.orchestrator.process_student_input(
                student_message="Please review my code",
                code_attempt=code_input
            )
        
        # Add to messages
        st.session_state.messages.append({
            "agent": "student",
            "content": "Here's my code submission"
        })
        st.session_state.messages.append({
            "agent": response["agent_used"],
            "content": response["response"]
        })
        
        # Save to history
        st.session_state.code_history.append({
            "attempt": len(st.session_state.code_history) + 1,
            "code": code_input,
            "agent_feedback": response["agent_used"]
        })
        
        # Update attempt counter
        st.session_state.attempt_count = len(st.session_state.code_history)
        
        # Update concepts learned
        if "metadata" in response and "concept" in response.get("metadata", {}):
            concept = response["metadata"]["concept"]
            st.session_state.concepts_learned.add(concept)
        
        st.rerun()
    
    # Code history
    if st.session_state.code_history:
        st.markdown("---")
        st.caption("📜 Code History")
        for entry in reversed(st.session_state.code_history[-3:]):
            with st.expander(f"Attempt {entry['attempt']} • Feedback by: {entry['agent_feedback']}"):
                st.code(entry['code'], language="python")

# Sidebar: Learning Progress
with st.sidebar:
    st.header("📊 Your Learning Journey")
    
    # Stats
    attempt_count = len(st.session_state.code_history)
    concepts = st.session_state.orchestrator.context.concepts_covered
    
    # Metrics
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("Attempts", attempt_count)
    with col_m2:
        st.metric("Concepts", len(concepts))
    
    # Progress bar
    if attempt_count > 0:
        progress = min(attempt_count / 10 * 100, 100)
        st.progress(progress / 100)
        st.caption(f"{progress:.0f}% toward mastery")
    
    # Concepts learned
    if concepts:
        st.markdown("### 🎯 Concepts Learned")
        for concept in concepts:
            st.markdown(f'<span class="concept-badge">{concept}</span>', unsafe_allow_html=True)
    else:
        st.info("💡 Concepts will appear here as you learn")
    
    # Agent activity
    st.markdown("---")
    st.markdown("### 🤖 Agent Activity")
    
    agent_counts = {}
    for msg in st.session_state.messages:
        agent = msg.get("agent", "student")
        if agent != "student":
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    if agent_counts:
        # Create bar chart with dark mode compatible styling
        fig = px.bar(
            x=list(agent_counts.keys()),
            y=list(agent_counts.values()),
            labels={"x": "Agent", "y": "Count"},
            color=list(agent_counts.keys()),
            color_discrete_map={
                "socratic": "#FF6B6B",
                "hint": "#4ECDC4",
                "reviewer": "#FFD93D",
                "explainer": "#95E1D3"
            }
        )
        fig.update_layout(
            showlegend=False, 
            height=180,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#E0E0E0', size=10), showgrid=False),
            yaxis=dict(tickfont=dict(color='#E0E0E0', size=10), showgrid=False),
            bargap=0.3
        )
        fig.update_traces(textposition='outside', textfont=dict(color='#E0E0E0', size=10))
        st.plotly_chart(fig, key="agent_chart")
    
    # Learning tips
    st.markdown("---")
    st.markdown("### 💡 Learning Tips")
    st.info("""
**Getting the most from CodeMentor AI:**
- Try solving before asking
- Read error messages carefully
- Test your code frequently
- Ask specific questions
- Don't give up after one attempt!
    """)
    
    # Learning Journey Visualization
    st.markdown("---")
    st.markdown("### 🗺️ Learning Journey")
    if attempt_count > 0:
        journey_fig = create_learning_journey_graph(
            st.session_state.orchestrator.context.session_history,
            concepts
        )
        st.plotly_chart(journey_fig, key="journey_chart")
        
        # Concept Mastery
        if concepts:
            st.markdown("### 📈 Concept Mastery")
            mastery_fig = create_concept_mastery_chart(concepts, attempt_count)
            st.plotly_chart(mastery_fig, key="mastery_chart")
    else:
        st.info("Start coding to see your learning journey map!")

# Footer
st.markdown("---")
st.caption("🎓 CodeMentor AI | Built with Google Gemini | Capstone Project 2025")
