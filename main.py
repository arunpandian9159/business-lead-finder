"""Lead Finder + WhatsApp Outreach — CLI Entry Point.

Usage:
    python main.py
    python main.py --api-key YOUR_GEOAPIFY_KEY
    python main.py --location "Puducherry" --radius 5 --max-leads 50
    python main.py --skip-enrichment
"""

import argparse
import sys
from datetime import date

from src.config import (
    DEFAULT_LAT, 
    DEFAULT_LOCATION,
    DEFAULT_LON,
    DEFAULT_RADIUS_KM,
    GEOAPIFY_API_KEY,
    MAX_LEADS,
)
from src.discovery import search_businesses
from src.enrichment import enrich_all
from src.export import export_to_excel
from src.messaging import generate_all
from src.scoring import score_all
from src.utils import deduplicate_leads


def main():
    parser = argparse.ArgumentParser(
        description="🔍 Lead Finder + WhatsApp Outreach Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--api-key", default=None, help="Geoapify API key (defaults to .env)")
    parser.add_argument("--location", default=DEFAULT_LOCATION, help="Search location name")
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT, help="Latitude")
    parser.add_argument("--lon", type=float, default=DEFAULT_LON, help="Longitude")
    parser.add_argument("--radius", type=int, default=DEFAULT_RADIUS_KM, help="Search radius in km")
    parser.add_argument("--max-leads", type=int, default=MAX_LEADS, help="Max leads to collect")
    parser.add_argument("--skip-enrichment", action="store_true", help="Skip Google scraping")
    parser.add_argument("--output", default=None, help="Output filename (auto-generated if not set)")

    args = parser.parse_args()

    api_key = args.api_key or GEOAPIFY_API_KEY
    if not api_key:
        print("❌ No API key provided. Set GEOAPIFY_API_KEY in .env or pass --api-key.")
        sys.exit(1)

    print("=" * 60)
    print("  🔍 LEAD FINDER + WHATSAPP OUTREACH GENERATOR")
    print("=" * 60)
    print(f"  📍 Location  : {args.location} ({args.lat}, {args.lon})")
    print(f"  📏 Radius    : {args.radius} km")
    print(f"  📊 Max Leads : {args.max_leads}")
    print("=" * 60)

    # Phase 1: Discovery
    businesses = search_businesses(
        api_key=api_key,
        lat=args.lat,
        lon=args.lon,
        radius_km=args.radius,
        max_leads=args.max_leads,
    )

    if not businesses:
        print("\n❌ No businesses found. Check your API key and location.")
        sys.exit(1)

    # Phase 2: Deduplication
    businesses = deduplicate_leads(businesses)
    print(f"\n🧹 After deduplication: {len(businesses)} unique businesses")

    # Phase 3: Enrichment (optional)
    if not args.skip_enrichment:
        businesses = enrich_all(businesses)
    else:
        print("\n⏩ Skipping Google enrichment (--skip-enrichment flag)")
        for biz in businesses:
            biz.setdefault("google_rating", "")
            biz.setdefault("review_count", 0)
            biz.setdefault("claimed", "Unknown")
            biz.setdefault("google_maps_link", "")
            biz.setdefault("instagram", "")
            biz.setdefault("facebook", "")

    # Phase 4: Scoring
    businesses = score_all(businesses)

    # Phase 5: Message Generation
    businesses = generate_all(businesses)

    # Phase 6: Excel Export
    filename = args.output or f"leads_{args.location.lower().replace(' ', '_')}_{date.today().isoformat()}.xlsx"
    export_to_excel(businesses, args.location, filename)

    # Final Summary
    total = len(businesses)
    hot = sum(1 for b in businesses if b.get("lead_status") == "HOT")
    warm = sum(1 for b in businesses if b.get("lead_status") == "WARM")
    cold = sum(1 for b in businesses if b.get("lead_status") == "COLD")
    wa_ready = sum(1 for b in businesses if b.get("wa_link", "").startswith("https://"))
    missing = sum(1 for b in businesses if b.get("wa_link") == "PHONE MISSING")

    top_5 = [b for b in businesses if b.get("lead_status") == "HOT"][:5]

    print("\n" + "=" * 60)
    print("  ✅ FINAL SUMMARY")
    print("=" * 60)
    print(f"  ✅ Leads Found           : {total} businesses")
    print(f"  ✅ Hot Leads (8-10)      : {hot} businesses")
    print(f"  ✅ Warm Leads (5-7)      : {warm} businesses")
    print(f"  ✅ Cold Leads (1-4)      : {cold} businesses")
    print(f"  ✅ WA Messages Generated : {total} messages")
    print(f"  ✅ WA Links Ready        : {wa_ready} clickable links")
    print(f"  ⚠️  Missing Phone Numbers : {missing} (highlighted orange in sheet)")
    print(f"  📁 File Created          : {filename}")
    print(f"  📍 Location Covered      : {args.location}")
    print()

    if top_5:
        print("  🏆 Top 5 Businesses to Contact RIGHT NOW:")
        for i, biz in enumerate(top_5, 1):
            name = biz.get("name", "?")
            phone = biz.get("phone_normalized", "N/A")
            score = biz.get("priority_score", 0)
            print(f"    {i}. {name} — {phone} — Score: {score}")

    print("\n" + "=" * 60)
    print("  Done! Open the Excel file to start reaching out. 🚀")
    print("=" * 60)


if __name__ == "__main__":
    main()
