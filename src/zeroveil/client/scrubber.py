"""Thin Presidio wrapper for PII scrubbing.

Simple scrub() function using Microsoft Presidio for PII detection.
All logic is kept minimal - server handles any advanced processing.

Install: pip install zeroveil[pii]
"""

from dataclasses import dataclass
from typing import List, Optional

# Lazy load presidio to avoid import errors if not installed
_analyzer = None
_anonymizer = None


@dataclass
class ScrubResult:
    """Result of PII scrubbing."""
    text: str
    entities_found: int


def _get_analyzer():
    """Lazy-load Presidio analyzer."""
    global _analyzer
    if _analyzer is None:
        try:
            from presidio_analyzer import AnalyzerEngine
            _analyzer = AnalyzerEngine()
        except ImportError:
            raise ImportError(
                "Presidio not installed. Install with: pip install zeroveil[pii]"
            )
    return _analyzer


def _get_anonymizer():
    """Lazy-load Presidio anonymizer."""
    global _anonymizer
    if _anonymizer is None:
        try:
            from presidio_anonymizer import AnonymizerEngine
            _anonymizer = AnonymizerEngine()
        except ImportError:
            raise ImportError(
                "Presidio not installed. Install with: pip install zeroveil[pii]"
            )
    return _anonymizer


def scrub(text: str, language: str = "en") -> ScrubResult:
    """Scrub PII from text using Presidio.

    Detects and replaces standard entity types:
    - PERSON (names)
    - EMAIL_ADDRESS
    - PHONE_NUMBER
    - CREDIT_CARD
    - US_SSN
    - IP_ADDRESS
    - URL
    - LOCATION

    Args:
        text: Text to scrub
        language: Language code (default: "en")

    Returns:
        ScrubResult with scrubbed text and count of entities found

    Example:
        result = scrub("Contact John at john@example.com")
        # result.text == "Contact <PERSON> at <EMAIL_ADDRESS>"
        # result.entities_found == 2
    """
    if not text:
        return ScrubResult(text="", entities_found=0)

    analyzer = _get_analyzer()
    anonymizer = _get_anonymizer()

    # Analyze for PII
    results = analyzer.analyze(text=text, language=language)

    if not results:
        return ScrubResult(text=text, entities_found=0)

    # Anonymize (replace with entity type labels)
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)

    return ScrubResult(
        text=anonymized.text,
        entities_found=len(results)
    )


def is_available() -> bool:
    """Check if Presidio is installed and available."""
    try:
        from presidio_analyzer import AnalyzerEngine  # noqa: F401
        from presidio_anonymizer import AnonymizerEngine  # noqa: F401
        return True
    except ImportError:
        return False
