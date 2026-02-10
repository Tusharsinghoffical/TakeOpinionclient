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
- **Database**: SQLite (development), PostgreSQL (production)
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
   cd TakeOpinionclient
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Load initial data (optional):
   ```bash
   python manage.py loaddata fixtures/*.json
   ```

6. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application:
   - Website: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Deployment

The project is configured for deployment on Render with:
- Custom build script ([build.sh](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\build.sh))
- Gunicorn configuration ([gunicorn.conf.py](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\gunicorn.conf.py))
- Proper static file handling with Whitenoise

### Environment Variables

For production deployment, set the following environment variables:
- [SECRET_KEY](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\takeopinion\settings_prod.py#L15-L15): Django secret key
- `DATABASE_URL`: PostgreSQL database connection URL
- [DEBUG](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\takeopinion\settings_prod.py#L18-L18): Set to "False" for production
- [ALLOWED_HOSTS](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\takeopinion\settings_prod.py#L21-L21): Comma-separated list of allowed hosts

### Render Deployment

1. Fork the repository to your GitHub account
2. Connect your GitHub repository to Render
3. Configure the environment variables as mentioned above
4. Deploy the application

The [render.yaml](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\render.yaml) file contains the deployment configuration for Render.

## Development Guidelines

- Follow American English spelling conventions
- Use hardcoded URL paths instead of Django namespaced URLs
- Maintain consistent pricing structure for room options
- Apply 15% discount to all bookings in the cost calculation

## API Endpoints

- `/api/v1/entities/<entity_type>/` - Get entities (doctors, hospitals, treatments) for dropdowns
- `/treatments/api/search/` - Search treatments
- `/doctors/api/search/` - Search doctors
- `/hospitals/api/search/` - Search hospitals

## Testing

Run tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is proprietary and confidential. All rights reserved.

## GITHUB ADD
git add .
git commit -m "Update navbar logo from TakeOpinion to Mediplus logo"
git push origin main