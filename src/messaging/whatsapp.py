"""WhatsApp message templates and generator for each business category."""

from src.config import USER_NAME
from src.utils import build_wa_link, normalize_phone

# ═══════════════════════════════════════════
# MESSAGE TEMPLATES — keyed by category
# ═══════════════════════════════════════════

TEMPLATES = {
    "Restaurant": {
        "short": "Hi {name}! 👋 Noticed you don't have a website. I build affordable restaurant sites with menu, photos & contact. Free demo? — {user}",
        "full": """Hi {name} Team! 👋

I noticed your restaurant doesn't have a website yet. Most customers search Google before deciding where to eat — and without a website, you might be losing them to nearby competitors.

I build affordable websites for local restaurants that display your menu, location, photos, and contact — helping you get more walk-ins and online orders consistently.

A good website also helps you show up in "best restaurants near me" searches, which means free marketing 24/7. Your Google listing already gets views — imagine how many more customers you'd convert with a professional site.

Can I show you a quick free demo? Takes just 10 minutes and there's no obligation at all. 😊

— {user}""",
    },
    "Bakery": {
        "short": "Hi {name}! 👋 A website with your menu & prices can bring more customers daily. I build bakery sites affordably. Quick demo? — {user}",
        "full": """Hi {name} Team! 👋

I noticed your bakery doesn't have a website yet. Most customers search Google before deciding where to eat — and without a website, you might be losing them to nearby competitors.

I build affordable websites for local bakeries that display your products, pricing, photos, and contact — helping you get more walk-ins and online orders consistently.

A website with your daily specials, cake catalogue, and order options can turn Google searchers into loyal customers. People in {locality} are searching right now!

Can I show you a quick free demo? Takes just 10 minutes and there's no obligation at all. 😊

— {user}""",
    },
    "Salon": {
        "short": "Hi {name}! 👋 People search 'best salon near me' daily. A website helps you get found & booked. Free demo? — {user}",
        "full": """Hi {name}! 👋

People search "best salon near me" on Google before booking. Without a website, your salon might not even show up in those searches — meaning you're missing bookings every single day.

I create beautiful, simple websites for salons that show your services, pricing, photos, and allow customers to book appointments directly. It's like having a 24/7 receptionist working for you.

Your work speaks for itself — a website just makes sure more people in {locality} actually see it.

Would love to show you a free demo for {name} — no pressure at all! 💼

— {user}""",
    },
    "Clinic": {
        "short": "Hello {name}! 👋 Patients search online before choosing a doctor. A website builds trust instantly. Quick chat? — {user}",
        "full": """Hello {name} 👋

Patients today search online before choosing a doctor or clinic. A professional website builds trust instantly and helps new patients find you easily — especially urgent cases searching nearby.

I help local clinics go online with a clean website showing specializations, timings, location, and contact — fully secure and professional. It also helps you appear in "clinic near me" and "{locality} doctor" searches.

Your reputation is already strong — a website simply makes it visible to the thousands of people searching online every month.

Can we connect for a quick 10-minute call? 🙏

— {user}""",
    },
    "Coaching": {
        "short": "Hi {name}! 👋 Parents search online for classes. Without a website, students go elsewhere. Free demo? — {user}",
        "full": """Hi {name} Team! 👋

Parents and students always search online when looking for coaching classes. Without a website, you're invisible to a huge number of potential students searching right now in {locality}.

I build clean, simple websites for coaching centers — showing subjects, batch timings, fees, faculty, and results — that generate steady new student inquiries.

A website also lets you share announcements, exam schedules, and results — making communication with parents much easier.

Happy to show you a free demo this week! 📚

— {user}""",
    },
    "Hardware": {
        "short": "Hi {name}! 👋 Customers Google for supplies before visiting. A simple website gets you found daily. Free chat? — {user}",
        "full": """Hi {name}! 👋

When someone needs an urgent repair or hardware supply, they Google it first. A simple website with your services, location, and phone number can bring you new customers every single month — even while you sleep.

I make affordable websites for local service businesses — quick to build, easy to manage, and optimized for local Google search. When people in {locality} search for supplies, your shop should be the first result.

Interested in a free quick chat? 🔧

— {user}""",
    },
    "Auto Repair": {
        "short": "Hi {name}! 👋 People Google 'car repair near me' when stuck. A website gets you those urgent calls. Demo? — {user}",
        "full": """Hi {name}! 👋

When someone needs an urgent repair or car service, they Google it first. A simple website with your services, location, and phone number can bring you new customers every single month — even while you sleep.

I make affordable websites for local auto service businesses — quick to build, easy to manage, and optimized for local Google search. People searching "car repair near me" in {locality} could be calling you!

Interested in a free quick chat? 🔧

— {user}""",
    },
    "Grocery": {
        "short": "Hi {name}! 👋 Customers search online before stepping out. A simple site brings more daily orders. Free demo? — {user}",
        "full": """Hi {name}! 👋

More customers are searching online even for nearby stores before stepping out. A simple website or WhatsApp order page can help you reach more people in {locality} and increase your daily order volume.

I create budget-friendly websites for local stores — simple, fast, and built to bring in more customers from your own neighborhood. It can include your product list, delivery options, and direct WhatsApp ordering.

Want to see how it works? Free demo! 🛒

— {user}""",
    },
    "Plumber / Electrician": {
        "short": "Hi {name}! 👋 People Google for services urgently. A website with your number gets you calls daily. Chat? — {user}",
        "full": """Hi {name}! 👋

When someone needs an urgent repair — plumbing, electrical, carpentry — they Google it first. A simple website with your services, location, and phone number can bring you new customers every single month — even while you sleep.

I make affordable websites for local service providers — quick to build, easy to manage, and optimized for local Google search. When people in {locality} search for help, you should be the first result.

Interested in a free quick chat? 🔧

— {user}""",
    },
    "Pest Control": {
        "short": "Hi {name}! 👋 People Google 'pest control near me' urgently. Without a website, you're invisible. Free demo? — {user}",
        "full": """Hi {name}! 👋

Most people search "pest control near me" or "home cleaning {locality}" on Google when they need help urgently. Without a website, you're invisible to all of those searches happening right now in {locality}.

I build affordable local service websites that show your services, coverage area, pricing, and contact — getting you discovered daily by people who need your help right now.

Want a quick free demo? 🏠

— {user}""",
    },
    "Event Decorator": {
        "short": "Hi {name}! 👋 Families browse online for decorators. A portfolio site gets you direct bookings. Demo? — {user}",
        "full": """Hi {name} Team! 👋

Couples and families planning events spend hours browsing online for decorators and caterers. Without a website showing your best work, you're missing bookings that go straight to competitors who are online.

I build portfolio websites for event businesses that showcase your photos, packages, pricing, and bring in direct inquiries — no middleman. Your work is stunning — a website just makes sure more people see it.

Can I show you a sample in 10 minutes? 🎊

— {user}""",
    },
    "Photographer": {
        "short": "Hi {name}! 👋 Clients Google photographers first. A portfolio website gets you direct bookings weekly. Demo? — {user}",
        "full": """Hi {name}! 👋

Clients always Google photographers before reaching out. Without a portfolio website, your best work is invisible — and potential clients simply move on to someone else.

I create stunning portfolio websites for photographers that showcase your work, list your packages, and get you direct booking inquiries every week. Your skill deserves to be seen by everyone searching in {locality}.

Happy to show you a free sample demo! 📸

— {user}""",
    },
}


