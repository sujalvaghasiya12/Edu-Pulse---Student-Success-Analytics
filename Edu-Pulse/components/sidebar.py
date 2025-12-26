"""
Sidebar component for EduPulse application.
"""

import streamlit as st
from typing import Dict, Any
from utils.helpers import format_percentage


def render_sidebar(prediction: Dict = None) -> Dict[str, Any]:
    """
    Render the application sidebar with controls and info.
    
    Args:
        prediction: Current prediction results (optional)
        
    Returns:
        Dictionary with sidebar state
    """
    with st.sidebar:
        # App Logo and Title
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #4A90E2; margin-bottom: 0;'>🎓</h1>
            <h3 style='color: #333; margin-top: 0;'>EduPulse</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # App Description
        st.markdown("""
        **Student Success Analytics Platform**
        
        Predict academic success risk factors and get personalized recommendations.
        """)
        
        st.markdown("---")
        
        # Quick Stats Section
        if prediction:
            st.subheader("📊 Current Prediction")
            
            success_prob = prediction['success_probability']
            risk_level = prediction['risk_assessment']['label']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Success Probability", format_percentage(success_prob))
            with col2:
                st.metric("Risk Level", risk_level.split()[-1])
        
        # Settings Section
        st.markdown("---")
        st.subheader("⚙️ Settings")
        
        # Display options
        show_details = st.checkbox(
            "Show Detailed Analysis",
            value=st.session_state.get('show_details', False),
            help="Show detailed factor analysis and recommendations"
        )
        
        # Update session state
        st.session_state.show_details = show_details
        
        # Model Settings (for future ML integration)
        st.markdown("#### Model Settings")
        use_advanced_model = st.checkbox(
            "Use Advanced Model",
            value=False,
            help="Enable when ML model is integrated",
            disabled=True  # Currently disabled
        )
        
        # Export Options
        st.markdown("---")
        st.subheader("📤 Export")
        
        if prediction:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Export as JSON"):
                    from utils.helpers import export_prediction_data
                    data = export_prediction_data(prediction, 'json')
                    st.download_button(
                        label="Download JSON",
                        data=data,
                        file_name="edupulse_prediction.json",
                        mime="application/json"
                    )
            
            with col2:
                if st.button("Export as CSV"):
                    from utils.helpers import export_prediction_data
                    data = export_prediction_data(prediction, 'csv')
                    st.download_button(
                        label="Download CSV",
                        data=data,
                        file_name="edupulse_prediction.csv",
                        mime="text/csv"
                    )
        
        # About Section
        st.markdown("---")
        with st.expander("ℹ️ About EduPulse"):
            st.markdown("""
            **Version:** 2.0.0  
            **Last Updated:** December 2024  
            
            This application uses predictive analytics to identify
            students at risk of academic challenges.
            
            ### How it works:
            1. Input student profile data
            2. System calculates success probability
            3. Get personalized recommendations
            4. Monitor improvements over time
            
            ### Technology Stack:
            - Streamlit for UI
            - Rule-based prediction engine
            - Plotly for visualizations
            - Modular architecture
            
            *Note: Currently uses rule-based scoring.
            ML model integration is planned for v3.0.*
            """)
    
    return {
        'show_details': show_details,
        'use_advanced_model': use_advanced_model
    }