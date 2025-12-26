"""
Prediction engine for EduPulse.
Contains the core ML logic for student success prediction.
"""

import numpy as np
from typing import Dict, Tuple
from dataclasses import asdict

from config import StudentProfile, WEIGHTS, SCORE_MAPPINGS, THRESHOLDS, RISK_LEVELS


class StudentSuccessPredictor:
    """
    Predictive model for student success.
    Currently uses rule-based scoring with weights.
    
    NOTE: This can be replaced with a trained ML model.
    See `predict_with_ml_model` method for integration example.
    """
    
    def __init__(self):
        """Initialize the predictor with configuration."""
        self.weights = WEIGHTS
        self.mappings = SCORE_MAPPINGS
        
    def normalize_continuous_value(self, value: float, min_val: float, max_val: float) -> float:
        """
        Normalize continuous values to 0-1 range.
        
        Args:
            value: The value to normalize
            min_val: Minimum expected value
            max_val: Maximum expected value
            
        Returns:
            Normalized value between 0 and 1
        """
        if value <= min_val:
            return 0.0
        elif value >= max_val:
            return 1.0
        else:
            return (value - min_val) / (max_val - min_val)
    
    def calculate_factor_scores(self, profile: StudentProfile) -> Dict[str, float]:
        """
        Calculate normalized scores for each factor (0 to 1).
        
        Args:
            profile: StudentProfile object
            
        Returns:
            Dictionary of factor scores
        """
        scores = {}
        
        # Academic factors
        scores['attendance'] = self.normalize_continuous_value(
            profile.attendance, 60, 100
        )
        scores['study_hours'] = self.normalize_continuous_value(
            profile.study_hours, 1, 8
        )
        
        # Wellness factors
        scores['sleep_hours'] = self.normalize_continuous_value(
            profile.sleep_hours, 4, 10
        )
        
        # Categorical factors (using predefined mappings)
        scores['family_support'] = self.mappings['family_support'][profile.family_support]
        scores['extracurricular'] = self.mappings['extracurricular'][profile.extracurricular]
        scores['previous_grades'] = self.mappings['previous_grades'][profile.previous_grades]
        scores['financial_status'] = self.mappings['financial_status'][profile.financial_status]
        scores['mental_health'] = self.mappings['mental_health'][profile.mental_health]
        scores['peer_influence'] = self.mappings['peer_influence'][profile.peer_influence]
        
        return scores
    
    def calculate_weighted_score(self, factor_scores: Dict[str, float]) -> float:
        """
        Calculate weighted success probability.
        
        Args:
            factor_scores: Dictionary of normalized factor scores
            
        Returns:
            Weighted success probability (0 to 1)
        """
        total_score = 0.0
        
        # Academic factors (60% weight)
        total_score += factor_scores['attendance'] * self.weights['academic_factors']['attendance']
        total_score += factor_scores['study_hours'] * self.weights['academic_factors']['study_hours']
        total_score += factor_scores['previous_grades'] * self.weights['academic_factors']['previous_grades']
        
        # Wellness factors (30% weight)
        total_score += factor_scores['sleep_hours'] * self.weights['wellness_factors']['sleep_hours']
        total_score += factor_scores['mental_health'] * self.weights['wellness_factors']['mental_health']
        total_score += factor_scores['extracurricular'] * self.weights['wellness_factors']['extracurricular']
        
        # Support factors (10% weight)
        total_score += factor_scores['family_support'] * self.weights['support_factors']['family_support']
        total_score += factor_scores['financial_status'] * self.weights['support_factors']['financial_status']
        total_score += factor_scores['peer_influence'] * self.weights['support_factors']['peer_influence']
        
        return round(total_score, 4)
    
    def determine_risk_level(self, score: float) -> Dict:
        """
        Determine risk level based on success probability.
        
        Args:
            score: Success probability (0 to 1)
            
        Returns:
            Dictionary with risk level information
        """
        for level_key, level_info in RISK_LEVELS.items():
            if level_info['min'] <= score < level_info['max']:
                return {
                    'level': level_key,
                    'label': level_info['label'],
                    'color': level_info['color'],
                    'description': level_info['description'],
                    'score': score
                }
        
        # Default fallback
        return {
            'level': 'UNKNOWN',
            'label': '❓ Unknown',
            'color': '#6C757D',
            'description': 'Unable to determine risk level',
            'score': score
        }
    
    def predict(self, profile: StudentProfile) -> Dict:
        """
        Main prediction method.
        
        Args:
            profile: StudentProfile object
            
        Returns:
            Dictionary with prediction results
        """
        # Calculate factor scores
        factor_scores = self.calculate_factor_scores(profile)
        
        # Calculate weighted success probability
        success_probability = self.calculate_weighted_score(factor_scores)
        
        # Determine risk level
        risk_assessment = self.determine_risk_level(success_probability)
        
        # Identify top 3 influencing factors
        top_factors = self.identify_key_factors(factor_scores)
        
        return {
            'success_probability': success_probability,
            'risk_assessment': risk_assessment,
            'factor_scores': factor_scores,
            'top_factors': top_factors,
            'profile': asdict(profile)
        }
    
    def identify_key_factors(self, factor_scores: Dict[str, float]) -> list:
        """
        Identify top 3 factors influencing the score.
        
        Args:
            factor_scores: Dictionary of factor scores
            
        Returns:
            List of tuples (factor_name, score, impact)
        """
        # Calculate impact (score * weight)
        impacts = []
        for factor, score in factor_scores.items():
            # Find weight for this factor
            weight = 0
            for category in self.weights.values():
                if factor in category:
                    weight = category[factor]
                    break
            
            impact = score * weight
            impacts.append((factor, score, impact))
        
        # Sort by impact (descending)
        impacts.sort(key=lambda x: x[2], reverse=True)
        
        return impacts[:3]
    
    # ============================================================================
    # ML MODEL INTEGRATION HOOK
    # ============================================================================
    
    def predict_with_ml_model(self, profile: StudentProfile) -> Dict:
        """
        TODO: Replace with actual trained ML model.
        
        Example integration with scikit-learn model:
        
        Steps to integrate:
        1. Train and save a model using scikit-learn/XGBoost
        2. Load the model using pickle/joblib
        3. Transform profile data to match training features
        4. Make prediction
        
        Example:
        ```
        import pickle
        import pandas as pd
        
        # Load trained model
        with open('models/student_success_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Convert profile to DataFrame
        profile_dict = asdict(profile)
        df = pd.DataFrame([profile_dict])
        
        # Make prediction
        probability = model.predict_proba(df)[0][1]
        ```
        """
        # For now, use the rule-based prediction
        return self.predict(profile)