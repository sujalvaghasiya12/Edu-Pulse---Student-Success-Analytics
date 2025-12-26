"""
Chart components for EduPulse application.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import pandas as pd


def create_radar_chart(factor_scores: Dict[str, float]) -> go.Figure:
    """
    Create radar chart for factor scores.
    
    Args:
        factor_scores: Dictionary of factor scores (0-1 scale)
        
    Returns:
        Plotly Figure object
    """
    from utils.calculations import normalize_scores
    
    # Normalize scores to 0-100
    normalized_scores = normalize_scores(factor_scores)
    
    # Prepare data
    categories = [key.replace('_', ' ').title() for key in normalized_scores.keys()]
    values = list(normalized_scores.values())
    
    # Close the radar chart
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(74, 144, 226, 0.3)',
        line_color='rgba(74, 144, 226, 0.8)',
        name='Current Scores'
    ))
    
    # Add target line (80%)
    fig.add_trace(go.Scatterpolar(
        r=[80] * len(categories),
        theta=categories,
        line_color='rgba(6, 214, 160, 0.5)',
        line_dash='dash',
        name='Target (80%)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                rotation=90
            )
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(l=80, r=80, t=40, b=40),
        height=500
    )
    
    return fig


def create_factor_impact_chart(top_factors: List[tuple]) -> go.Figure:
    """
    Create horizontal bar chart showing factor impacts.
    
    Args:
        top_factors: List of (factor, score, impact) tuples
        
    Returns:
        Plotly Figure object
    """
    # Prepare data
    factors = [f[0].replace('_', ' ').title() for f in top_factors]
    impacts = [f[2] * 100 for f in top_factors]  # Convert to percentage
    scores = [f[1] * 100 for f in top_factors]  # Convert to percentage
    
    # Create dataframe
    df = pd.DataFrame({
        'Factor': factors,
        'Impact (%)': impacts,
        'Score (%)': scores
    })
    
    # Sort by impact
    df = df.sort_values('Impact (%)', ascending=True)
    
    fig = px.bar(
        df,
        y='Factor',
        x='Impact (%)',
        orientation='h',
        color='Score (%)',
        color_continuous_scale='Blues',
        text='Score (%)',
        title='Top Influencing Factors'
    )
    
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        marker_line_color='rgba(0,0,0,0.2)',
        marker_line_width=1
    )
    
    fig.update_layout(
        yaxis=dict(title=''),
        xaxis=dict(title='Impact on Total Score (%)', range=[0, max(impacts) * 1.2]),
        coloraxis_colorbar=dict(title='Score (%)'),
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_category_comparison_chart(factor_scores: Dict[str, float]) -> go.Figure:
    """
    Create bar chart comparing scores across categories.
    
    Args:
        factor_scores: Dictionary of factor scores
        
    Returns:
        Plotly Figure object
    """
    from utils.calculations import generate_score_breakdown
    
    categories = generate_score_breakdown(factor_scores)
    
    # Prepare data
    category_names = [cat['category'] for cat in categories]
    category_scores = [cat['score'] for cat in categories]
    category_weights = [cat['weight'] for cat in categories]
    
    fig = go.Figure()
    
    # Add score bars
    fig.add_trace(go.Bar(
        x=category_names,
        y=category_scores,
        name='Actual Score',
        marker_color='#4A90E2',
        text=[f'{s:.1f}%' for s in category_scores],
        textposition='outside'
    ))
    
    # Add weight markers
    fig.add_trace(go.Scatter(
        x=category_names,
        y=category_weights,
        mode='markers',
        name='Weight',
        marker=dict(
            color='#FF6B6B',
            size=12,
            symbol='diamond'
        ),
        text=[f'{w:.0f}% weight' for w in category_weights]
    ))
    
    fig.update_layout(
        title='Score vs Weight by Category',
        xaxis=dict(title='Category'),
        yaxis=dict(title='Score (%)', range=[0, 100]),
        barmode='group',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        height=400,
        margin=dict(l=50, r=20, t=50, b=50)
    )
    
    return fig


def create_success_probability_gauge(success_prob: float) -> go.Figure:
    """
    Create gauge chart for success probability.
    
    Args:
        success_prob: Success probability (0-1)
        
    Returns:
        Plotly Figure object
    """
    # Convert to percentage
    value = success_prob * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Success Probability", 'font': {'size': 20}},
        delta={'reference': 70, 'increasing': {'color': "#06D6A0"}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#4A90E2"},
            'steps': [
                {'range': [0, 40], 'color': '#FF6B6B'},
                {'range': [40, 70], 'color': '#FFD166'},
                {'range': [70, 85], 'color': '#FFA726'},
                {'range': [85, 100], 'color': '#06D6A0'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig
