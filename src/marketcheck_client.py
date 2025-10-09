import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

import requests


API_BASE_URL = "https://marketcheck-prod.apigee.net/v2"
DEFAULT_TIMEOUT = 20  # seconds


class MarketCheckAuthError(RuntimeError):
    """Raised when the MarketCheck API key is missing."""


class MarketCheckClientError(RuntimeError):
    """Raised when the MarketCheck API request fails."""


def _coerce_int(value: Any) -> Optional[int]:
    try:
        if value is None or value == "":
            return None
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _coerce_float(value: Any) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _extract_listing_date(listing: Dict[str, Any]) -> Optional[str]:
    for key in ("list_date", "listing_date", "scraped_at", "first_seen_at"):
        value = listing.get(key)
        if value:
            return str(value)
    return None


@dataclass
class MarketCheckClient:
    """Thin HTTP client for the MarketCheck Inventory API."""

    api_key: Optional[str] = None
    base_url: str = API_BASE_URL
    timeout: int = DEFAULT_TIMEOUT

    def __post_init__(self) -> None:
        if not self.api_key:
            self.api_key = os.getenv("MARKETCHECK_API_KEY")
        if not self.api_key:
            raise MarketCheckAuthError(
                "MARKETCHECK_API_KEY is required. Set it in your environment or .env file."
            )

    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a GET request and return the parsed JSON payload."""
        if not path.startswith("/"):
            path = f"/{path}"
        query: Dict[str, Any] = {"api_key": self.api_key}
        if params:
            query.update({k: v for k, v in params.items() if v is not None})

        try:
            response = requests.get(
                f"{self.base_url}{path}",
                params=query,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise MarketCheckClientError(f"MarketCheck request failed: {exc}") from exc

        if response.status_code >= 400:
            raise MarketCheckClientError(
                f"MarketCheck returned {response.status_code}: {response.text}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise MarketCheckClientError("MarketCheck response was not valid JSON") from exc

    def search_active(self, **params: Any) -> Dict[str, Any]:
        """Convenience wrapper for the /v2/search/car/active endpoint."""
        return self.get_json("/search/car/active", params=params)


def normalize_listing(listing: Dict[str, Any]) -> Dict[str, Any]:
    """Project a raw MarketCheck listing into a normalized structure."""
    dealer = listing.get("dealer") or {}
    location = dealer.get("location") or {}

    normalized: Dict[str, Any] = {
        "vin": _clean_str(listing.get("vin")),
        "dealer_name": _clean_str(dealer.get("name")),
        "city": _clean_str(dealer.get("city") or location.get("city")),
        "state": _clean_str(dealer.get("state") or location.get("state")),
        "price": _coerce_float(listing.get("price") or listing.get("pricing", {}).get("sale_price")),
        "miles": _coerce_int(listing.get("miles")),
        "dom": _coerce_int(listing.get("dom")),
        "vdp_url": _clean_str(listing.get("vdp_url") or listing.get("vdp")),
        "listing_date": _extract_listing_date(listing),
    }

    return normalized


def normalize_listings(listings: Iterable[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """Normalize a sequence of listings."""
    return [normalize_listing(item) for item in listings]
