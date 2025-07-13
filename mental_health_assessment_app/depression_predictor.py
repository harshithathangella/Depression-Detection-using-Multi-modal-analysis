import numpy as np
from typing import Optional, List

class DepressionPredictor:
    def __init__(self):
        # Weights for combining text and voice analysis
        self.text_weight = 0.6
        self.voice_weight = 0.4
        
        # Risk thresholds (lower scores = lower risk)
        self.low_risk_threshold = 3.0
        self.moderate_risk_threshold = 5.0
        self.high_risk_threshold = 7.0
    
    def predict_depression_risk(self, text_score: Optional[float], voice_score: Optional[float]) -> float:
        """
        Combine text and voice analysis scores to predict depression risk
        Returns a score from 0-10 where lower scores indicate higher risk
        """
        if text_score is None and voice_score is None:
            return 5.0  # Neutral score if no data
        
        # If only one score is available, use it directly with slight confidence adjustment
        if text_score is None:
            # Only voice data available - use it with slight conservative adjustment
            return max(0.0, min(10.0, voice_score * 0.9 + 0.5))
        
        if voice_score is None:
            # Only text data available - use it with minimal adjustment
            return max(0.0, min(10.0, text_score * 0.95 + 0.2))
        
        # Combine both scores using weighted average
        combined_score = (text_score * self.text_weight) + (voice_score * self.voice_weight)
        
        # Ensure score is within valid range
        return max(0.0, min(10.0, combined_score))
    
    def get_risk_level(self, score: float) -> str:
        """Convert numerical score to risk level category"""
        if score <= self.low_risk_threshold:
            return "Low Risk"
        elif score <= self.moderate_risk_threshold:
            return "Moderate Risk"
        elif score <= self.high_risk_threshold:
            return "High Risk"
        else:
            return "Very High Risk"
    
    def get_recommendations(self, score: float) -> List[str]:
        """Get personalized recommendations based on risk score"""
        recommendations = []
        
        if score <= self.low_risk_threshold:
            # Low risk recommendations
            recommendations.extend([
                "Continue maintaining good mental health habits",
                "Regular exercise and healthy sleep patterns can help maintain wellbeing",
                "Consider mindfulness or meditation practices for stress management",
                "Stay connected with friends and family",
                "Engage in hobbies and activities you enjoy"
            ])
        
        elif score <= self.moderate_risk_threshold:
            # Moderate risk recommendations
            recommendations.extend([
                "Consider speaking with a mental health professional for support",
                "Establish a regular daily routine to provide structure",
                "Prioritize self-care activities and stress management",
                "Reach out to trusted friends or family members for support",
                "Consider joining a support group or community activity",
                "Monitor your mood and symptoms regularly"
            ])
        
        elif score <= self.high_risk_threshold:
            # High risk recommendations
            recommendations.extend([
                "Strongly consider scheduling an appointment with a mental health professional",
                "Reach out to a crisis helpline if you're feeling overwhelmed",
                "Don't isolate yourself - maintain regular contact with supportive people",
                "Consider temporary adjustments to work or school responsibilities",
                "Avoid making major life decisions while experiencing symptoms",
                "Focus on basic self-care: regular meals, sleep, and hygiene"
            ])
        
        else:
            # Very high risk recommendations
            recommendations.extend([
                "Seek immediate professional help - contact a mental health crisis line",
                "Consider visiting an emergency room if you're having thoughts of self-harm",
                "Ensure you have 24/7 access to support through crisis hotlines",
                "Remove any means of self-harm from your environment",
                "Stay with trusted friends or family members if possible",
                "Follow up with a mental health professional within 24-48 hours"
            ])
        
        # General recommendations for all risk levels
        recommendations.extend([
            "Remember that seeking help is a sign of strength, not weakness",
            "Mental health conditions are treatable with proper support",
            "Small steps toward improvement are still meaningful progress"
        ])
        
        return recommendations
    
    def get_confidence_level(self, text_score: Optional[float], voice_score: Optional[float]) -> str:
        """Determine confidence level of the prediction"""
        if text_score is not None and voice_score is not None:
            # Both analyses available
            score_difference = abs(text_score - voice_score)
            if score_difference < 1.0:
                return "High Confidence"
            elif score_difference < 2.0:
                return "Moderate Confidence"
            else:
                return "Low Confidence (Conflicting Signals)"
        
        elif text_score is not None or voice_score is not None:
            # Only one analysis available
            return "Moderate Confidence"
        
        else:
            # No analysis available
            return "No Confidence"
    
    def get_analysis_summary(self, text_score: Optional[float], voice_score: Optional[float]) -> dict:
        """Get comprehensive analysis summary"""
        combined_score = self.predict_depression_risk(text_score, voice_score)
        risk_level = self.get_risk_level(combined_score)
        confidence = self.get_confidence_level(text_score, voice_score)
        recommendations = self.get_recommendations(combined_score)
        
        return {
            'combined_score': combined_score,
            'risk_level': risk_level,
            'confidence': confidence,
            'recommendations': recommendations,
            'text_score': text_score,
            'voice_score': voice_score,
            'analysis_completeness': self._get_completeness_score(text_score, voice_score)
        }
    
    def _get_completeness_score(self, text_score: Optional[float], voice_score: Optional[float]) -> float:
        """Calculate how complete the analysis is (0-1 scale)"""
        if text_score is not None and voice_score is not None:
            return 1.0
        elif text_score is not None or voice_score is not None:
            return 0.6
        else:
            return 0.0
