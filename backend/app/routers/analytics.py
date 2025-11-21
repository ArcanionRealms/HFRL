"""
Analytics router - Handles analytics and metrics
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from app.schemas import AnalyticsRequest, AnalyticsResponse, Provider
from app.services.analytics_service import analytics_service

router = APIRouter()


@router.post("", response_model=AnalyticsResponse)
async def get_analytics(request: AnalyticsRequest):
    """
    Get analytics data
    
    Args:
        request: Analytics request with filters
    
    Returns:
        Analytics response with metrics
    """
    try:
        return analytics_service.get_analytics(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=AnalyticsResponse)
async def get_analytics_query(
    start_date: Optional[datetime] = Query(None, description="Start date for analytics"),
    end_date: Optional[datetime] = Query(None, description="End date for analytics"),
    provider: Optional[Provider] = Query(None, description="Filter by provider"),
    model: Optional[str] = Query(None, description="Filter by model")
):
    """
    Get analytics data using query parameters
    
    Args:
        start_date: Start date for analytics
        end_date: End date for analytics
        provider: Filter by provider
        model: Filter by model
    
    Returns:
        Analytics response with metrics
    """
    try:
        request = AnalyticsRequest(
            start_date=start_date,
            end_date=end_date,
            provider=provider,
            model=model
        )
        return analytics_service.get_analytics(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

