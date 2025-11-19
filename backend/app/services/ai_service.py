"""
AI Service - Handles interactions with various AI providers
"""
import httpx
import os
import logging
from typing import Optional
from app.schemas import Provider, ModelRequest, ModelResponse
from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for interacting with AI providers"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", settings.OPENAI_API_KEY)
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", settings.ANTHROPIC_API_KEY)
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", settings.DEEPSEEK_API_KEY)
        self.kimi_api_key = os.getenv("KIMI_API_KEY", settings.KIMI_API_KEY)
        self.timeout = settings.REQUEST_TIMEOUT
    
    async def generate(
        self,
        request: ModelRequest,
        api_key: Optional[str] = None
    ) -> ModelResponse:
        """
        Generate content using the specified AI provider
        
        Args:
            request: Model request with prompt and parameters
            api_key: Optional API key override
        
        Returns:
            ModelResponse with generated content
        
        Raises:
            ValueError: If provider is unsupported or configuration is invalid
            Exception: If API call fails
        """
        logger.info(f"Generating content with provider: {request.provider}, model: {request.model}")
        
        try:
            if request.provider == Provider.OPENAI:
                return await self._generate_openai(request, api_key)
            elif request.provider == Provider.ANTHROPIC:
                return await self._generate_anthropic(request, api_key)
            elif request.provider == Provider.DEEPSEEK:
                return await self._generate_deepseek(request, api_key)
            elif request.provider == Provider.KIMI:
                return await self._generate_kimi(request, api_key)
            else:
                raise ValueError(f"Unsupported provider: {request.provider}")
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}", exc_info=True)
            raise
    
    async def _generate_openai(
        self,
        request: ModelRequest,
        api_key: Optional[str] = None
    ) -> ModelResponse:
        """Generate content using OpenAI API"""
        api_key = api_key or self.openai_api_key
        if not api_key:
            raise ValueError("OpenAI API key not configured")
        
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=api_key)
            
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            response = await client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return ModelResponse(
                content=response.choices[0].message.content,
                model=request.model,
                provider="openai",
                tokens_used=response.usage.total_tokens if response.usage else None,
                finish_reason=response.choices[0].finish_reason
            )
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _generate_anthropic(
        self,
        request: ModelRequest,
        api_key: Optional[str] = None
    ) -> ModelResponse:
        """Generate content using Anthropic API"""
        api_key = api_key or self.anthropic_api_key
        if not api_key:
            raise ValueError("Anthropic API key not configured")
        
        try:
            import anthropic
            
            client = anthropic.AsyncAnthropic(api_key=api_key)
            
            system_prompt = request.system_prompt or ""
            
            response = await client.messages.create(
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": request.prompt}
                ]
            )
            
            return ModelResponse(
                content=response.content[0].text,
                model=request.model,
                provider="anthropic",
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                finish_reason=response.stop_reason
            )
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def _generate_deepseek(
        self,
        request: ModelRequest,
        api_key: Optional[str] = None
    ) -> ModelResponse:
        """Generate content using Deepseek API"""
        api_key = api_key or self.deepseek_api_key
        if not api_key:
            raise ValueError("Deepseek API key not configured")
        
        try:
            from openai import AsyncOpenAI
            
            # Deepseek uses OpenAI-compatible API
            client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )
            
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            response = await client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return ModelResponse(
                content=response.choices[0].message.content,
                model=request.model,
                provider="deepseek",
                tokens_used=response.usage.total_tokens if response.usage else None,
                finish_reason=response.choices[0].finish_reason
            )
        except Exception as e:
            raise Exception(f"Deepseek API error: {str(e)}")
    
    async def _generate_kimi(
        self,
        request: ModelRequest,
        api_key: Optional[str] = None
    ) -> ModelResponse:
        """Generate content using Kimi API"""
        api_key = api_key or self.kimi_api_key
        if not api_key:
            raise ValueError("Kimi API key not configured")
        
        try:
            from openai import AsyncOpenAI
            
            # Kimi uses OpenAI-compatible API
            client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.moonshot.cn/v1"
            )
            
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            response = await client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return ModelResponse(
                content=response.choices[0].message.content,
                model=request.model,
                provider="kimi",
                tokens_used=response.usage.total_tokens if response.usage else None,
                finish_reason=response.choices[0].finish_reason
            )
        except Exception as e:
            raise Exception(f"Kimi API error: {str(e)}")
    
    async def test_connection(
        self,
        provider: Provider,
        api_key: str
    ) -> bool:
        """
        Test connection to an AI provider
        
        Args:
            provider: AI provider to test
            api_key: API key to use for testing
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create a simple test request
            test_request = ModelRequest(
                prompt="Hello",
                provider=provider,
                model=self._get_default_model(provider),
                temperature=0.7,
                max_tokens=10
            )
            
            # Try to generate a response
            await self.generate(test_request, api_key)
            return True
        except Exception:
            return False
    
    def _get_default_model(self, provider: Provider) -> str:
        """Get default model for a provider"""
        defaults = {
            Provider.OPENAI: "gpt-3.5-turbo",
            Provider.ANTHROPIC: "claude-3-haiku-20240307",
            Provider.DEEPSEEK: "deepseek-chat",
            Provider.KIMI: "moonshot-v1-8k"
        }
        return defaults.get(provider, "gpt-3.5-turbo")


# Create singleton instance
ai_service = AIService()

