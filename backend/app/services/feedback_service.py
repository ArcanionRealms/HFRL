"""
Feedback Service - Handles feedback storage and retrieval
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.schemas import FeedbackCreate, FeedbackResponse
import uuid
import json


# In-memory storage (replace with database in production)
feedback_storage: Dict[str, Dict[str, Any]] = {}


class FeedbackService:
    """Service for managing feedback"""
    
    def create_feedback(self, feedback: FeedbackCreate) -> FeedbackResponse:
        """
        Create a new feedback entry
        
        Args:
            feedback: Feedback data to create
        
        Returns:
            Created feedback response
        """
        feedback_id = str(uuid.uuid4())
        session_id = feedback.session_id or str(uuid.uuid4())
        
        feedback_data = {
            "id": feedback_id,
            "session_id": session_id,
            "rating": feedback.rating,
            "comments": feedback.comments,
            "response_id": feedback.response_id,
            "inline_feedback": feedback.inline_feedback or [],
            "learning_rate": feedback.learning_rate or 0.001,
            "timestamp": datetime.now(),
            "created_at": datetime.now()
        }
        
        feedback_storage[feedback_id] = feedback_data
        
        return FeedbackResponse(**feedback_data)
    
    def get_feedback(self, feedback_id: str) -> Optional[FeedbackResponse]:
        """Get feedback by ID"""
        feedback_data = feedback_storage.get(feedback_id)
        if feedback_data:
            return FeedbackResponse(**feedback_data)
        return None
    
    def get_feedback_by_session(self, session_id: str) -> List[FeedbackResponse]:
        """Get all feedback for a session"""
        feedbacks = [
            FeedbackResponse(**data)
            for data in feedback_storage.values()
            if data.get("session_id") == session_id
        ]
        return sorted(feedbacks, key=lambda x: x.timestamp, reverse=True)
    
    def get_all_feedback(
        self,
        limit: int = 100,
        offset: int = 0
    ) -> List[FeedbackResponse]:
        """Get all feedback with pagination"""
        feedbacks = [
            FeedbackResponse(**data)
            for data in feedback_storage.values()
        ]
        feedbacks = sorted(feedbacks, key=lambda x: x.timestamp, reverse=True)
        return feedbacks[offset:offset + limit]
    
    def delete_feedback(self, feedback_id: str) -> bool:
        """Delete feedback by ID"""
        if feedback_id in feedback_storage:
            del feedback_storage[feedback_id]
            return True
        return False
    
    def get_average_rating(self, session_id: Optional[str] = None) -> float:
        """Get average rating"""
        feedbacks = (
            self.get_feedback_by_session(session_id)
            if session_id
            else self.get_all_feedback(limit=10000)
        )
        
        if not feedbacks:
            return 0.0
        
        total_rating = sum(f.rating for f in feedbacks)
        return total_rating / len(feedbacks)


# Create singleton instance
feedback_service = FeedbackService()

