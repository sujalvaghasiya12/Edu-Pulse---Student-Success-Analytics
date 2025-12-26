"""
General helper functions for EduPulse application.
"""

import streamlit as st
from typing import Any, Dict, List
import time
import json


def initialize_session_state():
    """
    Initialize or reset session state variables.
    """
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    if 'current_prediction' not in st.session_state:
        st.session_state.current_prediction = None
    
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False


def format_percentage(value: float) -> str:
    """
    Format float as percentage string.
    
    Args:
        value: Float between 0 and 1
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.1f}%"


def format_time_seconds(seconds: int) -> str:
    """
    Format seconds into human-readable time.
    
    Args:
        seconds: Number of seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


def get_progress_color(percentage: float) -> str:
    """
    Get color for progress bars based on percentage.
    
    Args:
        percentage: Value between 0 and 100
        
    Returns:
        CSS color string
    """
    if percentage >= 85:
        return "#06D6A0"  # Green
    elif percentage >= 70:
        return "#FFD166"  # Yellow
    elif percentage >= 50:
        return "#FFA726"  # Orange
    else:
        return "#FF6B6B"  # Red


def create_metric_card(title: str, value: Any, delta: str = None, 
                      help_text: str = None) -> None:
    """
    Create a styled metric card.
    
    Args:
        title: Card title
        value: Main value
        delta: Delta value (change)
        help_text: Help text for tooltip
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**{title}**")
        if help_text:
            st.caption(help_text)
    
    with col2:
        if delta:
            st.metric(label="", value=value, delta=delta)
        else:
            st.metric(label="", value=value)


def save_prediction_to_history(prediction: Dict):
    """
    Save current prediction to history.
    
    Args:
        prediction: Prediction result dictionary
    """
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    
    # Add timestamp
    prediction_with_time = prediction.copy()
    prediction_with_time['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    prediction_with_time['id'] = len(st.session_state.prediction_history)
    
    # Keep only last 10 predictions
    st.session_state.prediction_history.append(prediction_with_time)
    if len(st.session_state.prediction_history) > 10:
        st.session_state.prediction_history = st.session_state.prediction_history[-10:]


def export_prediction_data(prediction: Dict, format: str = 'json') -> str:
    """
    Export prediction data in specified format.
    
    Args:
        prediction: Prediction result dictionary
        format: Export format ('json' or 'csv')
        
    Returns:
        Formatted string of data
    """
    if format == 'json':
        return json.dumps(prediction, indent=2)
    elif format == 'csv':
        # Simple CSV format for key metrics
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Metric', 'Value'])
        
        # Write data
        writer.writerow(['Success Probability', prediction['success_probability']])
        writer.writerow(['Risk Level', prediction['risk_assessment']['label']])
        
        for factor, score in prediction['factor_scores'].items():
            writer.writerow([factor.title(), score])
        
        return output.getvalue()
    
    return ""


def load_custom_css():
    """
    Load custom CSS styles.
    """
    try:
        with open('assets/styles.css', 'r') as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Default styles if CSS file not found
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .risk-high { color: #FF6B6B; font-weight: bold; }
        .risk-medium { color: #FFD166; font-weight: bold; }
        .risk-low { color: #06D6A0; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)