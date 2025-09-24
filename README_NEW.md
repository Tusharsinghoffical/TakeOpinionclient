# TakeOpinion - Medical Travel Platform

TakeOpinion is a comprehensive medical travel platform that connects patients with doctors, hospitals, and treatments worldwide.

## Features

- **Treatment Search**: Find medical treatments across various categories
- **Doctor Profiles**: Detailed information about medical professionals
- **Hospital Listings**: Accredited hospitals with ratings and reviews
- **Booking System**: Complete medical travel booking workflow
- **Hotel Recommendations**: Accommodation suggestions near medical facilities
- **Reviews System**: Patient reviews and ratings
- **Blog Content**: Medical travel guides and information

## Technology Stack

- **Backend**: Django 5.2.6 (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: Render.com
- **Static Files**: WhiteNoise
- **Payment Processing**: Razorpay, Stripe

## Setup Instructions

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd takeopinion
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

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Load sample data:
   ```bash
   python manage.py seed_demo
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000` in your browser

## Deployment

### Deploy to Render

1. Run the deployment script:
   ```bash
   # On Windows
   deploy.bat
   
   # On macOS/Linux
   python deploy_to_render.py
   ```

2. Follow the instructions in [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

### Data Preservation

All existing data (doctors, hospitals, treatments, bookings, etc.) is automatically preserved during deployment through JSON fixtures.

## Project Structure

```
takeopinion/
├── accounts/          # User authentication and profiles
├── blogs/             # Blog posts and articles
├── bookings/          # Booking system and accommodations
├── core/              # Core functionality and middleware
├── doctors/           # Doctor profiles and management
├── feedbacks/         # Reviews and feedback system
├── hospitals/         # Hospital listings and management
├── payments/          # Payment processing
├── treatments/        # Treatment listings and management
├── templates/         # Base templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User uploads
├── fixtures/          # Data fixtures for deployment
└── takeopinion/       # Main Django project settings
```

## Key Features Implemented

### Booking System
- Real-time booking form with validation
- Doctor and hospital selection
- Treatment preferences
- Booking confirmation with hotel recommendations

### Hotel Recommendations
- Contextual hotel suggestions based on booked medical facilities
- Integration with Accommodation model
- Display on booking confirmation page

### Reviews System
- Patient reviews for doctors, hospitals, and treatments
- Real-time statistics (average rating, total reviews, recommendation percentage)
- Search functionality

### Admin Interface
- Comprehensive admin panel for managing all content
- User-friendly interface for adding/editing data

## Environment Variables

For production deployment, set these environment variables:

```
DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@host:port/dbname  # Optional
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary and confidential.

## Support

For support, contact the development team.