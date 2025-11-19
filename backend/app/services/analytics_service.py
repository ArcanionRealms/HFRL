"""
Analytics Service - Handles analytics and metrics
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.schemas import AnalyticsRequest, AnalyticsResponse, Provider
from app.services.feedback_service import feedback_service


class AnalyticsService:
    """Service for analytics and metrics"""
    
    def get_analytics(
        self,
        request: AnalyticsRequest
    ) -> AnalyticsResponse:
        """
        Get analytics data
        
        Args:
            request: Analytics request with filters
        
        Returns:
            Analytics response with metrics
        """
        # Get all feedback
        all_feedback = feedback_service.get_all_feedback(limit=10000)
        
        # Apply filters
        filtered_feedback = all_feedback
        
        if request.start_date:
            filtered_feedback = [
                f for f in filtered_feedback
                if f.timestamp >= request.start_date
            ]
        
        if request.end_date:
            filtered_feedback = [
                f for f in filtered_feedback
                if f.timestamp <= request.end_date
            ]
        
        # Calculate metrics
        total_sessions = len(set(f.session_id for f in filtered_feedback if f.session_id))
        total_feedback = len(filtered_feedback)
        
        if filtered_feedback:
            average_quality = sum(f.rating for f in filtered_feedback) / total_feedback
        else:
            average_quality = 0.0
        
        # Calculate improvement rate
        improvement_rate = self._calculate_improvement_rate(filtered_feedback)
        
        # Get quality over time
        quality_over_time = self._get_quality_over_time(filtered_feedback)
        
        # Get feedback distribution
        feedback_distribution = self._get_feedback_distribution(filtered_feedback)
        
        return AnalyticsResponse(
            total_sessions=total_sessions,
            average_quality=round(average_quality, 2),
            total_feedback=total_feedback,
            improvement_rate=improvement_rate,
            response_times=None,  # TODO: Implement response time tracking
            quality_over_time=quality_over_time,
            feedback_distribution=feedback_distribution
        )
    
    def _calculate_improvement_rate(
        self,
        feedbacks: List
    ) -> Optional[float]:
        """Calculate improvement rate over time"""
        if len(feedbacks) < 2:
            return None
        
        # Sort by timestamp
        sorted_feedback = sorted(feedbacks, key=lambda x: x.timestamp)
        
        # Get first and last ratings
        first_rating = sorted_feedback[0].rating
        last_rating = sorted_feedback[-1].rating
        
        if first_rating == 0:
            return None
        
        improvement = ((last_rating - first_rating) / first_rating) * 100
        return round(improvement, 2)
    
    def _get_quality_over_time(
        self,
        feedbacks: List
    ) -> List[Dict[str, Any]]:
        """Get quality metrics over time"""
        if not feedbacks:
            return []
        
        # Group by date
        date_groups: Dict[str, List[float]] = {}
        
        for feedback in feedbacks:
            date_key = feedback.timestamp.date().isoformat()
            if date_key not in date_groups:
                date_groups[date_key] = []
            date_groups[date_key].append(feedback.rating)
        
        # Calculate average for each date
        quality_over_time = [
            {
                "date": date,
                "average_quality": sum(ratings) / len(ratings),
                "count": len(ratings)
            }
            for date, ratings in sorted(date_groups.items())
        ]
        
        return quality_over_time
    
    def _get_feedback_distribution(
        self,
        feedbacks: List
    ) -> Dict[str, int]:
        """Get distribution of feedback ratings"""
        distribution = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0
        }
        
        for feedback in feedbacks:
            rating_str = str(feedback.rating)
            if rating_str in distribution:
                distribution[rating_str] += 1
        
        return distribution


# Create singleton instance
analytics_service = AnalyticsService()

