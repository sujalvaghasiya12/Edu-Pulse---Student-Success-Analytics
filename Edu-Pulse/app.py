"""
EduPulse - Student Success Analytics Dashboard
Simplified version to avoid import issues
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json

# ============================================================================
# DATA CLASSES AND CONFIGURATION
# ============================================================================

@dataclass
class StudentProfile:
    """Data class representing a student's profile for prediction."""
    attendance: float  # 0-100%
    study_hours: float  # hours per day
    sleep_hours: float  # hours per night
    family_support: str  # Low, Medium, High
    extracurricular: str  # None, Moderate, High
    previous_grades: str  # Poor, Average, Good, Excellent
    financial_status: str  # Struggling, Stable, Comfortable
    mental_health: str  # Poor, Fair, Good, Excellent
    peer_influence: str  # Negative, Neutral, Positive

# Configuration
SCORE_MAPPINGS = {
    'family_support': {'Low': 0.3, 'Medium': 0.7, 'High': 1.0},
    'extracurricular': {'None': 0.3, 'Moderate': 0.7, 'High': 1.0},
    'previous_grades': {'Poor': 0.2, 'Average': 0.5, 'Good': 0.8, 'Excellent': 1.0},
    'financial_status': {'Struggling': 0.3, 'Stable': 0.7, 'Comfortable': 1.0},
    'mental_health': {'Poor': 0.2, 'Fair': 0.5, 'Good': 0.8, 'Excellent': 1.0},
    'peer_influence': {'Negative': 0.2, 'Neutral': 0.5, 'Positive': 1.0}
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def initialize_session_state():
    """Initialize or reset session state variables."""
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    if 'current_prediction' not in st.session_state:
        st.session_state.current_prediction = None
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False

def validate_student_inputs(**kwargs) -> Tuple[bool, Optional[str]]:
    """Validate all student input values."""
    required_fields = [
        'attendance', 'study_hours', 'sleep_hours',
        'family_support', 'extracurricular', 'previous_grades',
        'financial_status', 'mental_health', 'peer_influence'
    ]
    
    for field in required_fields:
        if field not in kwargs:
            return False, f"Missing required field: {field}"
    
    if not (0 <= kwargs['attendance'] <= 100):
        return False, "Attendance must be between 0 and 100%"
    
    if not (0 <= kwargs['study_hours'] <= 24):
        return False, "Study hours must be between 0 and 24"
    
    if not (0 <= kwargs['sleep_hours'] <= 24):
        return False, "Sleep hours must be between 0 and 24"
    
    valid_values = {
        'family_support': ['Low', 'Medium', 'High'],
        'extracurricular': ['None', 'Moderate', 'High'],
        'previous_grades': ['Poor', 'Average', 'Good', 'Excellent'],
        'financial_status': ['Struggling', 'Stable', 'Comfortable'],
        'mental_health': ['Poor', 'Fair', 'Good', 'Excellent'],
        'peer_influence': ['Negative', 'Neutral', 'Positive']
    }
    
    for field, valid_options in valid_values.items():
        if kwargs[field] not in valid_options:
            return False, f"{field.replace('_', ' ').title()} must be one of: {', '.join(valid_options)}"
    
    return True, None

# ============================================================================
# PREDICTION ENGINE
# ============================================================================

class StudentSuccessPredictor:
    """Predictive model for student success."""
    
    def __init__(self):
        self.weights = {
            'academic_factors': {'attendance': 0.25, 'study_hours': 0.20, 'previous_grades': 0.15},
            'wellness_factors': {'sleep_hours': 0.15, 'mental_health': 0.10, 'extracurricular': 0.05},
            'support_factors': {'family_support': 0.05, 'financial_status': 0.03, 'peer_influence': 0.02}
        }
    
    def normalize_value(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize values to 0-1 range."""
        if value <= min_val:
            return 0.0
        elif value >= max_val:
            return 1.0
        else:
            return (value - min_val) / (max_val - min_val)
    
    def calculate_factor_scores(self, profile: StudentProfile) -> Dict[str, float]:
        """Calculate normalized scores for each factor."""
        scores = {}
        
        # Academic factors
        scores['attendance'] = self.normalize_value(profile.attendance, 60, 100)
        scores['study_hours'] = self.normalize_value(profile.study_hours, 1, 8)
        
        # Wellness factors
        scores['sleep_hours'] = self.normalize_value(profile.sleep_hours, 4, 10)
        
        # Categorical factors
        scores['family_support'] = SCORE_MAPPINGS['family_support'][profile.family_support]
        scores['extracurricular'] = SCORE_MAPPINGS['extracurricular'][profile.extracurricular]
        scores['previous_grades'] = SCORE_MAPPINGS['previous_grades'][profile.previous_grades]
        scores['financial_status'] = SCORE_MAPPINGS['financial_status'][profile.financial_status]
        scores['mental_health'] = SCORE_MAPPINGS['mental_health'][profile.mental_health]
        scores['peer_influence'] = SCORE_MAPPINGS['peer_influence'][profile.peer_influence]
        
        return scores
    
    def predict(self, profile: StudentProfile) -> Dict:
        """Main prediction method."""
        factor_scores = self.calculate_factor_scores(profile)
        
        # Calculate weighted success probability
        total_score = 0.0
        total_score += factor_scores['attendance'] * self.weights['academic_factors']['attendance']
        total_score += factor_scores['study_hours'] * self.weights['academic_factors']['study_hours']
        total_score += factor_scores['previous_grades'] * self.weights['academic_factors']['previous_grades']
        total_score += factor_scores['sleep_hours'] * self.weights['wellness_factors']['sleep_hours']
        total_score += factor_scores['mental_health'] * self.weights['wellness_factors']['mental_health']
        total_score += factor_scores['extracurricular'] * self.weights['wellness_factors']['extracurricular']
        total_score += factor_scores['family_support'] * self.weights['support_factors']['family_support']
        total_score += factor_scores['financial_status'] * self.weights['support_factors']['financial_status']
        total_score += factor_scores['peer_influence'] * self.weights['support_factors']['peer_influence']
        
        success_probability = round(total_score, 4)
        
        # Determine risk level
        if success_probability >= 0.85:
            risk_level = {'label': '🟩 Success', 'color': '#06D6A0', 'description': 'On track for academic success'}
        elif success_probability >= 0.7:
            risk_level = {'label': '🟧 At Risk', 'color': '#FFA726', 'description': 'Below target, needs improvement'}
        elif success_probability >= 0.4:
            risk_level = {'label': '🟨 Moderate Risk', 'color': '#FFD166', 'description': 'Requires monitoring and support'}
        else:
            risk_level = {'label': '🟥 High Risk', 'color': '#FF6B6B', 'description': 'Needs immediate intervention'}
        
        return {
            'success_probability': success_probability,
            'risk_assessment': risk_level,
            'factor_scores': factor_scores,
            'profile': {
                'attendance': profile.attendance,
                'study_hours': profile.study_hours,
                'sleep_hours': profile.sleep_hours,
                'family_support': profile.family_support,
                'extracurricular': profile.extracurricular,
                'previous_grades': profile.previous_grades,
                'financial_status': profile.financial_status,
                'mental_health': profile.mental_health,
                'peer_influence': profile.peer_influence
            }
        }

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #4A90E2; margin-bottom: 0;'>🎓</h1>
            <h3 style='color: #333; margin-top: 0;'>EduPulse</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Student Success Analytics Platform**")
        st.markdown("Predict academic success risk factors and get personalized recommendations.")
        
        st.markdown("---")
        st.subheader("⚙️ Settings")
        show_details = st.checkbox("Show Detailed Analysis", value=st.session_state.show_details)
        st.session_state.show_details = show_details
        
        return {'show_details': show_details}

def render_student_inputs():
    """Render all student input fields."""
    inputs = {}
    
    tab1, tab2, tab3 = st.tabs(["📚 Academic", "💪 Wellness", "👥 Support"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            inputs['attendance'] = st.slider("Attendance Rate (%)", 0, 100, 85)
            inputs['study_hours'] = st.slider("Daily Study Hours", 0.0, 12.0, 3.0, 0.5)
        with col2:
            inputs['previous_grades'] = st.selectbox(
                "Previous Academic Performance",
                ['Poor', 'Average', 'Good', 'Excellent'],
                index=2
            )
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            inputs['sleep_hours'] = st.slider("Sleep Hours per Night", 0.0, 12.0, 7.0, 0.5)
            inputs['mental_health'] = st.selectbox(
                "Mental Health Status",
                ['Poor', 'Fair', 'Good', 'Excellent'],
                index=2
            )
        with col2:
            inputs['extracurricular'] = st.selectbox(
                "Extracurricular Involvement",
                ['None', 'Moderate', 'High'],
                index=1
            )
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            inputs['family_support'] = st.selectbox(
                "Family Support",
                ['Low', 'Medium', 'High'],
                index=2
            )
            inputs['financial_status'] = st.selectbox(
                "Financial Status",
                ['Struggling', 'Stable', 'Comfortable'],
                index=1
            )
        with col2:
            inputs['peer_influence'] = st.selectbox(
                "Peer Influence",
                ['Negative', 'Neutral', 'Positive'],
                index=2
            )
    
    # Create profile
    is_valid, error = validate_student_inputs(**inputs)
    if not is_valid:
        st.error(f"Input Error: {error}")
        return None, None
    
    profile = StudentProfile(**inputs)
    return inputs, profile

def render_prediction_results(prediction: Dict):
    """Render prediction results."""
    success_prob = prediction['success_probability']
    risk_assessment = prediction['risk_assessment']
    
    # Header
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {risk_assessment["color"]}20 0%, {risk_assessment["color"]}40 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='text-align: center; color: {risk_assessment["color"]}; margin-bottom: 0.5rem;'>
            {success_prob*100:.1f}% Success Probability
        </h1>
        <h3 style='text-align: center; color: #333;'>
            {risk_assessment["label"]} - {risk_assessment["description"]}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Success Probability", f"{success_prob*100:.1f}%")
    with col2:
        st.metric("Risk Level", risk_assessment['label'])
    with col3:
        st.metric("Status", risk_assessment['description'])
    
    # Factor scores
    st.markdown("### 📊 Factor Scores")
    factor_scores = prediction['factor_scores']
    for factor, score in factor_scores.items():
        score_pct = score * 100
        color = "#06D6A0" if score_pct >= 70 else "#FFD166" if score_pct >= 50 else "#FF6B6B"
        st.markdown(f"""
        <div style='margin: 0.5rem 0;'>
            <div style='display: flex; justify-content: space-between;'>
                <span>{factor.replace('_', ' ').title()}</span>
                <span>{score_pct:.1f}%</span>
            </div>
            <div style='width: 100%; background: #f0f0f0; border-radius: 5px; height: 10px;'>
                <div style='width: {score_pct}%; background: {color}; height: 100%; border-radius: 5px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application function."""
    # Page configuration
    st.set_page_config(
        page_title="EduPulse - Student Success Analytics",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style='text-align: center; margin-bottom: 0.5rem;'>🎓 EduPulse - Student Success Analytics</h1>
        <h3 style='text-align: center; font-weight: 300; opacity: 0.9;'>
            AI-powered predictive analytics for identifying at-risk students
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    sidebar_state = render_sidebar()
    
    # Main content
    main_tab1, main_tab2 = st.tabs(["📊 Predict", "📋 History"])
    
    with main_tab1:
        st.header("📝 Student Profile Input")
        
        # Render inputs
        inputs, profile = render_student_inputs()
        
        # Prediction button
        st.markdown("---")
        if st.button("🚀 Predict Success Probability", type="primary", use_container_width=True):
            if profile:
                with st.spinner("🔮 Analyzing student profile..."):
                    predictor = StudentSuccessPredictor()
                    prediction_result = predictor.predict(profile)
                    st.session_state.current_prediction = prediction_result
                    st.session_state.prediction_history.append(prediction_result)
                    st.success("✅ Prediction completed successfully!")
        
        # Show results if available
        if st.session_state.current_prediction:
            st.markdown("---")
            render_prediction_results(st.session_state.current_prediction)
    
    with main_tab2:
        st.header("📋 Prediction History")
        
        if st.session_state.prediction_history:
            for i, pred in enumerate(reversed(st.session_state.prediction_history)):
                with st.expander(f"Prediction {i+1} - Success: {pred['success_probability']*100:.1f}%"):
                    st.json(pred)
        else:
            st.info("No prediction history yet.")

# ============================================================================
# RUN THE APP
# ============================================================================

if __name__ == "__main__":
    main()