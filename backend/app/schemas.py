"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class Provider(str, Enum):
    """AI Provider enum"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    KIMI = "kimi"


class ModelRequest(BaseModel):
    """Request schema for model generation"""
    prompt: str = Field(..., min_length=1, max_length=50000, description="Input prompt for the model")
    provider: Provider = Field(..., description="AI provider to use")
    model: str = Field(..., min_length=1, max_length=100, description="Specific model name")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Temperature parameter")
    max_tokens: int = Field(1000, ge=1, le=32000, description="Maximum tokens to generate")
    system_prompt: Optional[str] = Field(None, max_length=10000, description="System prompt")


class ModelResponse(BaseModel):
    """Response schema for model generation"""
    content: str = Field(..., description="Generated content")
    model: str = Field(..., description="Model used")
    provider: str = Field(..., description="Provider used")
    tokens_used: Optional[int] = Field(None, description="Tokens used")
    finish_reason: Optional[str] = Field(None, description="Finish reason")
    timestamp: datetime = Field(default_factory=datetime.now)


class FeedbackCreate(BaseModel):
    """Schema for creating feedback"""
    session_id: Optional[str] = Field(None, max_length=100, description="Session ID")
    rating: int = Field(..., ge=1, le=5, description="Quality rating (1-5)")
    comments: Optional[str] = Field(None, max_length=5000, description="Feedback comments")
    response_id: Optional[str] = Field(None, max_length=100, description="Associated response ID")
    inline_feedback: Optional[List[Dict[str, Any]]] = Field(
        None, max_items=100, description="Inline feedback for specific words/phrases"
    )
    learning_rate: Optional[float] = Field(0.001, ge=0.0, le=1.0, description="Learning rate")


class FeedbackResponse(BaseModel):
    """Schema for feedback response"""
    id: str
    session_id: Optional[str]
    rating: int
    comments: Optional[str]
    response_id: Optional[str]
    inline_feedback: Optional[List[Dict[str, Any]]]
    learning_rate: float
    timestamp: datetime
    created_at: datetime


class AnalyticsRequest(BaseModel):
    """Schema for analytics queries"""
    start_date: Optional[datetime] = Field(None, description="Start date for analytics")
    end_date: Optional[datetime] = Field(None, description="End date for analytics")
    provider: Optional[Provider] = Field(None, description="Filter by provider")
    model: Optional[str] = Field(None, description="Filter by model")


class AnalyticsResponse(BaseModel):
    """Schema for analytics response"""
    total_sessions: int
    average_quality: float
    total_feedback: int
    improvement_rate: Optional[float]
    response_times: Optional[List[float]]
    quality_over_time: Optional[List[Dict[str, Any]]]
    feedback_distribution: Optional[Dict[str, int]]


class SettingsUpdate(BaseModel):
    """Schema for updating settings"""
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    kimi_api_key: Optional[str] = None
    theme: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None


class SettingsResponse(BaseModel):
    """Schema for settings response"""
    theme: Optional[str]
    primary_color: Optional[str]
    secondary_color: Optional[str]
    providers_configured: Dict[str, bool]
    created_at: datetime
    updated_at: datetime


class ConnectionTest(BaseModel):
    """Schema for connection test"""
    provider: Provider
    api_key: str


class ConnectionTestResponse(BaseModel):
    """Schema for connection test response"""
    success: bool
    message: str
    provider: str