def generate_messages(business: dict) -> dict:
    """Generate short message, full message, and wa.me link for a business.

    Returns the business dict with added keys: 
      wa_short, wa_full, wa_link
    """
    category = business.get("category", "")
    name = business.get("name", "Unknown Business")
    locality = business.get("locality", "your area")
    phone = normalize_phone(business.get("phone", ""))

    template = TEMPLATES.get(category, TEMPLATES.get("Hardware"))

    fmt = {"name": name, "locality": locality, "user": USER_NAME}

    short = template["short"].format(**fmt)
    if len(short) > 200:
        short = short[:197] + "..."

    full = template["full"].format(**fmt)

    business["wa_short"] = short
    business["wa_full"] = full
    business["wa_link"] = build_wa_link(phone, short)
    business["phone_normalized"] = phone

    return business


def generate_all(businesses: list[dict]) -> list[dict]:
    """Generate WhatsApp messages for all businesses."""
    print(f"\n💬 Generating WhatsApp messages for {len(businesses)} businesses...")
    for biz in businesses:
        generate_messages(biz)

    ready = sum(1 for b in businesses if b.get("wa_link", "").startswith("https://"))
    missing = sum(1 for b in businesses if b.get("wa_link") == "PHONE MISSING")
    print(f"  ✓ Messages generated: {ready} ready | {missing} missing phone")

    return businesses
