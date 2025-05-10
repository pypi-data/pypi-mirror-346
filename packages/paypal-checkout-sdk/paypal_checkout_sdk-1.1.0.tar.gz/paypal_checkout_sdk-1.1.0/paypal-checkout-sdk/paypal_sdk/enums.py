from enum import StrEnum

class Environment(StrEnum):
    """
    PayPal API Environments
    """
    SANDBOX = "sandbox"
    LIVE = "live"

    def get_url(self) -> str:
        """Returns the base URL for the environment."""
        if self == Environment.SANDBOX:
            return "https://api-m.sandbox.paypal.com"
        elif self == Environment.LIVE:
            return "https://api-m.paypal.com"
        # This case should not be reached if enum is used correctly
        raise ValueError(f"Unknown environment: {self.value}")
