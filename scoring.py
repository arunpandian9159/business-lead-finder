"""Priority scoring and lead status classification."""

from config import (
    HOT_MIN,
    REVIEW_THRESHOLD,
    SCORE_FEW_REVIEWS,
    SCORE_HIGH_REVENUE,
    SCORE_NO_SOCIAL,
    SCORE_NO_WEBSITE,
    SCORE_UNCLAIMED,
    WARM_MIN,
)


def calculate_score(business: dict) -> int:
    """Calculate priority score (1-10) for a business."""
    score = 0

    if not business.get("has_website"):
        score += SCORE_NO_WEBSITE

    if business.get("claimed", "").lower() in ("no", "unknown", ""):
        score += SCORE_UNCLAIMED

    review_count = business.get("review_count", 0)
    if review_count < REVIEW_THRESHOLD:
        score += SCORE_FEW_REVIEWS

    has_social = bool(business.get("instagram") or business.get("facebook"))
    if not has_social:
        score += SCORE_NO_SOCIAL

    if business.get("high_revenue"):
        score += SCORE_HIGH_REVENUE

    return min(score, 10)


def get_lead_status(score: int) -> str:
    """Return lead status based on priority score."""
    if score >= HOT_MIN:
        return "HOT"
    if score >= WARM_MIN:
        return "WARM"
    return "COLD"


def score_all(businesses: list[dict]) -> list[dict]:
    """Calculate scores and statuses for all businesses, sort by score descending."""
    for biz in businesses:
        biz["priority_score"] = calculate_score(biz)
        biz["lead_status"] = get_lead_status(biz["priority_score"])

    businesses.sort(key=lambda b: b["priority_score"], reverse=True)

    hot = sum(1 for b in businesses if b["lead_status"] == "HOT")
    warm = sum(1 for b in businesses if b["lead_status"] == "WARM")
    cold = sum(1 for b in businesses if b["lead_status"] == "COLD")
    print(f"\n📈 Scoring complete: 🔴 HOT={hot} | 🟡 WARM={warm} | 🟢 COLD={cold}")

    return businesses
