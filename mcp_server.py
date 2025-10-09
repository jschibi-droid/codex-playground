import asyncio
from typing import Any, Dict, Optional

from mcp.server import FastMCP

from src.marketcheck_client import (
    MarketCheckAuthError,
    MarketCheckClient,
    MarketCheckClientError,
    normalize_listings,
)
from src.reporting import summarize_listings


server = FastMCP("dealership", instructions="MarketCheck inventory helper")


def _build_client() -> MarketCheckClient:
    try:
        return MarketCheckClient()
    except MarketCheckAuthError as exc:
        raise RuntimeError(str(exc)) from exc


@server.tool(
    name="mc_comp_search",
    description="Search MarketCheck active inventory for a specific year/make/model trim.",
)
async def mc_comp_search(
    year: int,
    make: str,
    model: str,
    trim: Optional[str] = None,
    zip: Optional[str] = None,
    radius: int = 100,
    rows: int = 200,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
) -> Dict[str, Any]:
    client = _build_client()
    params: Dict[str, Any] = {
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
        "zip": zip,
        "radius": radius,
        "rows": rows,
        "price_min": price_min,
        "price_max": price_max,
    }
    try:
        response = client.search_active(**params)
    except MarketCheckClientError as exc:
        raise RuntimeError(f"MarketCheck search failed: {exc}") from exc

    listings_raw = response.get("listings", [])
    listings = normalize_listings(listings_raw)
    summary = summarize_listings(listings)

    return {
        "summary": {
            "count": summary["count"],
            "price_avg": summary["price_avg"],
            "price_min": summary["price_min"],
            "price_max": summary["price_max"],
        },
        "listings": listings,
    }


@server.tool(
    name="mc_market_competition",
    description="Attempt to call MarketCheck market competition endpoints.",
)
async def mc_market_competition(
    year: int,
    make: str,
    model: str,
    trim: Optional[str] = None,
    zip: Optional[str] = None,
    radius: int = 100,
) -> Dict[str, Any]:
    client = _build_client()
    params = {
        "year": year,
        "make": make,
        "model": model,
        "trim": trim,
        "zip": zip,
        "radius": radius,
    }
    try:
        # Market endpoints are plan-dependent. Keep the call defensive.
        return client.get_json("/market/competitors", params=params)
    except MarketCheckClientError:
        return {"message": "market endpoints not enabled"}


def main() -> None:
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
