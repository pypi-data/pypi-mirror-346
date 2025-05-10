from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class Money(BaseModel):
    """Represents a monetary amount."""
    currency_code: str = Field(..., description="The three-character ISO-4217 currency code.")
    value: str = Field(..., description="The amount value.")

class LinkDescription(BaseModel):
    """Represents a HATEOAS link."""
    href: HttpUrl = Field(..., description="The complete target URL.")
    rel: str = Field(..., description="The relationship of the target URL to the current resource.")
    method: Optional[str] = Field(None, description="The HTTP method required to make the related call.")

class Name(BaseModel):
    """Represents a person's name."""
    given_name: Optional[str] = Field(None, description="The given name of the person.")
    surname: Optional[str] = Field(None, description="The surname of the person.")
    full_name: Optional[str] = Field(None, description="The full name representation.") # Sometimes provided

class AddressPortable(BaseModel):
    """Represents a postal address."""
    address_line_1: Optional[str] = Field(None, description="The first line of the address.")
    address_line_2: Optional[str] = Field(None, description="The second line of the address.")
    admin_area_1: Optional[str] = Field(None, description="The highest-level sub-division in a country (e.g., state, province).")
    admin_area_2: Optional[str] = Field(None, description="A city, town, or village.")
    postal_code: Optional[str] = Field(None, description="The postal code.")
    country_code: str = Field(..., description="The two-character ISO 3166-1 country code.")

