"""
Result display components for EduPulse application.
"""

import streamlit as st
from typing import Dict, Any
from utils.helpers import format_percentage, get_progress_color
from utils.calculations import generate_score_breakdown


def render_prediction_results(prediction: Dict) -> None:
    """
    Render main prediction results.
    
    Args:
        prediction: Prediction result dictionary
    """
    success_prob = prediction['success_probability']
    risk_assessment = prediction['risk_assessment']
    top_factors = prediction['top_factors']
    
    # Header with success probability
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {risk_assessment["color"]}20 0%, {risk_assessment["color"]}40 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
        <h1 style='text-align: center; color: {risk_assessment["color"]}; margin-bottom: 0.5rem;'>
            {format_percentage(success_prob)} Success Probability
        </h1>
        <h3 style='text-align: center; color: #333;'>
            {risk_assessment["label"]} - {risk_assessment["description"]}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_success_probability_card(success_prob)
    
    with col2:
        render_risk_level_card(risk_assessment)
    
    with col3:
        render_top_factor_card(top_factors)
    
    # Progress bar for success probability
    st.markdown("### 📈 Success Probability")
    render_success_progress(success_prob)
    
    # Score breakdown by category
    st.markdown("### 📊 Category Breakdown")
    render_category_breakdown(prediction['factor_scores'])
    
    # Top influencing factors
    st.markdown("### 🎯 Top Influencing Factors")
    render_top_factors(top_factors)


def render_success_probability_card(success_prob: float) -> None:
    """
    Render success probability metric card.
    
    Args:
        success_prob: Success probability (0-1)
    """
    color = get_progress_color(success_prob * 100)
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <div style='color: #666; font-size: 0.9rem;'>Success Probability</div>
        <div style='color: {color}; font-size: 2rem; font-weight: bold;'>{format_percentage(success_prob)}</div>
        <div style='color: #999; font-size: 0.8rem; margin-top: 0.5rem;'>0% to 100% scale</div>
    </div>
    """, unsafe_allow_html=True)


def render_risk_level_card(risk_assessment: Dict) -> None:
    """
    Render risk level metric card.
    
    Args:
        risk_assessment: Risk assessment dictionary
    """
    st.markdown(f"""
    <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <div style='color: #666; font-size: 0.9rem;'>Risk Level</div>
        <div style='color: {risk_assessment["color"]}; font-size: 1.5rem; font-weight: bold;'>
            {risk_assessment["label"]}
        </div>
        <div style='color: #999; font-size: 0.8rem; margin-top: 0.5rem;'>
            {risk_assessment["description"]}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_top_factor_card(top_factors: list) -> None:
    """
    Render top influencing factors card.
    
    Args:
        top_factors: List of top factors
    """
    if top_factors:
        top_factor = top_factors[0][0].replace('_', ' ').title()
        top_impact = f"{top_factors[0][2]*100:.1f}%"
        
        st.markdown(f"""
        <div style='background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='color: #666; font-size: 0.9rem;'>Top Influencer</div>
            <div style='color: #4A90E2; font-size: 1.2rem; font-weight: bold;'>{top_factor}</div>
            <div style='color: #999; font-size: 0.8rem; margin-top: 0.5rem;'>
                Impact: {top_impact} of total score
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_success_progress(success_prob: float) -> None:
    """
    Render success probability progress bar with thresholds.
    
    Args:
        success_prob: Success probability (0-1)
    """
    from config import THRESHOLDS
    
    # Create progress bar
    progress_html = f"""
    <div style='width: 100%; background: #f0f0f0; border-radius: 10px; height: 30px; position: relative; margin: 1rem 0;'>
        <div style='width: {success_prob * 100}%; background: {get_progress_color(success_prob * 100)}; 
                    height: 100%; border-radius: 10px; transition: width 0.5s;'></div>
        <div style='position: absolute; top: 5px; left: {success_prob * 100}%; transform: translateX(-50%); 
                    color: #333; font-weight: bold;'>{format_percentage(success_prob)}</div>
    </div>
    """
    
    # Add threshold markers
    thresholds_html = "<div style='display: flex; justify-content: space-between; margin-top: 5px;'>"
    for threshold_name, threshold_value in THRESHOLDS.items():
        thresholds_html += f"""
        <div style='text-align: center; width: {threshold_value * 100}%;'>
            <div style='border-left: 2px dashed #ccc; height: 10px; margin: 0 auto;'></div>
            <div style='font-size: 0.7rem; color: #666;'>{threshold_name.replace("_", " ").title()}</div>
            <div style='font-size: 0.6rem; color: #999;'>{threshold_value*100:.0f}%</div>
        </div>
        """
    thresholds_html += "</div>"
    
    st.markdown(progress_html + thresholds_html, unsafe_allow_html=True)


def render_category_breakdown(factor_scores: Dict[str, float]) -> None:
    """
    Render score breakdown by category.
    
    Args:
        factor_scores: Dictionary of factor scores
    """
    categories = generate_score_breakdown(factor_scores)
    
    for category in categories:
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**{category['category']}**")
            st.caption(f"Factors: {', '.join(category['factors']).replace('_', ' ').title()}")
        
        with col2:
            # Progress bar for category score
            progress = category['score']
            color = get_progress_color(progress)
            st.markdown(f"""
            <div style='width: 100%; background: #f0f0f0; border-radius: 5px; height: 10px;'>
                <div style='width: {progress}%; background: {color}; height: 100%; border-radius: 5px;'></div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"{progress:.1f}/100")
        
        with col3:
            st.markdown(f"**{category['weight']:.0f}%**")
            st.caption("Weight")


