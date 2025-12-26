"""
Input validation utilities for EduPulse application.
"""
from typing import List  # Add this line
from typing import Dict, Tuple, Optional, List  # Added List import here
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import StudentProfile
except ImportError:
    # Fallback if config import fails
    from dataclasses import dataclass
    
    @dataclass
    class StudentProfile:
        """Fallback StudentProfile class if config import fails"""
        attendance: float
        study_hours: float
        sleep_hours: float
        family_support: str
        extracurricular: str
        previous_grades: str
        financial_status: str
        mental_health: str
        peer_influence: str


def validate_student_inputs(**kwargs) -> Tuple[bool, Optional[str]]:
    """
    Validate all student input values.
    
    Args:
        **kwargs: Input parameters
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check required fields
    required_fields = [
        'attendance', 'study_hours', 'sleep_hours',
        'family_support', 'extracurricular', 'previous_grades',
        'financial_status', 'mental_health', 'peer_influence'
    ]
    
    for field in required_fields:
        if field not in kwargs:
            return False, f"Missing required field: {field}"
    
    # Validate numerical ranges
    if not (0 <= kwargs['attendance'] <= 100):
        return False, "Attendance must be between 0 and 100%"
    
    if not (0 <= kwargs['study_hours'] <= 24):
        return False, "Study hours must be between 0 and 24"
    
    if not (0 <= kwargs['sleep_hours'] <= 24):
        return False, "Sleep hours must be between 0 and 24"
    
    # Validate categorical values
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


def create_student_profile(**kwargs) -> Tuple[Optional[StudentProfile], Optional[str]]:
    """
    Create StudentProfile object with validation.
    
    Args:
        **kwargs: Input parameters
        
    Returns:
        Tuple of (profile, error_message)
    """
    is_valid, error_message = validate_student_inputs(**kwargs)
    
    if not is_valid:
        return None, error_message
    
    try:
        profile = StudentProfile(**kwargs)
        return profile, None
    except Exception as e:
        return None, f"Error creating profile: {str(e)}"


def sanitize_inputs(inputs: Dict) -> Dict:
    """
    Sanitize and normalize input values.
    
    Args:
        inputs: Raw input dictionary
        
    Returns:
        Sanitized input dictionary
    """
    sanitized = inputs.copy()
    
    # Round numerical values
    for field in ['attendance', 'study_hours', 'sleep_hours']:
        if field in sanitized:
            sanitized[field] = round(float(sanitized[field]), 1)
    
    # Capitalize categorical values
    for field in ['family_support', 'extracurricular', 'previous_grades',
                  'financial_status', 'mental_health', 'peer_influence']:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitized[field].strip().title()
    
    return sanitized


def check_for_anomalies(profile: StudentProfile) -> List[str]:
    """
    Check for unusual or concerning input patterns.
    
    Args:
        profile: StudentProfile object
        
    Returns:
        List of anomaly warnings
    """
    warnings = []
    
    # Check for concerning values
    if profile.attendance < 70:
        warnings.append(f"⚠️ Low attendance ({profile.attendance}%) - Consider intervention")
    
    if profile.study_hours < 2:
        warnings.append(f"⚠️ Very low study hours ({profile.study_hours} hrs/day)")
    elif profile.study_hours > 10:
        warnings.append(f"⚠️ Very high study hours ({profile.study_hours} hrs/day) - Risk of burnout")
    
    if profile.sleep_hours < 6:
        warnings.append(f"⚠️ Insufficient sleep ({profile.sleep_hours} hrs/night)")
    elif profile.sleep_hours > 12:
        warnings.append(f"⚠️ Excessive sleep ({profile.sleep_hours} hrs/night)")
    
    if profile.mental_health in ['Poor', 'Fair']:
        warnings.append("⚠️ Mental health concerns detected")
    
    if profile.financial_status == 'Struggling':
        warnings.append("⚠️ Financial struggles may impact academic performance")
    
    return warnings