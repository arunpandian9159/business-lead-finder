"""Quick verification test for the lead finder pipeline."""

from messages import generate_messages
from scoring import calculate_score, get_lead_status
from excel_export import export_to_excel

# Test 1: Message generation
biz1 = {
    "name": "Ravi Salon",
    "category": "Salon",
    "category_label": "Salon / Spa / Barbershop / Beauty",
    "phone": "9876543210",
    "locality": "MG Road",
    "has_website": False,
    "claimed": "No",
    "review_count": 5,
    "instagram": "",
    "facebook": "",
    "high_revenue": True,
    "email": "",
    "address": "123 MG Road, Puducherry",
    "google_maps_link": "",
    "website": "",
    "google_rating": "4.2",
}

biz2 = {
    "name": "Kumar Clinic",
    "category": "Clinic",
    "category_label": "Clinic / Doctor / Dental / Medical Lab",
    "phone": "+91 98765 43211",
    "locality": "White Town",
    "has_website": True,
    "claimed": "Yes",
    "review_count": 50,
    "instagram": "https://instagram.com/kumarclinic",
    "facebook": "",
    "high_revenue": True,
    "email": "kumar@clinic.com",
    "address": "45 White Town, Puducherry",
    "google_maps_link": "",
    "website": "https://kumarclinic.com",
    "google_rating": "4.5",
}

biz3 = {
    "name": "Pondy Hardware",
    "category": "Hardware",
    "category_label": "Hardware / Building Material",
    "phone": "",
    "locality": "Lawspet",
    "has_website": False,
    "claimed": "Unknown",
    "review_count": 3,
    "instagram": "",
    "facebook": "",
    "high_revenue": False,
    "email": "",
    "address": "78 Lawspet, Puducherry",
    "google_maps_link": "",
    "website": "",
    "google_rating": "",
}

businesses = [biz1, biz2, biz3]

print("=== Test 1: Scoring ===")
for biz in businesses:
    biz["priority_score"] = calculate_score(biz)
    biz["lead_status"] = get_lead_status(biz["priority_score"])
    print(f"  {biz['name']}: Score={biz['priority_score']}, Status={biz['lead_status']}")

print("\n=== Test 2: Messages ===")
for biz in businesses:
    generate_messages(biz)
    short_len = len(biz["wa_short"])
    print(f"  {biz['name']}: short={short_len} chars, link={biz['wa_link'][:50]}...")

print("\n=== Test 3: Excel Export ===")
filename = "test_output.xlsx"
export_to_excel(businesses, "Puducherry", filename)
print(f"  File created: {filename}")

print("\n✅ All tests passed!")
