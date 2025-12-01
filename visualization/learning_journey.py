"""
Learning Journey Visualization
Creates interactive graphs showing student progress
"""

import plotly.graph_objects as go
import networkx as nx
from typing import List, Dict

# Theme-compatible colors (work on both light and dark backgrounds)
THEME_COLORS = {
    'background': 'rgba(0,0,0,0)',  # Transparent - adapts to theme
    'text_primary': '#E0E0E0',       # Light gray - visible on dark
    'text_secondary': '#B0B0B0',     # Medium gray
    'edge': 'rgba(150,150,150,0.6)', # Semi-transparent gray
    'attempt_node': '#4ECDC4',       # Teal
    'concept_node': '#9D7BEA',       # Purple (brighter for visibility)
    'node_border': 'rgba(255,255,255,0.8)',
    'grid': 'rgba(100,100,100,0.1)'
}


def create_learning_journey_graph(session_history: List[Dict], concepts_covered: List[str]):
    """
    Create interactive knowledge graph showing:
    - Student attempts (nodes)
    - Agent interventions (edges)
    - Concept mastery progression (colors)
    """
    
    if not session_history:
        # Return empty figure with theme-compatible styling
        fig = go.Figure()
        fig.add_annotation(
            text="Start coding to see your learning journey!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=THEME_COLORS['text_secondary'])
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['background'],
            height=300,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        return fig
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes for each attempt
    attempt_count = len(session_history)
    for i in range(attempt_count):
        G.add_node(f"Attempt {i+1}", 
                   type="attempt",
                   index=i)
    
    # Add nodes for concepts
    for concept in concepts_covered:
        G.add_node(concept, type="concept")
    
    # Add edges between attempts
    for i in range(attempt_count - 1):
        G.add_edge(f"Attempt {i+1}", f"Attempt {i+2}")
    
    # Link concepts to attempts where they were learned
    for i, concept in enumerate(concepts_covered):
        attempt_num = min(i + 2, attempt_count)
        if attempt_num > 0:
            G.add_edge(concept, f"Attempt {attempt_num}")
    
    # Create layout with fixed seed for consistency
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Separate node types
    attempt_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'attempt']
    concept_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'concept']
    
    # Create edge traces with theme-compatible colors
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_traces.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=2, color=THEME_COLORS['edge']),
                hoverinfo='none',
                showlegend=False
            )
        )
    
    # Attempt nodes trace with theme-compatible styling
    attempt_x = [pos[n][0] for n in attempt_nodes]
    attempt_y = [pos[n][1] for n in attempt_nodes]
    attempt_trace = go.Scatter(
        x=attempt_x, y=attempt_y,
        mode='markers+text',
        marker=dict(
            size=35, 
            color=THEME_COLORS['attempt_node'],
            line=dict(width=2, color=THEME_COLORS['node_border'])
        ),
        text=[f"#{i+1}" for i in range(len(attempt_nodes))],
        textposition="middle center",
        textfont=dict(size=11, color='white', family='Arial Black'),
        name="Attempts",
        hovertemplate='<b>Attempt %{text}</b><extra></extra>'
    )
    
    # Concept nodes trace with theme-compatible styling
    concept_x = [pos[n][0] for n in concept_nodes]
    concept_y = [pos[n][1] for n in concept_nodes]
    concept_trace = go.Scatter(
        x=concept_x, y=concept_y,
        mode='markers+text',
        marker=dict(
            size=45, 
            color=THEME_COLORS['concept_node'],
            line=dict(width=2, color=THEME_COLORS['node_border']),
            symbol='star'
        ),
        text=concept_nodes,
        textposition="bottom center",
        textfont=dict(size=11, color=THEME_COLORS['text_primary'], family='Arial'),
        name="Concepts",
        hovertemplate='<b>Concept: %{text}</b><extra></extra>'
    )
    
    # Create figure with theme-compatible layout
    fig = go.Figure(
        data=edge_traces + [attempt_trace, concept_trace],
        layout=go.Layout(
            showlegend=False,  # Cleaner look for sidebar
            hovermode='closest',
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['background'],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
            height=280,
            margin=dict(l=5, r=5, t=5, b=5),
            dragmode=False  # Disable drag for cleaner UX
        )
    )
    
    return fig


def create_concept_mastery_chart(concepts: List[str], attempt_count: int):
    """
    Create horizontal bar chart showing concept mastery levels
    """
    if not concepts:
        fig = go.Figure()
        fig.add_annotation(
            text="Concepts will appear here as you learn",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color=THEME_COLORS['text_secondary'])
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['background'],
            height=150,
            margin=dict(l=5, r=5, t=5, b=5)
        )
        return fig
    
    # Calculate mock mastery levels (would be real in production)
    mastery_levels = {}
    for i, concept in enumerate(concepts):
        # Simulate increasing mastery with attempts
        base_mastery = 30
        progress = min(70, attempt_count * 15)
        mastery_levels[concept] = base_mastery + progress
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(mastery_levels.values()),
            y=list(mastery_levels.keys()),
            orientation='h',
            marker=dict(
                color=list(mastery_levels.values()),
                colorscale='Viridis',
                line=dict(width=1, color='rgba(255,255,255,0.3)')
            ),
            text=[f"{v}%" for v in mastery_levels.values()],
            textposition='inside',
            textfont=dict(color='white', size=12),
            hovertemplate='<b>%{y}</b><br>Mastery: %{x}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        xaxis=dict(
            range=[0, 100], 
            showgrid=False,
            showticklabels=False,
            fixedrange=True
        ),
        yaxis=dict(
            tickfont=dict(color=THEME_COLORS['text_primary'], size=11),
            fixedrange=True
        ),
        height=max(len(concepts) * 40 + 40, 100),
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor=THEME_COLORS['background'],
        paper_bgcolor=THEME_COLORS['background'],
        bargap=0.3
    )
    
    return fig
