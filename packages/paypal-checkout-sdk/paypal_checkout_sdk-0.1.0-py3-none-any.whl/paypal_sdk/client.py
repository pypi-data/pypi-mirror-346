import httpx
import time
import base64
from typing import Optional, Any, Tuple
from .exceptions import AuthenticationError, APIError, RequestError, PayPalError
from .services.orders import OrdersService
from .enums import Environment

# Define environment URLs
ENV_URLS = {
    "sandbox": "https://api-m.sandbox.paypal.com",
    "live": "https://api-m.paypal.com"
}

class PayPalClient:
    """
    Main client for interacting with the PayPal REST API.

    Handles authentication, request retries, and provides access to API services.
    """
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        environment: Environment = Environment.SANDBOX,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        """
        Initializes the PayPalClient.

        Args:
            client_id: Your PayPal application's Client ID.
            client_secret: Your PayPal application's Client Secret.
            environment: The API environment (Environment.SANDBOX or Environment.LIVE).
                         Defaults to Environment.SANDBOX.
            timeout: Default request timeout in seconds. Defaults to 30.0.
            max_retries: Default maximum number of retries for failed requests. Defaults to 3.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = environment
        self.base_url = environment.get_url()
        self.timeout = timeout
        self.max_retries = max_retries

        self._access_token: Optional[str] = None
        self._token_expiry: Optional[float] = None # Store expiry time as timestamp
        self._token_type: str = "Bearer"

        # Initialize httpx client with retry transport
        # Note: Retries only apply to idempotent methods (GET, PUT, DELETE, HEAD, OPTIONS)
        # and specific status codes by default. POST requests are not retried by default.
        # More complex retry logic for POST might be needed depending on PayPal's idempotency guarantees.
        limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
        transport = httpx.HTTPTransport(retries=max_retries)
        self._http_client = httpx.Client(transport=transport, limits=limits, timeout=self.timeout)

        # Initialize services
        self.orders = OrdersService(self)
        # Add other services here as they are implemented (e.g., self.payments, self.webhooks)

    def _get_auth_headers(self) -> dict[str, str]:
        """
        Retrieves valid authentication headers, refreshing the token if necessary.

        Returns:
            A dictionary containing the Authorization header.

        Raises:
            AuthenticationError: If unable to obtain an access token.
        """
        if not self._is_token_valid():
            self._refresh_access_token()

        if not self._access_token:
             raise AuthenticationError("Failed to obtain or refresh access token.")

        return {"Authorization": f"{self._token_type} {self._access_token}"}

    def _is_token_valid(self) -> bool:
        """Checks if the current access token is valid and not expired."""
        # Check if token exists and expiry is set
        if not self._access_token or not self._token_expiry:
            return False
        # Check if token is expired (with a small buffer, e.g., 60 seconds)
        buffer_seconds = 60
        return time.time() < (self._token_expiry - buffer_seconds)

    def _refresh_access_token(self):
        """
        Obtains a new OAuth2 access token from PayPal.

        Raises:
            AuthenticationError: If the token request fails.
        """
        token_url = f"{self.base_url}/v1/oauth2/token"
        auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Accept-Language": "en_US" # Recommended by PayPal docs
        }
        data = {"grant_type": "client_credentials"}

        try:
            # Use a separate httpx client instance or direct call for auth
            # to avoid potential circular dependency or complex state in the main client's transport
            with httpx.Client(timeout=self.timeout) as auth_client:
                response = auth_client.post(token_url, headers=headers, data=data)
                response.raise_for_status() # Raise HTTPStatusError for 4xx/5xx responses

            response_data = response.json()
            self._access_token = response_data.get("access_token")
            self._token_type = response_data.get("token_type", "Bearer")
            expires_in = response_data.get("expires_in")

            if not self._access_token or not expires_in:
                raise AuthenticationError("Invalid token response received from PayPal.")

            # Calculate expiry time (timestamp)
            self._token_expiry = time.time() + expires_in
            print(f"Successfully obtained new PayPal access token (expires in {expires_in}s)") # Basic logging

        except httpx.HTTPStatusError as e:
            error_body = None
            try:
                error_body = e.response.json()
            except Exception:
                pass # Ignore if response body is not JSON
            if error_body:
                raise AuthenticationError(f"Failed to get access token: {error_body}")
            raise AuthenticationError(f"Failed to get access token: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise AuthenticationError(f"Network error during authentication: {e}") from e
        except Exception as e:
            raise AuthenticationError(f"An unexpected error occurred during authentication: {e}") from e

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Tuple[int, dict[str, Any]]:
        """
        Makes an authenticated request to the PayPal API.

        Args:
            method: HTTP method (e.g., 'GET', 'POST', 'PATCH').
            path: API endpoint path (e.g., '/v2/checkout/orders').
            params: URL query parameters.
            json_data: Request body data (will be JSON encoded).
            headers: Additional request headers.

        Returns:
            A tuple containing the HTTP status code and the JSON response data.

        Raises:
            APIError: If the PayPal API returns an error status code (4xx or 5xx).
            RequestError: If a network or request-related error occurs.
            AuthenticationError: If authentication fails.
            PayPalError: For other unexpected errors.
        """
        full_url = f"{self.base_url}{path}"
        auth_headers = self._get_auth_headers()
        request_headers = auth_headers.copy()
        if headers:
            request_headers.update(headers)

        # Ensure standard headers like Accept are present if not overridden
        if "Accept" not in request_headers:
             request_headers["Accept"] = "application/json"
        if method in ["POST", "PATCH", "PUT"] and "Content-Type" not in request_headers and json_data is not None:
             request_headers["Content-Type"] = "application/json"


        try:
            response = self._http_client.request(
                method=method,
                url=full_url,
                params=params,
                json=json_data, # httpx handles JSON encoding
                headers=request_headers,
            )

            # Check for API errors
            if not response.is_success: # Checks for 2xx status codes
                error_data = None
                try:
                    error_data = response.json()
                except Exception:
                    # If response is not JSON, create a basic error dict
                    error_data = {"message": response.text or f"HTTP error {response.status_code}"}
                raise APIError(response.status_code, error_data)

            # Handle successful responses
            # Handle 204 No Content specifically
            if response.status_code == 204:
                return response.status_code, {}

            # For other success codes, try to parse JSON
            try:
                response_json = response.json()
                return response.status_code, response_json
            except Exception as e:
                # If response is successful but not valid JSON (unexpected but possible)
                raise PayPalError(f"Failed to parse successful response JSON: {e}. Response text: {response.text[:1000]}")

        except httpx.TimeoutException as e:
            raise RequestError(f"Request to {method} {path} timed out: {e}") from e
        except httpx.RequestError as e:
            # Includes network errors, connection errors, etc.
            raise RequestError(f"HTTP request error for {method} {path}: {e}") from e
        except APIError:
             raise # Re-raise APIError directly
        except AuthenticationError:
             raise # Re-raise AuthenticationError directly
        except Exception as e:
            # Catch any other unexpected errors during the request/response cycle
            raise PayPalError(f"An unexpected error occurred during the API request to {method} {path}: {e}") from e

    def close(self):
        """Closes the underlying HTTP client."""
        self._http_client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

