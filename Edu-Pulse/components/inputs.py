"""
Input components for EduPulse application.
"""

import streamlit as st
from typing import Dict, Any, Tuple
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import StudentProfile
    from utils.validators import sanitize_inputs, check_for_anomalies
except ImportError:
    # Define fallbacks if imports fail
    from dataclasses import dataclass
    
    @dataclass
    class StudentProfile:
        """Fallback StudentProfile class"""
        attendance: float
        study_hours: float
        sleep_hours: float
        family_support: str
        extracurricular: str
        previous_grades: str
        financial_status: str
        mental_health: str
        peer_influence: str
    
    def sanitize_inputs(inputs: Dict) -> Dict:
        """Fallback sanitize function"""
        return inputs.copy()
    
    def check_for_anomalies(profile: StudentProfile) -> list:
        """Fallback anomaly check"""
        return []


def render_student_inputs() -> Tuple[Dict[str, Any], Any]:
    """
    Render all student input fields in tabs.
    
    Returns:
        Tuple of (raw_inputs, student_profile)
    """
    raw_inputs = {}
    
    # Create tabs for different input categories
    tab1, tab2, tab3 = st.tabs(["📚 Academic", "💪 Wellness", "👥 Support"])
    
    with tab1:
        raw_inputs.update(render_academic_inputs())
    
    with tab2:
        raw_inputs.update(render_wellness_inputs())
    
    with tab3:
        raw_inputs.update(render_support_inputs())
    
    # Sanitize inputs
    sanitized_inputs = sanitize_inputs(raw_inputs)
    
    # Create profile
    from utils.validators import create_student_profile
    profile, error = create_student_profile(**sanitized_inputs)
    
    if error:
        st.error(f"Input Error: {error}")
        return None, None
    
    return sanitized_inputs, profile


def render_academic_inputs() -> Dict[str, Any]:
    """
    Render academic-related input fields.
    
    Returns:
        Dictionary of academic inputs
    """
    inputs = {}
    
    st.markdown("### Academic Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        inputs['attendance'] = st.slider(
            "Attendance Rate (%)",
            min_value=0,
            max_value=100,
            value=85,
            help="Percentage of classes attended"
        )
        
        inputs['study_hours'] = st.slider(
            "Daily Study Hours",
            min_value=0.0,
            max_value=12.0,
            value=3.0,
            step=0.5,
            help="Average hours spent studying per day"
        )
    
    with col2:
        inputs['previous_grades'] = st.selectbox(
            "Previous Academic Performance",
            options=['Poor', 'Average', 'Good', 'Excellent'],
            index=2,
            help="Overall academic performance in previous terms"
        )
        
        # Display visual feedback
        st.markdown("---")
        if inputs['attendance'] < 75:
            st.warning(f"⚠️ Attendance ({inputs['attendance']}%) is below recommended level (75%+)")
        if inputs['study_hours'] < 2:
            st.warning(f"⚠️ Study hours ({inputs['study_hours']}) may be insufficient")
    
    return inputs


def render_wellness_inputs() -> Dict[str, Any]:
    """
    Render wellness-related input fields.
    
    Returns:
        Dictionary of wellness inputs
    """
    inputs = {}
    
    st.markdown("### Health & Wellness")
    
    col1, col2 = st.columns(2)
    
    with col1:
        inputs['sleep_hours'] = st.slider(
            "Sleep Hours per Night",
            min_value=0.0,
            max_value=12.0,
            value=7.0,
            step=0.5,
            help="Average hours of sleep per night"
        )
        
        inputs['mental_health'] = st.selectbox(
            "Mental Health Status",
            options=['Poor', 'Fair', 'Good', 'Excellent'],
            index=2,
            help="Self-reported mental well-being"
        )
    
    with col2:
        inputs['extracurricular'] = st.selectbox(
            "Extracurricular Involvement",
            options=['None', 'Moderate', 'High'],
            index=1,
            help="Level of participation in extracurricular activities"
        )
        
        # Display visual feedback
        st.markdown("---")
        if inputs['sleep_hours'] < 6:
            st.warning(f"⚠️ Sleep ({inputs['sleep_hours']} hrs) is below recommended 7-9 hours")
        if inputs['mental_health'] in ['Poor', 'Fair']:
            st.warning(f"⚠️ Mental health ({inputs['mental_health']}) may need attention")
    
    return inputs


def render_support_inputs() -> Dict[str, Any]:
    """
    Render support system input fields.
    
    Returns:
        Dictionary of support inputs
    """
    inputs = {}
    
    st.markdown("### Support Systems")
    
    col1, col2 = st.columns(2)
    
    with col1:
        inputs['family_support'] = st.selectbox(
            "Family Support",
            options=['Low', 'Medium', 'High'],
            index=2,
            help="Level of support from family"
        )
        
        inputs['financial_status'] = st.selectbox(
            "Financial Status",
            options=['Struggling', 'Stable', 'Comfortable'],
            index=1,
            help="Current financial situation"
        )
    
    with col2:
        inputs['peer_influence'] = st.selectbox(
            "Peer Influence",
            options=['Negative', 'Neutral', 'Positive'],
            index=2,
            help="Influence of peers on academic behavior"
        )
        
        # Display visual feedback
        st.markdown("---")
        if inputs['family_support'] == 'Low':
            st.warning("⚠️ Low family support may impact academic success")
        if inputs['financial_status'] == 'Struggling':
            st.warning("⚠️ Financial struggles may create additional stress")
        if inputs['peer_influence'] == 'Negative':
            st.warning("⚠️ Negative peer influence may affect motivation")
    
    return inputs


def render_prediction_button(profile) -> bool:
    """
    Render the prediction button with validation.
    
    Args:
        profile: StudentProfile object or None
        
    Returns:
        True if prediction button was clicked
    """
    st.markdown("---")
    
    # Check for anomalies if profile exists
    if profile:
        try:
            anomalies = check_for_anomalies(profile)
            if anomalies:
                with st.expander("⚠️ Anomaly Detected", expanded=True):
                    for anomaly in anomalies:
                        st.write(anomaly)
        except:
            pass  # Skip if check fails
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_clicked = st.button(
            "🚀 Predict Success Probability",
            type="primary",
            use_container_width=True,
            help="Click to analyze student profile and predict success"
        )
    
    if predict_clicked:
        if profile:
            st.success("✅ Profile validated successfully!")
            return True
        else:
            st.error("❌ Please fill in all required fields correctly")
    
    return False