# ZeroVeil SDK

Privacy-first client library for LLM interactions.

## Overview

ZeroVeil SDK provides client-side tools for privacy-preserving LLM usage:

- **PII Scrubbing**: Remove personally identifiable information before sending prompts
- **Relay Client**: Connect to ZeroVeil privacy relay for provider-side anonymity
- **Device Detection**: Automatic routing optimization based on client capabilities

## Installation

```bash
pip install zeroveil
```

## Quick Start

```python
from zeroveil import scrub, send

# Scrub PII from your prompt
clean_prompt = scrub("My SSN is 123-45-6789 and I need help with...")

# Send through ZeroVeil relay
response = send(clean_prompt)
```

## Features

### Basic PII Scrubbing

Uses Presidio for detecting and removing:
- Social Security Numbers
- Credit Card Numbers
- Email Addresses
- Phone Numbers
- Names and Addresses

### Relay Client

Connect to ZeroVeil privacy relay for provider-side anonymity:

```python
from zeroveil.client import ZeroVeilClient

client = ZeroVeilClient(relay_url="https://relay.zeroveil.io")
response = client.send(prompt, model="claude-3-sonnet")
```

## Pro Tier

Advanced features available with ZeroVeil Pro:

- Deterministic/non-deterministic scrubbing modes
- Reversible token mapping (restore original text)
- Multiple scrubbing backends
- Audit logging

Contact: Saqib.Khan@Me.com

## Documentation

See [Cortex1-ZeroVeil](https://github.com/Free-Radical/Cortex1-ZeroVeil) for full architecture documentation.

## License

Business Source License 1.1 — See [LICENSE](LICENSE) for details.

## Author

Saqib Ali Khan