# Copyright © 2025 Saqib Ali Khan. All Rights Reserved.
# Licensed under Business Source License 1.1

"""Simple API client for ZeroVeil relay.

Minimal HTTP client with send/receive operations.
All routing, tier selection, and model decisions are server-side.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import time

import requests

from zeroveil.client.config import ZeroVeilConfig, load_config


@dataclass
class Response:
    """Response from ZeroVeil API."""
    content: str
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None


class ZeroVeilClient:
    """Simple client for ZeroVeil relay API.

    Usage:
        client = ZeroVeilClient()
        response = client.send("What is the capital of France?")
        print(response.content)
    """

    def __init__(self, config: Optional[ZeroVeilConfig] = None):
        """Initialize client.

        Args:
            config: Connection config. If None, loads from environment.
        """
        self.config = config or load_config()
        if not self.config.api_key:
            raise ValueError(
                "API key required. Set ZEROVEIL_API_KEY environment variable "
                "or pass config with api_key."
            )

    def send(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        zdr_only: bool = True,
        max_retries: int = 3,
    ) -> Response:
        """Send prompt to ZeroVeil relay.

        Args:
            prompt: User prompt/message (should be scrubbed of PII)
            system_prompt: Optional system prompt
            zdr_only: Only route to Zero Data Retention providers (default: True)
            max_retries: Retry count on network failure (default: 3)

        Returns:
            Response with content from relay

        Raises:
            requests.RequestException: On network failure after retries
            ValueError: On API error response
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return self._send_messages(messages, max_retries, zdr_only=zdr_only)

    def send_messages(
        self,
        messages: List[Dict[str, str]],
        zdr_only: bool = True,
        max_retries: int = 3,
    ) -> Response:
        """Send message list to ZeroVeil relay.

        Args:
            messages: List of {"role": "...", "content": "..."} dicts
            zdr_only: Only route to Zero Data Retention providers (default: True)
            max_retries: Retry count on network failure (default: 3)

        Returns:
            Response with content from relay
        """
        return self._send_messages(messages, max_retries, zdr_only=zdr_only)

    def _send_messages(
        self,
        messages: List[Dict[str, str]],
        max_retries: int,
        zdr_only: bool = True,
    ) -> Response:
        """Internal send with retry logic."""
        endpoint = f"{self.config.endpoint.rstrip('/')}/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }

        data = {
            "messages": messages,
            "zdr_only": zdr_only,
        }

        last_error = None
        for attempt in range(max_retries):
            try:
                resp = requests.post(
                    endpoint,
                    headers=headers,
                    json=data,
                    timeout=self.config.timeout,
                )
                resp.raise_for_status()

                payload = resp.json()

                # Extract response
                choices = payload.get("choices", [])
                if not choices:
                    raise ValueError("Empty response from API")

                content = choices[0].get("message", {}).get("content", "")

                return Response(
                    content=content,
                    usage=payload.get("usage"),
                    model=payload.get("model"),
                )

            except requests.RequestException as e:
                last_error = e
                if attempt < max_retries - 1:
                    # Exponential backoff
                    time.sleep(2 ** attempt)
                    continue
                raise

        raise last_error  # type: ignore


def create_client(config: Optional[ZeroVeilConfig] = None) -> ZeroVeilClient:
    """Create a ZeroVeil client.

    Args:
        config: Optional config. If None, loads from environment.

    Returns:
        Configured ZeroVeilClient instance
    """
    return ZeroVeilClient(config)
