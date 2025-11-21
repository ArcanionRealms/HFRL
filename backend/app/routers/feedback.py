"""
Feedback router - Handles feedback operations
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.schemas import FeedbackCreate, FeedbackResponse
from app.services.feedback_service import feedback_service

router = APIRouter()


@router.post("", response_model=FeedbackResponse)
async def create_feedback(feedback: FeedbackCreate):
    """
    Create a new feedback entry
    
    Args:
        feedback: Feedback data to create
    
    Returns:
        Created feedback response
    """
    try:
        return feedback_service.create_feedback(feedback)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(feedback_id: str):
    """
    Get feedback by ID
    
    Args:
        feedback_id: Feedback ID
    
    Returns:
        Feedback response
    """
    feedback = feedback_service.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.get("", response_model=List[FeedbackResponse])
async def get_all_feedback(
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get all feedback with optional filters
    
    Args:
        session_id: Optional session ID filter
        limit: Maximum number of results
        offset: Offset for pagination
    
    Returns:
        List of feedback responses
    """
    try:
        if session_id:
            return feedback_service.get_feedback_by_session(session_id)
        return feedback_service.get_all_feedback(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: str):
    """
    Delete feedback by ID
    
    Args:
        feedback_id: Feedback ID to delete
    
    Returns:
        Success message
    """
    success = feedback_service.delete_feedback(feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}


@router.get("/session/{session_id}/average")
async def get_session_average(session_id: str):
    """
    Get average rating for a session
    
    Args:
        session_id: Session ID
    
    Returns:
        Average rating
    """
    average = feedback_service.get_average_rating(session_id)
    return {
        "session_id": session_id,
        "average_rating": average
    }

