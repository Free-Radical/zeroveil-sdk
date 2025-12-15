# Copyright © 2025 Saqib Ali Khan. All Rights Reserved.
# Licensed under Business Source License 1.1

"""ZeroVeil client SDK.

Minimal client for the ZeroVeil privacy relay:
- scrubber: PII scrubbing (Presidio wrapper)
- api_client: Simple send/receive
- device_detector: Hardware capability detection (utility)
- config: Connection settings
"""

from zeroveil.client.config import ZeroVeilConfig, load_config
from zeroveil.client.api_client import ZeroVeilClient, Response, create_client
from zeroveil.client.scrubber import scrub, ScrubResult, is_available as pii_available
from zeroveil.client.device_detector import (
    detect_device_capabilities,
    DeviceCapability,
    RoutingMode,
    DeviceDetectionResult,
)

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
    "RoutingMode",
    "DeviceDetectionResult",
]
