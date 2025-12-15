"""Minimal configuration for ZeroVeil client SDK.

Connection settings only. All routing, tier selection, and model
decisions are handled server-side by the ZeroVeil relay.
"""

from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class ZeroVeilConfig:
    """Connection configuration for ZeroVeil client.

    Attributes:
        endpoint: ZeroVeil relay API endpoint URL
        api_key: API key for authentication
        timeout: Request timeout in seconds
    """
    endpoint: str = "https://api.zeroveil.io/v1"
    api_key: Optional[str] = None
    timeout: int = 60


def load_config() -> ZeroVeilConfig:
    """Load config from environment variables.

    Environment Variables:
        ZEROVEIL_ENDPOINT: API endpoint URL
        ZEROVEIL_API_KEY: API key for authentication
        ZEROVEIL_TIMEOUT: Request timeout in seconds

    Returns:
        ZeroVeilConfig with values from environment
    """
    return ZeroVeilConfig(
        endpoint=os.getenv("ZEROVEIL_ENDPOINT", "https://api.zeroveil.io/v1"),
        api_key=os.getenv("ZEROVEIL_API_KEY"),
        timeout=int(os.getenv("ZEROVEIL_TIMEOUT", "60")),
    )
