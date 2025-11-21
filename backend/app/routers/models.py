"""
Models router - Handles AI model interactions
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.schemas import (
    ModelRequest,
    ModelResponse,
    Provider,
    ConnectionTest,
    ConnectionTestResponse
)
from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/generate", response_model=ModelResponse)
async def generate_content(
    request: ModelRequest,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Generate content using the specified AI model
    
    Args:
        request: Model generation request
        x_api_key: Optional API key override in header
    
    Returns:
        Generated content response
    """
    try:
        response = await ai_service.generate(request, api_key=x_api_key)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-connection", response_model=ConnectionTestResponse)
async def test_connection(test: ConnectionTest):
    """
    Test connection to an AI provider
    
    Args:
        test: Connection test request with provider and API key
    
    Returns:
        Connection test response
    """
    try:
        success = await ai_service.test_connection(test.provider, test.api_key)
        
        return ConnectionTestResponse(
            success=success,
            message="Connection successful" if success else "Connection failed",
            provider=test.provider.value
        )
    except Exception as e:
        return ConnectionTestResponse(
            success=False,
            message=str(e),
            provider=test.provider.value
        )


@router.get("/providers")
async def get_providers():
    """Get list of available AI providers"""
    return {
        "providers": [
            {
                "id": "openai",
                "name": "OpenAI",
                "models": [
                    "gpt-4",
                    "gpt-4-turbo",
                    "gpt-3.5-turbo",
                    "gpt-3.5-turbo-16k"
                ],
                "status": "available"
            },
            {
                "id": "anthropic",
                "name": "Anthropic",
                "models": [
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307"
                ],
                "status": "available"
            },
            {
                "id": "deepseek",
                "name": "Deepseek",
                "models": [
                    "deepseek-chat",
                    "deepseek-coder"
                ],
                "status": "available"
            },
            {
                "id": "kimi",
                "name": "Kimi K2",
                "models": [
                    "moonshot-v1-8k",
                    "moonshot-v1-32k",
                    "moonshot-v1-128k"
                ],
                "status": "available"
            }
        ]
    }

