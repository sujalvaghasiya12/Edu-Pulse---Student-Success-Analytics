"""
Utility functions for calculations and data processing.
"""

import numpy as np
from typing import Dict, List, Tuple


def calculate_statistics(scores: List[float]) -> Dict:
    """
    Calculate basic statistics for a list of scores.
    
    Args:
        scores: List of numerical scores
        
    Returns:
        Dictionary with mean, median, std, min, max
    """
    if not scores:
        return {
            'mean': 0,
            'median': 0,
            'std': 0,
            'min': 0,
            'max': 0
        }
    
    return {
        'mean': round(np.mean(scores), 2),
        'median': round(np.median(scores), 2),
        'std': round(np.std(scores), 2),
        'min': round(np.min(scores), 2),
        'max': round(np.max(scores), 2)
    }


def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize scores to 0-100 scale for display.
    
    Args:
        scores: Dictionary of scores (0-1 scale)
        
    Returns:
        Dictionary of scores (0-100 scale)
    """
    return {k: round(v * 100, 1) for k, v in scores.items()}


def calculate_improvement_needed(current_score: float, target_score: float = 0.85) -> Dict:
    """
    Calculate improvement needed to reach target.
    
    Args:
        current_score: Current success probability (0-1)
        target_score: Target success probability (default: 0.85)
        
    Returns:
        Dictionary with improvement metrics
    """
    improvement = max(0, target_score - current_score)
    
    if improvement == 0:
        return {
            'needed': 0,
            'percentage': 0,
            'status': 'Target achieved'
        }
    
    percentage_needed = (improvement / current_score) * 100 if current_score > 0 else 100
    
    return {
        'needed': round(improvement, 3),
        'percentage': round(percentage_needed, 1),
        'status': f'Need {round(improvement * 100, 1)}% improvement'
    }


def estimate_intervention_impact(factor_scores: Dict[str, float], 
                                improvements: Dict[str, float]) -> float:
    """
    Estimate impact of proposed interventions.
    
    Args:
        factor_scores: Current factor scores
        improvements: Proposed improvements for each factor
        
    Returns:
        Estimated new success probability
    """
    from config import WEIGHTS
    
    new_score = 0
    
    # Calculate new weighted score with improvements
    for factor, current_score in factor_scores.items():
        improvement = improvements.get(factor, 0)
        new_factor_score = min(1.0, current_score + improvement)
        
        # Find weight for this factor
        weight = 0
        for category in WEIGHTS.values():
            if factor in category:
                weight = category[factor]
                break
        
        new_score += new_factor_score * weight
    
    return round(new_score, 4)


def generate_score_breakdown(factor_scores: Dict[str, float]) -> List[Dict]:
    """
    Generate detailed breakdown of scores by category.
    
    Args:
        factor_scores: Dictionary of factor scores
        
    Returns:
        List of dictionaries with category breakdown
    """
    from config import WEIGHTS
    
    categories = []
    
    for category_name, factors in WEIGHTS.items():
        category_score = 0
        max_possible = sum(factors.values())
        
        for factor, weight in factors.items():
            category_score += factor_scores.get(factor, 0) * weight
        
        # Normalize to 0-100
        normalized_score = (category_score / max_possible) * 100 if max_possible > 0 else 0
        
        categories.append({
            'category': category_name.replace('_', ' ').title(),
            'score': round(normalized_score, 1),
            'weight': round(max_possible * 100, 1),
            'factors': list(factors.keys())
        })
    
    return categories