def render_top_factors(top_factors: list) -> None:
    """
    Render detailed view of top influencing factors.
    
    Args:
        top_factors: List of top factors
    """
    cols = st.columns(3)
    
    for idx, (factor, score, impact) in enumerate(top_factors[:3]):
        with cols[idx]:
            factor_name = factor.replace('_', ' ').title()
            impact_percent = impact * 100
            
            st.markdown(f"""
            <div style='background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
                        border-left: 4px solid {get_progress_color(score * 100)};'>
                <div style='font-size: 1rem; font-weight: bold; color: #333;'>{idx + 1}. {factor_name}</div>
                <div style='font-size: 0.9rem; color: #666; margin: 0.5rem 0;'>Score: {score:.2f}</div>
                <div style='font-size: 0.8rem; color: #4A90E2;'>
                    Impact: {impact_percent:.1f}% of total
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_detailed_analysis(prediction: Dict) -> None:
    """
    Render detailed factor analysis and recommendations.
    
    Args:
        prediction: Prediction result dictionary
    """
    st.markdown("---")
    st.subheader("🔍 Detailed Analysis")
    
    # Factor scores table
    with st.expander("📋 All Factor Scores", expanded=True):
        render_factor_scores_table(prediction['factor_scores'])
    
    # Recommendations
    with st.expander("💡 Personalized Recommendations", expanded=True):
        render_recommendations(prediction)
    
    # Improvement simulator
    with st.expander("🎯 Improvement Simulator"):
        render_improvement_simulator(prediction)


def render_factor_scores_table(factor_scores: Dict[str, float]) -> None:
    """
    Render table of all factor scores.
    
    Args:
        factor_scores: Dictionary of factor scores
    """
    from utils.calculations import normalize_scores
    
    # Convert scores to 0-100 scale
    normalized_scores = normalize_scores(factor_scores)
    
    # Create table
    table_data = []
    for factor, score in normalized_scores.items():
        color = get_progress_color(score)
        table_data.append({
            "Factor": factor.replace('_', ' ').title(),
            "Score": f"{score:.1f}",
            "Status": "🟢 Good" if score >= 70 else "🟡 Fair" if score >= 50 else "🔴 Needs Improvement",
            "Color": color
        })
    
    # Display as metrics or table
    cols = st.columns(3)
    for idx, item in enumerate(table_data):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='padding: 0.5rem; border-left: 3px solid {item["Color"]};'>
                <div style='font-size: 0.9rem; color: #666;'>{item["Factor"]}</div>
                <div style='font-size: 1.2rem; color: #333; font-weight: bold;'>{item["Score"]}%</div>
                <div style='font-size: 0.8rem; color: {item["Color"]};'>{item["Status"]}</div>
            </div>
            """, unsafe_allow_html=True)


def render_recommendations(prediction: Dict) -> None:
    """
    Render personalized recommendations based on factor scores.
    
    Args:
        prediction: Prediction result dictionary
    """
    from config import RECOMMENDATIONS
    
    factor_scores = prediction['factor_scores']
    
    # Identify low-scoring factors
    low_factors = []
    for factor, score in factor_scores.items():
        if score < 0.5:  # Below 50%
            low_factors.append(factor)
    
    if not low_factors:
        st.success("🎉 All factors are at acceptable levels! Maintain current habits.")
        return
    
    st.info(f"**Focus Areas:** {', '.join([f.replace('_', ' ').title() for f in low_factors[:3]])}")
    
    for factor in low_factors[:3]:  # Show top 3
        factor_name = factor.replace('_', ' ').title()
        current_score = factor_scores[factor] * 100
        
        st.markdown(f"### {factor_name} ({current_score:.1f}%)")
        
        if factor in RECOMMENDATIONS:
            recommendations = RECOMMENDATIONS[factor]['low' if current_score < 50 else 'medium']
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
        else:
            st.markdown(f"1. Focus on improving {factor_name.lower()}")
            st.markdown(f"2. Set specific goals for {factor_name.lower()}")
            st.markdown(f"3. Track progress weekly")
        
        st.markdown("---")


def render_improvement_simulator(prediction: Dict) -> None:
    """
    Render improvement simulator for what-if scenarios.
    
    Args:
        prediction: Prediction result dictionary
    """
    st.markdown("Simulate the impact of improvements:")
    
    factor_scores = prediction['factor_scores']
    current_score = prediction['success_probability']
    
    # Create sliders for improvements
    improvements = {}
    cols = st.columns(3)
    
    low_factors = [f for f, s in factor_scores.items() if s < 0.7]
    
    for idx, factor in enumerate(low_factors[:3]):
        with cols[idx % 3]:
            factor_name = factor.replace('_', ' ').title()
            current = factor_scores[factor] * 100
            improvement = st.slider(
                f"{factor_name} Improvement",
                min_value=0,
                max_value=int(100 - current),
                value=10,
                help=f"Current: {current:.1f}%"
            )
            improvements[factor] = improvement / 100
    
    # Calculate new score
    if improvements:
        from utils.calculations import estimate_intervention_impact
        new_score = estimate_intervention_impact(factor_scores, improvements)
        improvement_pct = ((new_score - current_score) / current_score) * 100
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current Score", format_percentage(current_score))
        
        with col2:
            st.metric(
                "Projected Score", 
                format_percentage(new_score),
                delta=f"{improvement_pct:.1f}% improvement"
            )
        
        if new_score >= 0.85:
            st.success("🎯 With these improvements, student would reach success threshold!")
        elif new_score >= 0.7:
            st.warning("📈 Significant improvement, but still below target")