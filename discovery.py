"""Geoapify Places API integration for business discovery."""

import httpx
from config import (
    CATEGORIES,
    DEFAULT_LAT,
    DEFAULT_LON,
    DEFAULT_RADIUS_KM,
    EXPANDED_RADIUS_KM,
    MAX_LEADS,
    MIN_RESULTS_BEFORE_EXPAND,
)
from utils import is_chain_or_franchise

GEOAPIFY_BASE = "https://api.geoapify.com/v2/places"


def search_businesses(
    api_key: str,
    lat: float = DEFAULT_LAT,
    lon: float = DEFAULT_LON,
    radius_km: int = DEFAULT_RADIUS_KM,
    max_leads: int = MAX_LEADS,
) -> list[dict]:
    """Search for businesses across all categories using Geoapify Places API.

    Auto-expands radius to EXPANDED_RADIUS_KM if fewer than MIN_RESULTS_BEFORE_EXPAND found.
    """
    all_results = []
    radius_m = radius_km * 1000

    print(f"\n🔍 Searching businesses within {radius_km}km of ({lat}, {lon})...")

    for cat_key, cat_info in CATEGORIES.items():
        geoapify_cats = cat_info["geoapify"]
        results = _fetch_category(api_key, geoapify_cats, lat, lon, radius_m, cat_key)
        all_results.extend(results)
        print(f"  ✓ {cat_key}: found {len(results)} businesses")

    if len(all_results) < MIN_RESULTS_BEFORE_EXPAND and radius_km < EXPANDED_RADIUS_KM:
        print(f"\n⚡ Only {len(all_results)} results. Expanding to {EXPANDED_RADIUS_KM}km...")
        all_results = []
        radius_m = EXPANDED_RADIUS_KM * 1000
        for cat_key, cat_info in CATEGORIES.items():
            geoapify_cats = cat_info["geoapify"]
            results = _fetch_category(api_key, geoapify_cats, lat, lon, radius_m, cat_key)
            all_results.extend(results)
            print(f"  ✓ {cat_key}: found {len(results)} businesses")

    all_results = all_results[:max_leads]
    print(f"\n📊 Total businesses collected: {len(all_results)}")
    return all_results


def _fetch_category(
    api_key: str,
    categories: str,
    lat: float,
    lon: float,
    radius_m: int,
    category_key: str,
) -> list[dict]:
    """Fetch businesses for a single Geoapify category group."""
    params = {
        "categories": categories,
        "filter": f"circle:{lon},{lat},{radius_m}",
        "bias": f"proximity:{lon},{lat}",
        "limit": 50,
        "apiKey": api_key,
    }

    try:
        resp = httpx.get(GEOAPIFY_BASE, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPStatusError as e:
        print(f"  ⚠ API error for {category_key}: {e.response.status_code}")
        return []
    except httpx.RequestError as e:
        print(f"  ⚠ Network error for {category_key}: {e}")
        return []

    businesses = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        name = props.get("name", "").strip()

        if not name:
            continue
        if is_chain_or_franchise(name):
            continue

        business = {
            "name": name,
            "category": category_key,
            "category_label": CATEGORIES[category_key]["label"],
            "phone": props.get("contact", {}).get("phone", "")
                     or props.get("datasource", {}).get("raw", {}).get("phone", ""),
            "email": props.get("contact", {}).get("email", ""),
            "address": props.get("formatted", ""),
            "locality": props.get("suburb", "")
                        or props.get("district", "")
                        or props.get("city", ""),
            "lat": props.get("lat", ""),
            "lon": props.get("lon", ""),
            "website": props.get("website", "")
                       or props.get("datasource", {}).get("raw", {}).get("website", ""),
            "has_website": bool(
                props.get("website")
                or props.get("datasource", {}).get("raw", {}).get("website")
            ),
            "high_revenue": CATEGORIES[category_key]["high_revenue"],
        }
        businesses.append(business)

    return businesses
