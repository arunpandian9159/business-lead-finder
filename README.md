# 🔍 Lead Finder + WhatsApp Outreach Generator

> Discover local businesses without websites, generate personalized WhatsApp cold outreach messages, and export everything to a structured Excel file — ready to use.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with your Geoapify API key
python main.py --api-key YOUR_GEOAPIFY_KEY

# 3. Open the generated .xlsx file and start reaching out!
```

> **Need an API key?** Sign up free at [geoapify.com](https://www.geoapify.com/) → Create project → Copy key. Free tier gives 3,000 requests/day.

---

## Features

- 🗺️ **Smart Discovery** — Searches 12 business categories via Geoapify Places API
- 🌐 **Google Enrichment** — Scrapes Google for ratings, reviews, claimed status, social links
- 📊 **Priority Scoring** — Auto-scores leads 1–10 and classifies as HOT / WARM / COLD
- 💬 **WhatsApp Messages** — 9 industry-specific templates (short + full versions)
- 🔗 **Clickable wa.me Links** — Pre-filled WhatsApp links, ready to send
- 📁 **Formatted Excel Export** — 4 color-coded sheets with frozen headers & auto-filters
- 🚫 **Chain Detection** — Automatically skips franchises (McDonald's, KFC, Lakme, etc.)
- 🔄 **Deduplication** — Removes duplicates by phone number + business name

---

## Configuration

### CLI Options

| Flag                | Default          | Description                                               |
| ------------------- | ---------------- | --------------------------------------------------------- |
| `--api-key`         | _(required)_     | Your Geoapify API key                                     |
| `--location`        | `Puducherry`     | Location name (used in file naming & messages)            |
| `--lat`             | `11.9416`        | Latitude of search center                                 |
| `--lon`             | `79.8083`        | Longitude of search center                                |
| `--radius`          | `5`              | Search radius in km (auto-expands to 10km if <20 results) |
| `--max-leads`       | `100`            | Maximum number of leads to collect                        |
| `--skip-enrichment` | `off`            | Skip Google scraping for a faster run                     |
| `--output`          | _auto-generated_ | Custom output filename                                    |

### Examples

```bash
# Default: Puducherry, 5km radius, full enrichment
python main.py --api-key abc123

# Custom location with coordinates
python main.py --api-key abc123 --location "Chennai" --lat 13.0827 --lon 80.2707

# Quick scan without Google scraping
python main.py --api-key abc123 --skip-enrichment

# Limit to 30 leads with custom output name
python main.py --api-key abc123 --max-leads 30 --output my_leads.xlsx
```

---

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│  Geoapify   │────▶│   Google     │────▶│  Scoring  │
│  Discovery  │     │  Enrichment  │     │  (1-10)   │
└─────────────┘     └──────────────┘     └───────────┘
       │                                       │
  12 categories                          HOT / WARM / COLD
  50km → auto 100km                              │
                                               ▼
                                    ┌──────────────────┐
                                    │  WhatsApp Msgs   │
                                    │  9 templates     │
                                    │  short + full    │
                                    └──────────────────┘
                                               │
                                               ▼
                                    ┌──────────────────┐
                                    │  Excel Export    │
                                    │  4 sheets        │
                                    │  color-coded     │
                                    └──────────────────┘
```

### Pipeline Steps

| #   | Phase             | What Happens                                                   |
| --- | ----------------- | -------------------------------------------------------------- |
| 1   | **Discovery**     | Searches Geoapify for businesses across 12 categories          |
| 2   | **Deduplication** | Removes duplicates by phone + name                             |
| 3   | **Enrichment**    | Scrapes Google for ratings, reviews, social links _(optional)_ |
| 4   | **Scoring**       | Calculates priority score, assigns HOT/WARM/COLD status        |
| 5   | **Messages**      | Generates category-specific WhatsApp messages                  |
| 6   | **Export**        | Creates formatted `.xlsx` with 4 sheets                        |

---

## Excel Output

The generated file contains **4 sheets**:

### Sheet 1 — All Leads

All 22 columns with full business data. Color-coded rows:

