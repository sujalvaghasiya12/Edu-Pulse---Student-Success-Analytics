"""
Configuration file for EduPulse application.
Contains constants, mappings, and scoring weights.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

# ============================================================================
# STUDENT PROFILE CONFIGURATION
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
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary for easy processing."""
        return {
            'attendance': self.attendance,
            'study_hours': self.study_hours,
            'sleep_hours': self.sleep_hours,
            'family_support': self.family_support,
            'extracurricular': self.extracurricular,
            'previous_grades': self.previous_grades,
            'financial_status': self.financial_status,
            'mental_health': self.mental_health,
            'peer_influence': self.peer_influence
        }

# ============================================================================
# SCORING WEIGHTS (Rules for Success Prediction)
# ============================================================================

WEIGHTS = {
    'academic_factors': {
        'attendance': 0.25,
        'study_hours': 0.20,
        'previous_grades': 0.15,
    },
    'wellness_factors': {
        'sleep_hours': 0.15,
        'mental_health': 0.10,
        'extracurricular': 0.05,
    },
    'support_factors': {
        'family_support': 0.05,
        'financial_status': 0.03,
        'peer_influence': 0.02,
    }
}

# ============================================================================
# CATEGORICAL MAPPINGS
# ============================================================================

SCORE_MAPPINGS = {
    'family_support': {'Low': 0.3, 'Medium': 0.7, 'High': 1.0},
    'extracurricular': {'None': 0.3, 'Moderate': 0.7, 'High': 1.0},
    'previous_grades': {'Poor': 0.2, 'Average': 0.5, 'Good': 0.8, 'Excellent': 1.0},
    'financial_status': {'Struggling': 0.3, 'Stable': 0.7, 'Comfortable': 1.0},
    'mental_health': {'Poor': 0.2, 'Fair': 0.5, 'Good': 0.8, 'Excellent': 1.0},
    'peer_influence': {'Negative': 0.2, 'Neutral': 0.5, 'Positive': 1.0}
}

# ============================================================================
# THRESHOLDS AND BOUNDARIES
# ============================================================================

THRESHOLDS = {
    'HIGH_RISK': 0.4,
    'MODERATE_RISK': 0.7,
    'SUCCESS': 0.85
}

RISK_LEVELS = {
    'HIGH_RISK': {
        'min': 0.0,
        'max': 0.4,
        'label': '🟥 High Risk',
        'color': '#FF6B6B',
        'description': 'Needs immediate intervention'
    },
    'MODERATE_RISK': {
        'min': 0.4,
        'max': 0.7,
        'label': '🟨 Moderate Risk',
        'color': '#FFD166',
        'description': 'Requires monitoring and support'
    },
    'AT_RISK': {
        'min': 0.7,
        'max': 0.85,
        'label': '🟧 At Risk',
        'color': '#FFA726',
        'description': 'Below target, needs improvement'
    },
    'SUCCESS': {
        'min': 0.85,
        'max': 1.0,
        'label': '🟩 Success',
        'color': '#06D6A0',
        'description': 'On track for academic success'
    }
}

# ============================================================================
# RECOMMENDATIONS DATABASE
# ============================================================================

RECOMMENDATIONS = {
    'attendance': {
        'low': [
            "Implement daily attendance tracking",
            "Schedule regular check-ins with advisor",
            "Consider flexible attendance options"
        ],
        'medium': [
            "Maintain current attendance rate",
            "Set goal for 5% improvement",
            "Join study groups for accountability"
        ]
    },
    'study_hours': {
        'low': [
            "Create structured study schedule",
            "Use Pomodoro technique (25 min focus, 5 min break)",
            "Attend study skills workshop"
        ],
        'medium': [
            "Optimize study environment",
            "Incorporate active recall techniques",
            "Join peer study sessions"
        ]
    },
    'sleep_hours': {
        'low': [
            "Establish consistent sleep schedule",
            "Avoid screens 1 hour before bed",
            "Create relaxing bedtime routine"
        ]
    }
}

# ============================================================================
# UI CONSTANTS
# ============================================================================

APP_TITLE = "🎓 EduPulse - Student Success Analytics"
APP_DESCRIPTION = """
AI-powered predictive analytics for identifying at-risk students 
and recommending personalized interventions.
"""

COLORS = {
    'primary': '#4A90E2',
    'success': '#06D6A0',
    'warning': '#FFD166',
    'danger': '#FF6B6B',
    'info': '#118AB2',
    'light': '#F8F9FA',
    'dark': '#212529'
}