from typing import TYPE_CHECKING, Optional
from ..models.orders import (
    CreateOrderRequest, CreateOrderResponse,
    CaptureOrderRequest, CaptureOrderResponse, Order
)
from ..exceptions import PayPalError, APIError, RequestError
import httpx # Import httpx for type hinting if needed, actual client is passed

if TYPE_CHECKING:
    from ..client import PayPalClient # Import for type hinting only

class OrdersService:
    """
    Service class for interacting with the PayPal Orders API V2.

    Provides methods for creating, retrieving, updating, and capturing orders.
    """
    def __init__(self, client: 'PayPalClient'):
        """
        Initializes the OrdersService.

        Args:
            client: An instance of the PayPalClient.
        """
        self._client = client
        self._base_path = "/v2/checkout/orders"

    def create_order(self, order_request: CreateOrderRequest, paypal_request_id: Optional[str] = None, prefer: str = "return=representation") -> CreateOrderResponse:
        """
        Creates a PayPal order.

        Args:
            order_request: A CreateOrderRequest model instance containing order details.
            paypal_request_id: Optional PayPal request ID for idempotency.
            prefer: Representation preference (e.g., 'return=minimal', 'return=representation').

        Returns:
            A CreateOrderResponse model instance representing the created order.

        Raises:
            APIError: If the PayPal API returns an error.
            RequestError: If there's an issue with the HTTP request itself.
            AuthenticationError: If authentication fails.
            ConfigurationError: If the client is not configured properly.
            PayPalError: For other SDK-related errors.
        """
        headers = {}
        if paypal_request_id:
            headers["PayPal-Request-Id"] = paypal_request_id
        if prefer:
            headers["Prefer"] = prefer

        try:
            status_code, response_data = self._client._make_request(
                method="POST",
                path=self._base_path,
                json_data=order_request.model_dump(exclude_none=True), # Use model_dump for Pydantic v2
                headers=headers
            )

            if status_code in [200, 201]: # 201 Created is standard, 200 OK might occur sometimes
                 # Parse the response using the Pydantic model
                return CreateOrderResponse.model_validate(response_data)
            else:
                # Let _make_request handle raising APIError for non-2xx codes
                 raise APIError(status_code, response_data) # Should be handled by _make_request, but as fallback

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise RequestError(f"An HTTP request error occurred: {e}")
        except APIError as e: # Re-raise APIError if caught from _make_request
             raise e
        except Exception as e: # Catch other potential errors during processing
            raise PayPalError(f"An unexpected error occurred during order creation: {e}")


    def capture_order(self, order_id: str, capture_request: Optional[CaptureOrderRequest] = None, paypal_request_id: Optional[str] = None, prefer: str = "return=representation") -> CaptureOrderResponse:
        """
        Captures payment for a previously approved PayPal order.

        Args:
            order_id: The ID of the order to capture payment for.
            capture_request: Optional request body details (rarely needed for basic capture).
            paypal_request_id: Optional PayPal request ID for idempotency.
            prefer: Representation preference (e.g., 'return=minimal', 'return=representation').

        Returns:
            A CaptureOrderResponse model instance representing the captured order details.

        Raises:
            APIError: If the PayPal API returns an error (e.g., order not approved, already captured).
            RequestError: If there's an issue with the HTTP request itself.
            AuthenticationError: If authentication fails.
            ConfigurationError: If the client is not configured properly.
            PayPalError: For other SDK-related errors.
        """
        path = f"{self._base_path}/{order_id}/capture"
        headers = {
            "Content-Type": "application/json" # Required by PayPal for capture
        }
        if paypal_request_id:
            headers["PayPal-Request-Id"] = paypal_request_id
        if prefer:
            headers["Prefer"] = prefer

        # Prepare JSON body - often empty, but handle if provided
        json_data = capture_request.model_dump(exclude_none=True) if capture_request else None

        try:
            status_code, response_data = self._client._make_request(
                method="POST",
                path=path,
                json_data=json_data, # Pass None if capture_request is None
                headers=headers
            )

            if status_code in [200, 201]: # 201 Created is standard, 200 OK might occur
                 # Parse the response using the Pydantic model
                return CaptureOrderResponse.model_validate(response_data)
            else:
                # Let _make_request handle raising APIError for non-2xx codes
                 raise APIError(status_code, response_data) # Should be handled by _make_request, but as fallback

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise RequestError(f"An HTTP request error occurred: {e}")
        except APIError as e: # Re-raise APIError if caught from _make_request
             raise e
        except Exception as e: # Catch other potential errors during processing
            raise PayPalError(f"An unexpected error occurred during order capture: {e}")

    def get_order(self, order_id: str) -> Order:
        """
        Retrieves the details of a PayPal order.

        Args:
            order_id: The ID of the order to retrieve.

        Returns:
            An Order model instance containing the order details.

        Raises:
            APIError: If the PayPal API returns an error (e.g., order not found).
            RequestError: If there's an issue with the HTTP request itself.
            AuthenticationError: If authentication fails.
            ConfigurationError: If the client is not configured properly.
            PayPalError: For other SDK-related errors.
        """
        path = f"{self._base_path}/{order_id}"
        try:
            status_code, response_data = self._client._make_request(
                method="GET",
                path=path
            )

            if status_code == 200:
                return Order.model_validate(response_data)
            else:
                 raise APIError(status_code, response_data) # Should be handled by _make_request

        except httpx.TimeoutException as e:
            raise RequestError(f"Request timed out: {e}")
        except httpx.RequestError as e:
            raise RequestError(f"An HTTP request error occurred: {e}")
        except APIError as e: # Re-raise APIError if caught from _make_request
             raise e
        except Exception as e: # Catch other potential errors during processing
            raise PayPalError(f"An unexpected error occurred while getting order details: {e}")

