"""Utility functions: phone normalization, URL encoding, deduplication."""

import re
from urllib.parse import quote


def normalize_phone(raw: str) -> str:
    """Normalize an Indian phone number to 91XXXXXXXXXX format.

    Handles formats like:
      +91 80723 96488, 091-8072396488, 8072396488, 08072396488
    Returns empty string if phone can't be normalized.
    """
    if not raw:
        return ""

    digits = re.sub(r"\D", "", raw)

    if digits.startswith("91") and len(digits) == 12:
        return digits
    if digits.startswith("0") and len(digits) == 11:
        return "91" + digits[1:]
    if len(digits) == 10:
        return "91" + digits
    if digits.startswith("091") and len(digits) == 13:
        return "91" + digits[3:]

    return digits if len(digits) >= 10 else ""


def build_wa_link(phone: str, message: str) -> str:
    """Build a clickable wa.me link with pre-filled message.

    Phone must be in 91XXXXXXXXXX format.
    """
    if not phone:
        return "PHONE MISSING"
    encoded = quote(message, safe="")
    return f"https://wa.me/{phone}?text={encoded}"


def deduplicate_leads(leads: list[dict]) -> list[dict]:
    """Remove duplicate businesses by (phone, name) pair."""
    seen = set()
    unique = []
    for lead in leads:
        key = (
            lead.get("phone", "").strip(),
            lead.get("name", "").strip().lower(),
        )
        if key == ("", ""):
            unique.append(lead)
            continue
        if key not in seen:
            seen.add(key)
            unique.append(lead)
    return unique


def is_chain_or_franchise(name: str) -> bool:
    """Basic check to skip known chains/franchises."""
    chains = [
        "mcdonald", "kfc", "domino", "pizza hut", "subway", "starbucks",
        "burger king", "dunkin", "baskin robbins", "haldiram", "barbeque nation",
        "cafe coffee day", "ccd", "naturals", "jawed habib", "lakme salon",
        "apollo", "fortis", "manipal", "max hospital", "reliance",
        "big bazaar", "dmart", "more supermarket", "spencer", "heritage",
    ]
    name_lower = name.lower()
    return any(chain in name_lower for chain in chains)