| Color     | Meaning                                   |
| --------- | ----------------------------------------- |
| 🔴 Red    | **HOT** lead (score 8–10) — contact first |
| 🟡 Yellow | **WARM** lead (score 5–7)                 |
| ⚪ White  | **COLD** lead (score 1–4)                 |
| 🟠 Orange | Phone number missing                      |

### Sheet 2 — Hot Leads

Only HOT leads (score ≥ 8) with 6 key columns: name, category, phone, address, short message, and wa.me link. **Contact these first.**

### Sheet 3 — Outreach Messages

All businesses with their WhatsApp messages. Includes a summary block:

```
Total Messages Generated     : XX
WhatsApp Links Ready         : XX
Missing Phone Numbers        : XX
Hot Leads to Contact Today   : XX
```

### Sheet 4 — Summary & Stats

Dashboard with totals, top 3 categories, and the **Top 5 businesses to call TODAY**.

---

## Scoring Logic

Each business gets a priority score (max 10):

| Signal                                          | Points |
| ----------------------------------------------- | ------ |
| No website found                                | +4     |
| Google listing unclaimed                        | +2     |
| Fewer than 20 reviews                           | +1     |
| No social media (Instagram/Facebook)            | +2     |
| High-revenue category (restaurant/salon/clinic) | +1     |

| Score Range | Status  | Action              |
| ----------- | ------- | ------------------- |
| **8–10**    | 🔴 HOT  | Contact immediately |
| **5–7**     | 🟡 WARM | Follow up this week |
| **1–4**     | 🟢 COLD | Low priority        |

---

## Business Categories Targeted

| Category                         | Geoapify Search                             |
| -------------------------------- | ------------------------------------------- |
| 🍽️ Restaurants, Dhabas, Bakeries | `catering.restaurant`, `catering.fast_food` |
| 💇 Salons, Spas, Barbershops     | `service.beauty`                            |
| 🏥 Clinics, Dentists, Hospitals  | `healthcare.clinic_or_praxis`               |
| 🏫 Coaching, Tuition, Training   | `education.school`, `education.training`    |
| 🔧 Hardware, Building Material   | `commercial.hardware_and_tools`             |
| 🚗 Auto Repair, Car Wash         | `service.vehicle.repair`                    |
| 🛒 Grocery, Kirana, Supermarket  | `commercial.supermarket`                    |
| 🔌 Plumbers, Electricians        | `service`                                   |
| 🌿 Pest Control, Cleaning        | `service.cleaning`                          |
| 🎉 Event Decorators, Caterers    | `entertainment.event_service`               |
| 📸 Photographers, Videographers  | `service.photography`                       |

---

## Project Structure

```
lead-finder/
├── main.py              # CLI entry point (argparse)
├── config.py            # Location, categories, scoring weights
├── utils.py             # Phone normalizer, wa.me links, dedup
├── discovery.py         # Geoapify Places API integration
├── enrichment.py        # Google search scraping for extra data
├── scoring.py           # Priority scoring engine
├── messages.py          # 9 WhatsApp message templates
├── excel_export.py      # 4-sheet Excel export with formatting
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

---

## Dependencies

| Package          | Purpose                               |
| ---------------- | ------------------------------------- |
| `httpx`          | HTTP client for Geoapify API          |
| `openpyxl`       | Excel file generation with formatting |
| `beautifulsoup4` | HTML parsing for Google scraping      |
| `lxml`           | Fast HTML parser backend              |

---

## Troubleshooting

| Problem                  | Solution                                                                       |
| ------------------------ | ------------------------------------------------------------------------------ |
| `No businesses found`    | Check your API key is valid. Verify lat/lon coordinates.                       |
| `API error 401`          | Invalid Geoapify API key. Get one at [geoapify.com](https://www.geoapify.com/) |
| `Enrichment is slow`     | Use `--skip-enrichment` for a faster run (skips Google scraping)               |
| `Few results found`      | Tool auto-expands to 10km. Try `--radius 15` for wider search.                 |
| `PHONE MISSING in Excel` | Business has no phone on Geoapify. These rows are highlighted orange.          |

---

## License

MIT
