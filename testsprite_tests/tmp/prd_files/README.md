# TakeOpinion Medical Tourism Platform

TakeOpinion is a comprehensive Django-based platform for medical tourism that connects patients with doctors, hospitals, and treatments across the globe.

## Project Overview

This platform enables patients to:
- Browse and compare medical treatments
- Find qualified doctors and accredited hospitals
- Book appointments and treatments
- Arrange accommodation at partnered hotels
- Process payments securely
- Access medical reports and consultation records

## Key Features

### Medical Services
- **Treatment Catalog**: Extensive database of medical treatments with pricing and details
- **Doctor Directory**: Profiles of qualified medical professionals with specialties and experience
- **Hospital Network**: Accredited hospitals with facilities and location information
- **Booking System**: Comprehensive appointment scheduling with Google Meet integration

### User Management
- Patient and doctor accounts
- Admin dashboard for platform management
- Profile management for all user types

### Accommodation
- Hotel booking system integrated with hospital locations
- Room options with amenities (Normal, Deluxe, Premium, Executive Suite)
- Pricing: ₹2,500-₹9,000 per night depending on room tier

### Payment Processing
- Secure payment handling with Stripe and Razorpay integration
- Transparent pricing with 15% platform discount

### Content Management
- Blog system for medical travel insights
- Feedback and review system
- Search functionality across all entities

## Technology Stack

- **Backend**: Django 5.2.6 with Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5 with crispy forms
- **Deployment**: Gunicorn with Whitenoise for static files
- **Background Tasks**: Celery with Redis
- **Payment Processing**: Stripe and Razorpay
- **Static Files**: Whitenoise with CompressedManifestStaticFilesStorage

## Project Structure

```
├── accounts/          # User authentication and profiles
├── blogs/             # Blog content management
├── bookings/          # Appointment and treatment booking system
├── core/              # Shared components and base functionality
├── doctors/           # Doctor profiles and management
├── feedbacks/         # User feedback and reviews
├── hospitals/         # Hospital listings and information
├── hotels/            # Accommodation booking system
├── payments/          # Payment processing
├── treatments/        # Treatment catalog and details
├── static/            # CSS, JavaScript, and other static assets
└── templates/         # HTML templates
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tusharsinghoffical/TakeOpinionclient.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py migrate
   ```

4. Load initial data (optional):
   ```bash
   python manage.py loaddata fixtures/*.json
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment

The project is configured for deployment on Render with:
- Custom build script (`build.sh`)
- Gunicorn configuration (`gunicorn.conf.py`)
- Proper static file handling with Whitenoise

## Development Guidelines

- Follow American English spelling conventions
- Use hardcoded URL paths instead of Django namespaced URLs
- Maintain consistent pricing structure for room options
- Apply 15% discount to all bookings in the cost calculation

## Environment Variables

Key environment variables required for production:
- Database connection settings
- Payment gateway credentials (Stripe, Razorpay)
- Email configuration
- Secret key for Django

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is proprietary and confidential. All rights reserved.