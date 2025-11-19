"""
Custom exceptions for the application
"""


class HFRLException(Exception):
    """Base exception for HFRL application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class APIKeyNotConfiguredError(HFRLException):
    """Raised when API key is not configured"""
    def __init__(self, provider: str):
        super().__init__(
            f"API key for {provider} is not configured",
            status_code=400
        )


class ProviderAPIError(HFRLException):
    """Raised when provider API call fails"""
    def __init__(self, provider: str, message: str):
        super().__init__(
            f"{provider} API error: {message}",
            status_code=502
        )


class InvalidRequestError(HFRLException):
    """Raised when request is invalid"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ResourceNotFoundError(HFRLException):
    """Raised when resource is not found"""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            f"{resource} with ID {resource_id} not found",
            status_code=404
        )
