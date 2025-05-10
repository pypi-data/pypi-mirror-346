from typing import Any


class PayPalError(Exception):
    """Base exception class for PayPal SDK errors."""
    def __init__(self, message="An error occurred with the PayPal SDK"):
        self.message = message
        super().__init__(self.message)

class AuthenticationError(PayPalError):
    """Raised when authentication with the PayPal API fails."""
    def __init__(self, message="PayPal authentication failed"):
        super().__init__(message)

class APIError(PayPalError):
    """Raised when the PayPal API returns an error response."""
    def __init__(self, status_code: int, error_response: dict | None = None):
        self.status_code = status_code
        self.error_response = error_response or {}
        self.name = self.error_response.get('name', 'UNKNOWN_ERROR')
        self.message = self.error_response.get('message', 'An unknown API error occurred')
        self.short_message = self.error_response.get('message', 'An unknown API error occurred')
        self.debug_id = self.error_response.get('debug_id')
        self.details: list[dict[str, Any]] = self.error_response.get('details', [])
        # Construct a more informative message
        full_message = f"PayPal API Error ({self.name}): {self.message} (Status Code: {status_code}"
        if self.debug_id:
            full_message += f", Debug ID: {self.debug_id}"
        if self.details:
            details_str = "; ".join([f"{d.get('field', '')}: {d.get('description', '')}" for d in self.details])
            full_message += f", Details: {details_str}"
        full_message += ")"

        super().__init__(full_message)

    def __str__(self):
        return self.message # Use the constructed message

class ConfigurationError(PayPalError):
    """Raised for configuration-related errors."""
    def __init__(self, message="PayPal SDK configuration error"):
        super().__init__(message)

class RequestError(PayPalError):
    """Raised for errors during the HTTP request process (e.g., network issues, timeouts)."""
    def __init__(self, message="Error during HTTP request to PayPal API"):
        super().__init__(message)

