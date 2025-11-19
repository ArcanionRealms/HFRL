"""
Settings router - Handles application settings
"""
from fastapi import APIRouter, HTTPException
from app.schemas import SettingsUpdate, SettingsResponse
from datetime import datetime
import os

router = APIRouter()

# In-memory settings storage (replace with database in production)
settings_storage = {
    "theme": "cosmic",
    "primary_color": "#FF00FF",
    "secondary_color": "#00FFFF",
    "providers_configured": {
        "openai": False,
        "anthropic": False,
        "deepseek": False,
        "kimi": False
    },
    "created_at": datetime.now(),
    "updated_at": datetime.now()
}


@router.get("", response_model=SettingsResponse)
async def get_settings():
    """
    Get current settings
    
    Returns:
        Settings response
    """
    return SettingsResponse(**settings_storage)


@router.put("", response_model=SettingsResponse)
async def update_settings(settings: SettingsUpdate):
    """
    Update settings
    
    Args:
        settings: Settings to update
    
    Returns:
        Updated settings response
    """
    try:
        # Update theme and colors if provided
        if settings.theme:
            settings_storage["theme"] = settings.theme
        if settings.primary_color:
            settings_storage["primary_color"] = settings.primary_color
        if settings.secondary_color:
            settings_storage["secondary_color"] = settings.secondary_color
        
        # Update API keys if provided (in production, store securely)
        if settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key
            settings_storage["providers_configured"]["openai"] = True
        if settings.anthropic_api_key:
            os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key
            settings_storage["providers_configured"]["anthropic"] = True
        if settings.deepseek_api_key:
            os.environ["DEEPSEEK_API_KEY"] = settings.deepseek_api_key
            settings_storage["providers_configured"]["deepseek"] = True
        if settings.kimi_api_key:
            os.environ["KIMI_API_KEY"] = settings.kimi_api_key
            settings_storage["providers_configured"]["kimi"] = True
        
        settings_storage["updated_at"] = datetime.now()
        
        return SettingsResponse(**settings_storage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

