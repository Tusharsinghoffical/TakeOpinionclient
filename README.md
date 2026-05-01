# TakeOpinion — Medical Tourism Platform

> **AI-powered medical tourism platform** connecting patients with verified doctors, hospitals, and treatments worldwide. Features an intelligent chatbot that analyzes medical reports and delivers personalized results.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)

---

## 🌟 What's New

### AI Smart Search & Chatbot
- **Medical Report Analysis** — Upload PDF/image/text reports; the system extracts diagnosis, conditions, medications, and precautions automatically
- **Smart Results Page** (`/enquiries/results/`) — Shows relevant doctors, hospitals, treatments, blogs, and pricing based on your query or uploaded report
- **Session Context** — Follow-up queries are merged with prior search context for refined results
- **Floating Chatbot Widget** — Available on every page; redirects to Smart Results with full report support

### Complete Database Seed
Run `python manage.py seed_full_data` to populate:
- **19 real doctors** (Dr. Naresh Trehan, Dr. Devi Shetty, Dr. Ahmed Khan, etc.)
- **28 hospitals** (Apollo, AIIMS, Medanta, Fortis, Bumrungrad, etc.)
- **72 treatments** across 13 specialities
- **56 patient feedbacks** with realistic reviews
- **24 blog posts** covering all major conditions

### Redesigned UI
- Modern dark navy/blue theme consistent across all pages
- Redesigned: Home, Doctors list, Hospitals list, Treatments list, Treatment detail, Pricing/Comparison, Smart Results
- New footer with real patient reviews from DB
- Responsive design with hover effects and smooth transitions

---

## 🏗️ Project Structure

```
TakeOpinionclient/
├── accounts/           # User auth, patient/doctor/admin profiles
├── blogs/              # Medical blog content
├── bookings/           # Appointment & treatment booking with Google Meet
├── core/               # Base views, context processors, seed commands
│   └── management/commands/
│       └── seed_full_data.py   # Full DB seed command
├── doctors/            # Doctor profiles, specializations, media
├── enquiry_bot/        # AI chatbot & Smart Search engine
│   ├── smart_search.py         # MedicalIntentExtractor, SiteContentAggregator
│   ├── views.py                # smart_results_view, smart_results_api
│   └── templates/enquiry_bot/
│       └── smart_results.html  # Smart Results page
├── feedbacks/          # Patient reviews and ratings
├── hospitals/          # Hospital listings, accreditations
├── hotels/             # Accommodation booking
├── payments/           # Stripe & Razorpay integration
├── treatments/         # Treatment catalog, FAQs, detail pages
├── static/             # CSS, JS, images
├── templates/
│   └── base.html       # Global navbar, footer, floating chatbot
├── conftest.py         # Pytest Django configuration
└── pytest.ini          # Test settings
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/Tusharsinghoffical/TakeOpinionclient.git
cd TakeOpinionclient
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 3. Seed Realistic Data

```bash
python manage.py seed_full_data
```

This creates all doctors, hospitals, treatments, feedbacks, blogs, and patient users.

### 4. Run

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**  
Admin: **http://127.0.0.1:8000/admin/**

---

## 🤖 AI Smart Search

### How It Works

1. User types a condition (e.g. "diabetes") or uploads a medical report PDF
2. `MedicalIntentExtractor` tokenizes the text and matches against `CONDITION_SPECIALIZATION_MAP`
3. `SiteContentAggregator` queries doctors, hospitals, treatments, blogs filtered by matched conditions
4. Results page shows: Diagnosis, Medications, Precautions, Recommendations + DB results

### Key Components (`enquiry_bot/smart_search.py`)

| Class | Purpose |
|-------|---------|
| `MedicalIntentExtractor` | Extracts keywords, conditions, specializations from text |
| `ReportParser` | Parses PDF/image/text medical reports |
| `SiteContentAggregator` | Queries DB and returns `SmartResultsContext` |
| `PlaceholderRegistry` | Ensures all 10 content categories always render |
| `CONDITION_SPECIALIZATION_MAP` | Maps 35+ medical terms to doctor specializations |

### Supported Conditions

Cardiac, Orthopedic, Neurology, Oncology, Endocrinology, Gastroenterology, Pulmonology, Ophthalmology, Urology, Fertility, Cosmetic Surgery, Dental, Wellness

### Test Reports

Sample PDFs for testing are in `test_reports/`. Regenerate with:
```bash
python test_reports/generate_pdfs.py
```

---

## 🧪 Testing

```bash
# Run all tests
pytest enquiry_bot/tests_smart_search.py -v

# Run with coverage
pytest enquiry_bot/tests_smart_search.py --cov=enquiry_bot -v
```

**31 tests** covering:
- Property 1: `raw_query` identity (200 examples)
- Property 2: Specializations subset invariant (200 examples)
- Property 3: Bounded doctor results ≤ 6 (50 examples)
- Property 4: Placeholder count invariant (200 examples)
- Unit tests: `MedicalIntentExtractor`, `ReportParser`, `PlaceholderRegistry`
- Integration tests: `smart_results_view` (GET/POST/file upload)

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Django REST Framework |
| AI/Search | Custom NLP with Hypothesis property-based testing |
| Database | SQLite (dev), PostgreSQL (prod) |
| Frontend | Bootstrap 5.3, Bootstrap Icons |
| Payments | Stripe, Razorpay |
| PDF Parsing | PyPDF2 |
| Testing | pytest, hypothesis |
| Deployment | Gunicorn, Whitenoise, Render |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/enquiries/results/` | GET/POST | Smart Results page |
| `/enquiries/results/api/` | POST | Smart Results JSON API |
| `/api/v1/entities/<type>/` | GET | Entity dropdowns |
| `/treatments/api/search/` | GET | Search treatments |
| `/doctors/api/search/` | GET | Search doctors |
| `/hospitals/api/search/` | GET | Search hospitals |
| `/book/api/hospitals/<id>/` | GET | Hospitals by treatment |

---

## 🌐 Deployment (Render)

### Environment Variables

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### Deploy Steps

1. Fork repo → Connect to Render
2. Set environment variables
3. Render auto-detects `build.sh` and `render.yaml`
4. After deploy: `python manage.py seed_full_data`

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `enquiry_bot/smart_search.py` | Core AI search engine |
| `enquiry_bot/views.py` | Smart Results view + API |
| `core/management/commands/seed_full_data.py` | Full DB seed |
| `templates/base.html` | Global layout with floating chatbot |
| `core/templates/core/home.html` | Redesigned home page |
| `conftest.py` | Pytest Django setup |
| `pytest.ini` | Test configuration |

---

## 🔧 Development Commands

```bash
# Seed full database
python manage.py seed_full_data

# Generate test PDFs
python test_reports/generate_pdfs.py

# Run tests
pytest enquiry_bot/tests_smart_search.py -v

# Django checks
python manage.py check

# Collect static files
python manage.py collectstatic
```

---

## 📄 License

Proprietary and confidential. All rights reserved © 2026 TakeOpinion.
