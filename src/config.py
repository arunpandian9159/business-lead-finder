"""Configuration and constants for the Lead Finder tool."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ═══════════════════════════════════════════
# USER DETAILS (from .env)
# ═══════════════════════════════════════════
USER_NAME = os.getenv("USER_NAME", "Arunpandian")
USER_PHONE = os.getenv("USER_PHONE", "918072396488")

# ═══════════════════════════════════════════
# API KEY (from .env)
# ═══════════════════════════════════════════
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY", "")

# ═══════════════════════════════════════════
# LOCATION (from .env) 
# ═══════════════════════════════════════════
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Puducherry")
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", "11.9416"))
DEFAULT_LON = float(os.getenv("DEFAULT_LON", "79.8083"))
DEFAULT_RADIUS_KM = int(os.getenv("DEFAULT_RADIUS_KM", "50"))
EXPANDED_RADIUS_KM = 100
MIN_RESULTS_BEFORE_EXPAND = 20
MAX_LEADS = 100

# ═══════════════════════════════════════════
# GEOAPIFY CATEGORIES
# Ref: https://apidocs.geoapify.com/docs/places/#categories
# ═══════════════════════════════════════════
CATEGORIES = {
    "Restaurant": {
        "geoapify": "catering.restaurant,catering.fast_food,catering.cafe",
        "label": "Restaurant / Dhaba / Bakery / Food",
        "high_revenue": True,
    },
    "Bakery": {
        "geoapify": "commercial.food_and_drink.bakery",
        "label": "Bakery",
        "high_revenue": False,
    },
    "Salon": {
        "geoapify": "service.beauty.hairdresser,service.beauty.spa,service.beauty",
        "label": "Salon / Spa / Barbershop / Beauty",
        "high_revenue": True,
    },
    "Clinic": {
        "geoapify": "healthcare.clinic_or_praxis,healthcare.dentist,healthcare.hospital",
        "label": "Clinic / Doctor / Dental / Medical Lab",
        "high_revenue": True,
    },
    "Coaching": {
        "geoapify": "education.school,education.training,education.college",
        "label": "Coaching / Tuition / Education / Training",
        "high_revenue": False,
    },
    "Hardware": {
        "geoapify": "commercial.hardware_and_tools,commercial.building_materials_and_supplies",
        "label": "Hardware / Building Material",
        "high_revenue": False,
    },
    "Auto Repair": {
        "geoapify": "service.vehicle.repair,service.vehicle.car_wash",
        "label": "Auto Repair / Car Wash",
        "high_revenue": False,
    },
    "Grocery": {
        "geoapify": "commercial.supermarket,commercial.convenience,commercial.marketplace",
        "label": "Grocery / Kirana / General Store",
        "high_revenue": False,
    },
    "Plumber / Electrician": {
        "geoapify": "service",
        "label": "Plumber / Electrician / Carpenter",
        "high_revenue": False,
    },
    "Pest Control": {
        "geoapify": "service.cleaning",
        "label": "Pest Control / Cleaning / Home Services",
        "high_revenue": False,
    },
    "Event Decorator": {
        "geoapify": "entertainment.event_service",
        "label": "Event Decorator / Caterer / Wedding Planner",
        "high_revenue": False,
    },
    "Photographer": {
        "geoapify": "service.photography",
        "label": "Photographer / Videographer",
        "high_revenue": False,
    },
}

# ═══════════════════════════════════════════
# SCORING WEIGHTS
# ═══════════════════════════════════════════
SCORE_NO_WEBSITE = 4
SCORE_UNCLAIMED = 2
SCORE_FEW_REVIEWS = 1
SCORE_NO_SOCIAL = 2
SCORE_HIGH_REVENUE = 1
REVIEW_THRESHOLD = 20

HOT_MIN = 8
WARM_MIN = 5
