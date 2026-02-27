"""Google Maps scraping for enrichment data (rating, reviews, claimed status, social links)."""

import re
import time

import httpx
from bs4 import BeautifulSoup

GOOGLE_SEARCH_URL = "https://www.google.com/search"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def enrich_business(business: dict) -> dict:
    """Enrich a business dict with Google Maps data.

    Adds: google_rating, review_count, claimed, google_maps_link,
          instagram, facebook.
    """
    name = business.get("name", "")
    locality = business.get("locality", "")
    category = business.get("category_label", "")

    business.setdefault("google_rating", "")
    business.setdefault("review_count", 0)
    business.setdefault("claimed", "Unknown")
    business.setdefault("google_maps_link", "")
    business.setdefault("instagram", "")
    business.setdefault("facebook", "")

    if not name:
        return business

    maps_link = _build_maps_link(name, locality)
    business["google_maps_link"] = maps_link

    try:
        data = _scrape_google_search(name, locality, category)
        business["google_rating"] = data.get("rating", "")
        business["review_count"] = data.get("review_count", 0)
        business["claimed"] = data.get("claimed", "Unknown")
        business["instagram"] = data.get("instagram", "")
        business["facebook"] = data.get("facebook", "")

        if data.get("website") and not business.get("has_website"):
            business["website"] = data["website"]
            business["has_website"] = True

    except Exception as e:
        print(f"    ⚠ Enrichment failed for {name}: {e}")

    return business


def enrich_all(businesses: list[dict]) -> list[dict]:
    """Enrich all businesses with Google data. Adds a delay between requests."""
    total = len(businesses)
    print(f"\n🌐 Enriching {total} businesses via Google search...")

    for i, biz in enumerate(businesses, 1):
        print(f"  [{i}/{total}] {biz['name']}...", end=" ")
        enrich_business(biz)
        print("✓")
        if i < total:
            time.sleep(2)

    return businesses


def _build_maps_link(name: str, locality: str) -> str:
    """Build a Google Maps search link."""
    query = f"{name} {locality}".strip()
    encoded = query.replace(" ", "+")
    return f"https://www.google.com/maps/search/{encoded}"


def _scrape_google_search(name: str, locality: str, category: str) -> dict:
    """Scrape Google search results for business info.

    Returns a dict with: rating, review_count, claimed, website, instagram, facebook.
    """
    query = f"{name} {locality} {category}"
    result = {
        "rating": "",
        "review_count": 0,
        "claimed": "Unknown",
        "website": "",
        "instagram": "",
        "facebook": "",
    }

    try:
        resp = httpx.get(
            GOOGLE_SEARCH_URL,
            params={"q": query},
            headers=HEADERS,
            timeout=15,
            follow_redirects=True,
        )
        if resp.status_code != 200:
            return result

        html = resp.text
        soup = BeautifulSoup(html, "lxml")
        text = soup.get_text(" ", strip=True)

        rating_match = re.search(r"(\d\.?\d?)\s*(?:out of 5|/5|\u2605)", text)
        if rating_match:
            result["rating"] = rating_match.group(1)

        review_match = re.search(r"(\d[\d,]*)\s*(?:reviews?|Google reviews?)", text, re.IGNORECASE)
        if review_match:
            result["review_count"] = int(review_match.group(1).replace(",", ""))

        if "claim this business" in text.lower() or "unclaimed" in text.lower():
            result["claimed"] = "No"
        elif "claimed" in text.lower() or name.lower() in text.lower():
            result["claimed"] = "Yes"

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "instagram.com/" in href and not result["instagram"]:
                ig_match = re.search(r"instagram\.com/([^/?&]+)", href)
                if ig_match:
                    result["instagram"] = f"https://instagram.com/{ig_match.group(1)}"
            if "facebook.com/" in href and not result["facebook"]:
                fb_match = re.search(r"facebook\.com/([^/?&]+)", href)
                if fb_match:
                    result["facebook"] = f"https://facebook.com/{fb_match.group(1)}"

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if (
                "google" not in href
                and "youtube" not in href
                and "instagram" not in href
                and "facebook" not in href
                and "twitter" not in href
                and href.startswith("http")
            ):
                clean = re.sub(r"/url\?q=", "", href).split("&")[0]
                if "." in clean and len(clean) > 10:
                    result["website"] = clean
                    break

    except Exception:
        pass

    return result
