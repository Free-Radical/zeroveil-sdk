# Copyright © 2025 Saqib Ali Khan. All Rights Reserved.
# Licensed under Business Source License 1.1

"""ZeroVeil - Minimal client SDK for ZeroVeil privacy relay.

Usage:
    from zeroveil import ZeroVeilClient, scrub

    # Scrub PII locally before sending
    result = scrub("Contact John at john@example.com")
    clean_text = result.text  # "Contact <PERSON> at <EMAIL_ADDRESS>"

    # Send to ZeroVeil relay
    client = ZeroVeilClient()
    response = client.send(clean_text)
    print(response.content)

For more info: https://github.com/Free-Radical/Cortex1-ZeroVeil
"""

from zeroveil.client.config import ZeroVeilConfig, load_config
from zeroveil.client.api_client import ZeroVeilClient, Response, create_client
from zeroveil.client.scrubber import scrub, ScrubResult, is_available as pii_available
from zeroveil.client.device_detector import (
    detect_device_capabilities,
    DeviceCapability,
    DeviceDetectionResult,
)

__version__ = "0.1.0"

__all__ = [
    # Config
    "ZeroVeilConfig",
    "load_config",
    # API Client
    "ZeroVeilClient",
    "Response",
    "create_client",
    # PII Scrubber
    "scrub",
    "ScrubResult",
    "pii_available",
    # Device Detection (utility)
    "detect_device_capabilities",
    "DeviceCapability",
    "DeviceDetectionResult",
]
