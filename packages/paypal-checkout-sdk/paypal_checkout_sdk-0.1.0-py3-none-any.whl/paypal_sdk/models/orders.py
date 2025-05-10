from enum import StrEnum
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, Any
from .base import Money, LinkDescription, Name, AddressPortable

# --- Enums ---
class OrderIntent(StrEnum):
    CAPTURE = "CAPTURE"
    AUTHORIZE = "AUTHORIZE"

class LandingPage(StrEnum):
    LOGIN = "LOGIN"
    BILLING = "BILLING"
    NO_PREFERENCE = "NO_PREFERENCE"

class ShippingPreference(StrEnum):
    GET_FROM_FILE = "GET_FROM_FILE"
    NO_SHIPPING = "NO_SHIPPING"
    SET_PROVIDED_ADDRESS = "SET_PROVIDED_ADDRESS"

class UserAction(StrEnum):
    CONTINUE = "CONTINUE"
    PAY_NOW = "PAY_NOW"

class OrderStatus(StrEnum):
    CREATED = "CREATED"
    SAVED = "SAVED"
    APPROVED = "APPROVED"
    VOIDED = "VOIDED"
    COMPLETED = "COMPLETED"
    PAYER_ACTION_REQUIRED = "PAYER_ACTION_REQUIRED"

class CaptureStatus(StrEnum):
    COMPLETED = "COMPLETED"
    DECLINED = "DECLINED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    PENDING = "PENDING"
    REFUNDED = "REFUNDED"
    FAILED = "FAILED"

class SellerProtectionStatus(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    PARTIALLY_ELIGIBLE = "PARTIALLY_ELIGIBLE"
    NOT_ELIGIBLE = "NOT_ELIGIBLE"


# --- Request Models ---

class ExperienceContext(BaseModel):
    """Customizes the payer experience during the approval process."""
    brand_name: Optional[str] = Field(None, max_length=127)
    locale: Optional[str] = Field(None, pattern=r"^[a-z]{2}(?:-[A-Z][a-z]{3})?(?:-(?:[A-Z]{2}))?$") # e.g., en-US
    landing_page: Optional[LandingPage] = LandingPage.NO_PREFERENCE
    shipping_preference: Optional[ShippingPreference] = ShippingPreference.GET_FROM_FILE
    user_action: Optional[UserAction] = UserAction.CONTINUE
    return_url: Optional[HttpUrl] = Field(None, description="URL to redirect payer after approval.")
    cancel_url: Optional[HttpUrl] = Field(None, description="URL to redirect payer if they cancel.")
    # payment_method_preference: Optional[str] = None # Deprecated/Complex, omitting for now
    # stored_payment_source: Optional[dict] = None # Complex, omitting for now

class PayPalPaymentSource(BaseModel):
    """Details for PayPal payment source."""
    experience_context: Optional[ExperienceContext] = None

class PaymentSource(BaseModel):
    """The payment source definition for the order."""
    paypal: Optional[PayPalPaymentSource] = None
    # card: Optional[dict] = None # Add later if needed

class PurchaseUnitRequest(BaseModel):
    """Represents a purchase unit in an order creation request."""
    reference_id: Optional[str] = Field(None, max_length=256)
    amount: Money
    description: Optional[str] = Field(None, max_length=127)
    custom_id: Optional[str] = Field(None, max_length=127)
    invoice_id: Optional[str] = Field(None, max_length=127)
    soft_descriptor: Optional[str] = Field(None, max_length=22)
    # items: Optional[list[dict]] = None # Add later if needed
    # shipping: Optional[dict] = None # Add later if needed

class CreateOrderRequest(BaseModel):
    """Request body for creating an order."""
    intent: OrderIntent
    purchase_units: list[PurchaseUnitRequest]
    payment_source: Optional[PaymentSource] = None
    # application_context: Optional[ExperienceContext] = None # Deprecated, use payment_source.paypal.experience_context

# --- Response Models ---

class Payee(BaseModel):
    """The merchant who receives payment for this transaction."""
    email_address: Optional[EmailStr] = None
    merchant_id: Optional[str] = Field(None, min_length=13, max_length=13)

class SellerProtection(BaseModel):
    """Protection eligibility for the seller."""
    status: Optional[SellerProtectionStatus] = None
    dispute_categories: Optional[list[str]] = None

class SellerReceivableBreakdown(BaseModel):
    """Breakdown of the seller's receivable funds."""
    gross_amount: Money
    paypal_fee: Optional[Money] = None
    net_amount: Optional[Money] = None
    # receivable_amount: Optional[Money] = None # Deprecated
    # exchange_rate: Optional[dict] = None # Add later if needed

class Capture(BaseModel):
    """A captured payment detail."""
    id: str
    status: CaptureStatus
    amount: Money
    final_capture: bool
    seller_protection: SellerProtection
    seller_receivable_breakdown: Optional[SellerReceivableBreakdown] = None
    links: list[LinkDescription]
    create_time: str # Consider datetime parsing later
    update_time: str # Consider datetime parsing later
    # disbursement_mode: Optional[str] = None # Add later if needed
    # processor_response: Optional[dict] = None # Add later if needed

class Payments(BaseModel):
    """Payment details for a purchase unit."""
    # authorizations: Optional[list[dict]] = None # Add later if needed for AUTHORIZE intent
    captures: Optional[list[Capture]] = None

class PurchaseUnit(BaseModel):
    """Represents a purchase unit in an order response."""
    reference_id: Optional[str] = None
    amount: Optional[Money] = None # Optional in some responses
    payee: Optional[Payee] = None
    # description: Optional[str] = None
    # custom_id: Optional[str] = None
    # invoice_id: Optional[str] = None
    # soft_descriptor: Optional[str] = None
    # items: Optional[list[dict]] = None # Add later if needed
    # shipping: Optional[dict] = None # Add later if needed
    payments: Optional[Payments] = None

class Payer(BaseModel):
    """Information about the payer."""
    name: Optional[Name] = None
    email_address: Optional[EmailStr] = None
    payer_id: Optional[str] = Field(None, min_length=13, max_length=13)
    # phone: Optional[dict] = None # Add later if needed
    address: Optional[AddressPortable] = None

class Order(BaseModel):
    """Represents a PayPal order."""
    id: str
    intent: Optional[OrderIntent] = None # Not always present in capture response
    status: OrderStatus
    payment_source: Optional[dict[str, Any]] = None # Can contain 'card', 'paypal', etc. Keeping generic for now.
    purchase_units: list[PurchaseUnit]
    payer: Optional[Payer] = None
    create_time: Optional[str] = None # Consider datetime parsing later
    update_time: Optional[str] = None # Consider datetime parsing later
    links: list[LinkDescription]

# Specific response model for Create Order, inheriting from base Order
class CreateOrderResponse(Order):
    pass

# Specific response model for Capture Order, inheriting from base Order
class CaptureOrderResponse(Order):
    pass

# Request model for Capture Order (often empty, but can specify payment source)
class CaptureOrderRequest(BaseModel):
    payment_source: Optional[PaymentSource] = None
    # Add other potential fields like soft_descriptor if needed later

