# TakeOpinion - Complete Website Documentation

## Overview
TakeOpinion is a comprehensive medical tourism platform that connects patients with global healthcare providers. Built with Django, the platform streamlines the process of finding treatments, booking appointments, and managing medical travel arrangements.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Technology Stack](#technology-stack)
3. [Core Features](#core-features)
4. [User Roles and Permissions](#user-roles-and-permissions)
5. [Data Models](#data-models)
6. [Booking System](#booking-system)
7. [Payment Processing](#payment-processing)
8. [Hotel Management](#hotel-management)
9. [Content Management](#content-management)
10. [API Endpoints](#api-endpoints)
11. [Admin Panel](#admin-panel)
12. [Security Measures](#security-measures)
13. [Deployment Configuration](#deployment-configuration)
14. [Development Guidelines](#development-guidelines)

## Project Structure

```
TakeOpinionclient/
├── accounts/                 # User authentication and profiles
│   ├── management/
│   │   └── commands/         # Custom management commands
│   ├── migrations/           # Database migrations
│   ├── templates/accounts/   # Account-related templates
│   ├── admin.py              # Admin panel configuration
│   ├── models.py             # User profile models
│   ├── urls.py               # Account URLs
│   └── views.py              # Account views
├── blogs/                    # Blog content management
│   ├── migrations/
│   ├── templates/blogs/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── bookings/                 # Appointment booking system
│   ├── management/commands/
│   ├── migrations/
│   ├── templates/bookings/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── core/                     # Core functionality and base templates
│   ├── management/commands/
│   ├── migrations/
│   ├── templates/core/
│   ├── admin.py
│   ├── context_processors.py
│   ├── middleware.py
│   ├── models.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
├── doctors/                  # Doctor management
│   ├── migrations/
│   ├── templates/doctors/
│   ├── templatetags/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── feedbacks/                # Patient feedback system
│   ├── migrations/
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── fixtures/                 # Sample data
├── hospitals/                # Hospital management
│   ├── migrations/
│   ├── templates/hospitals/
│   ├── templatetags/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── hotels/                   # Hotel accommodation management
│   ├── management/commands/
│   ├── migrations/
│   ├── templates/hotels/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── payments/                 # Payment processing
│   ├── management/commands/
│   ├── migrations/
│   ├── templates/payments/
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/                   # Static assets
├── staticfiles/              # Collected static files
├── takeopinion/              # Main Django project settings
├── templates/                # Base templates
├── treatments/               # Treatment management
│   ├── migrations/
│   ├── templates/treatments/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Technology Stack

### Backend
- **Framework**: Django 5.2.6
- **Language**: Python 3.8+
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django Auth System
- **Payment Processing**: Razorpay Integration

### Frontend
- **Templates**: Django Templates
- **Styling**: Bootstrap 5, Custom CSS
- **JavaScript**: Vanilla JS with some jQuery
- **Icons**: Bootstrap Icons

### Deployment
- **Platform**: Render.com
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Build System**: Custom build.sh script

## Core Features

### 1. Treatment Management
- Treatment categories (Medical, Aesthetic, Wellness)
- Detailed treatment information with pricing
- Starting prices for each treatment
- Treatment FAQs
- Affiliated hospitals and doctors

### 2. Doctor Management
- Doctor profiles with specializations
- Ratings and review system
- Associated hospitals and treatments
- Contact information
- Awards and achievements
- Languages spoken
- Profile pictures and media

### 3. Hospital Management
- Hospital listings with detailed information
- Location-based search
- Associated treatments and doctors
- Rating system
- Awards and recognition
- Starting prices for treatments
- Profile pictures and media

### 4. Booking System
- Multi-step booking process
- Treatment selection
- Doctor and hospital preferences
- Date scheduling
- Room preferences
- Booking status tracking
- Google Meet integration for consultations

### 5. Payment Processing
- Secure payment gateway integration (Razorpay)
- Payment status tracking
- Receipt generation
- Refund management
- Multiple currency support

### 6. Hotel Management
- Hotel listings near hospitals
- Room pricing and availability
- Booking system for medical travelers
- Location-based recommendations
- Post-payment suggestions

### 7. User Management
- Role-based access control (Patient, Doctor, Admin)
- Profile management
- Authentication and authorization
- Password recovery
- Google OAuth integration

### 8. Content Management
- Blog system for medical travel insights
- Treatment and hospital information
- Review and feedback system
- Portfolio and case studies

## User Roles and Permissions

### 1. Patient
- Browse treatments, doctors, and hospitals
- Book appointments
- Make payments
- Manage bookings
- Book hotel accommodations
- Upload medical reports
- Access patient dashboard
- View booking history
- Leave reviews and feedback

### 2. Doctor
- Manage professional profile
- View appointment schedules
- Update availability
- Access patient information
- Manage appointments
- View booking statistics
- Upload media and certificates
- Access doctor dashboard

### 3. Administrator
- Platform management
- User account oversight
- Content moderation
- Booking management
- Financial reporting
- System configuration
- Data analytics
- User role management
- Content approval

## Data Models

### User Management
```
User (Django Auth)
└── UserProfile
    ├── PatientProfile
    └── DoctorProfile
        ├── Specialization
        ├── Award
        └── Language
```

### Medical Entities
```
Treatment
├── TreatmentCategory
├── TreatmentFAQ
└── Hospital (Many-to-Many)

Doctor
├── Specialization
├── Award
├── Language
├── DoctorMedia
└── Hospital (Many-to-Many)

Hospital
├── Award
├── HospitalMedia
├── Accommodation
└── Treatment (Many-to-Many)
```

### Booking System
```
Booking
├── MedicalReport
├── BookingStatus
└── GoogleMeetLink

HotelBooking
├── Hotel
│   ├── HotelImage
│   └── HotelBooking
└── Nearby Hospitals (Many-to-Many)
```

### Content Management
```
BlogPost
├── BlogCategory
└── BlogMedia

Feedback
└── Approval Status
```

### Payment System
```
Payment
├── PaymentStatus
└── Currency
```

## Booking System

### Booking Process Workflow

#### Step 1: Treatment Selection
- Browse or search treatments
- View treatment details and pricing
- Select preferred treatment
- View affiliated hospitals and doctors

#### Step 2: Doctor Selection
- View doctors for selected treatment
- Check doctor ratings and reviews
- Select preferred doctor
- View doctor profile and credentials

#### Step 3: Hospital Selection
- View hospitals offering the treatment
- Check hospital ratings and facilities
- Select preferred hospital
- View hospital amenities and services

#### Step 4: Date and Preferences
- Select preferred date
- Choose room type and amenities
- Specify special requirements
- Add notes for the medical team

#### Step 5: Review and Confirm
- Review booking details
- Agree to terms and conditions
- Confirm booking
- Receive booking confirmation

#### Step 6: Payment
- Process payment through secure gateway
- Receive payment confirmation
- Get booking confirmation with Google Meet link
- Receive email notifications

### Booking Cost Calculation
- Treatment cost from hospital pricing
- ₹5,000 doctor consultation fee when doctor is selected
- ₹1,000 per selected amenity
- 15% discount applied to the total before displaying TakeOpinion price

### Booking Status Tracking
- Pending: Booking created but not confirmed
- Confirmed: Booking confirmed by hospital
- Completed: Treatment completed
- Cancelled: Booking cancelled
- Rescheduled: Booking rescheduled

## Payment Processing

### Features
- Integration with Razorpay
- Multiple payment methods (Credit/Debit Cards, Net Banking, UPI)
- Secure transaction processing
- Payment status tracking
- Receipt generation
- Refund management
- Multiple currency support (INR, USD)

### Process
1. User completes booking form
2. Redirected to payment page
3. Process payment through Razorpay
4. Payment verification
5. Booking confirmation
6. Receipt generation
7. Email notifications

### Security
- 256-bit SSL encryption
- PCI DSS compliance
- 3D Secure authentication
- Data protection
- Secure credential storage

## Hotel Management

### Features
- Hotel listings near hospitals
- Room pricing and availability
- Booking system for medical travelers
- Location-based recommendations
- Post-payment suggestions
- Hotel images and amenities

### Workflow
1. User completes medical booking
2. System suggests nearby hotels
3. User browses hotel options
4. Select and book hotel
5. Receive booking confirmation
6. Hotel contacts user for confirmation

### Hotel Data Model
```
Hotel
├── Name, Address, City, State, Country
├── Rating, Price per night
├── Description, Amenities
├── Nearby Hospitals (Many-to-Many)
├── Hotel Images
└── Hotel Bookings
```

## Content Management

### Blog System
- Medical travel insights
- Treatment-specific articles
- Destination information
- Success stories
- Health tips and advice
- Blog categories and tags

### Review System
- Patient feedback collection
- Star ratings (1-5)
- Written reviews
- Review moderation
- Approval workflow
- Response system

### Media Management
- Image uploads for doctors and hospitals
- Video URL integration
- Media galleries
- Profile pictures
- Certificate uploads

## API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/logout/` - User logout
- `POST /api/register/` - User registration

### Search
- `GET /api/search/doctors/` - Search doctors
- `GET /api/search/hospitals/` - Search hospitals
- `GET /api/search/treatments/` - Search treatments
- `GET /api/search/hotels/` - Search hotels

### Booking
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/` - Update booking

### Payments
- `POST /api/payments/` - Process payment
- `GET /api/payments/{id}/` - Get payment status

### Content
- `GET /api/blogs/` - List blog posts
- `GET /api/blogs/{id}/` - Get blog post details
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Submit review

## Admin Panel

### Features
- User management
- Content management
- Booking oversight
- Payment tracking
- Report generation
- System configuration
- Data analytics
- Role management
- Content approval

### Access
- URL: `/admin/`
- Role-based permissions
- Activity logging
- Audit trails
- Export capabilities

### Modules
1. **Accounts**: User profiles, authentication
2. **Bookings**: Appointment management, status tracking
3. **Doctors**: Doctor profiles, credentials, media
4. **Hospitals**: Hospital listings, media, pricing
5. **Treatments**: Treatment information, categories
6. **Payments**: Transaction tracking, refunds
7. **Hotels**: Accommodation listings, bookings
8. **Blogs**: Content management, categories
9. **Feedbacks**: Review moderation, approval
10. **Core**: Site settings, navigation

## Security Measures

### Authentication
- Django authentication system
- Session management
- Password hashing (PBKDF2)
- Two-factor authentication (planned)
- Google OAuth integration

### Data Protection
- HTTPS encryption
- Data validation and sanitization
- SQL injection prevention
- Cross-site scripting protection
- CSRF protection
- Clickjacking protection

### Payment Security
- PCI DSS compliance
- 256-bit SSL encryption
- 3D Secure authentication
- Tokenization
- Secure credential storage

### Access Control
- Role-based permissions
- Session timeout
- IP restrictions (configurable)
- Activity monitoring
- Failed login attempts tracking

### Content Security
- File upload validation
- Image processing with Pillow
- URL validation for external content
- Media file size limits
- Allowed file type restrictions

## Deployment Configuration

### Requirements
- Python 3.8+
- Django 5.2.6
- PostgreSQL (production)
- Redis (for caching)
- WhiteNoise (for static files)
- Gunicorn (WSGI server)

### Environment Variables
```
SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
RAZORPAY_KEY=your_razorpay_key
RAZORPAY_SECRET=your_razorpay_secret
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Render Deployment
- Uses [build.sh](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\build.sh) script
- Gunicorn configuration in [gunicorn.conf.py](file://c:\Users\tusha\Desktop\FreeLancer%20Website\TakeOpinionclient\gunicorn.conf.py)
- Automatic static file serving with WhiteNoise
- Environment variable configuration
- Health check endpoints

### Static Files
- Served using WhiteNoise
- STATIC_ROOT pointing to 'staticfiles' directory
- CompressedManifestStaticFilesStorage enabled for production
- Custom URL patterns in urls.py for production

### Media Files
- MEDIA_ROOT set to local 'media' directory
- MEDIA_URL set to '/media/' for serving user-uploaded content
- WHITENOISE_ALLOW_ALL_ORIGINS = True for proper media asset delivery

## Development Guidelines

### Coding Standards
- PEP 8 compliance
- Type hints for function signatures
- Descriptive variable names
- Consistent naming conventions
- Proper documentation strings
- Modular code organization

### Git Workflow
- Main branch for production
- Feature branches for development
- Pull requests for code review
- Semantic commit messages
- Regular merging to main branch

### Testing
- Unit tests for models and views
- Integration tests for workflows
- Manual testing for UI changes
- Cross-browser compatibility testing
- Performance testing

### Database Management
- Django migrations for schema changes
- Fixtures for sample data
- Regular backups
- Data validation
- Index optimization

### Performance Optimization
- Database indexing
- Query optimization
- Caching strategies
- Image optimization
- Minified assets
- Lazy loading

### Error Handling
- Proper exception handling
- Logging for debugging
- User-friendly error messages
- Graceful degradation
- Monitoring and alerts

## Custom Management Commands

### Accounts
- `setup_google_oauth.py` - Configure Google OAuth settings

### Bookings
- `create_sample_booking.py` - Create sample booking data

### Core
- `seed_demo.py` - Populate database with demo data
- `fix_naive_datetimes.py` - Fix timezone-aware datetime issues

### Doctors
- `add_doctor_profile_pictures.py` - Add profile pictures to doctors

### Hotels
- `populate_hotels.py` - Add sample hotel data
- `associate_hotels_hospitals.py` - Link hotels with nearby hospitals

### Payments
- `cleanup_razorpay_payments.py` - Clean up old payment records

## Template Structure

### Base Templates
- `base.html` - Main template with navigation and footer
- `core/partials/` - Shared UI components
- `hero_section.html` - Dynamic hero section

### App-Specific Templates
- `accounts/` - Login, signup, dashboard templates
- `blogs/` - Blog listing and detail pages
- `bookings/` - Booking forms and confirmation pages
- `doctors/` - Doctor listings and profiles
- `hospitals/` - Hospital listings and details
- `hotels/` - Hotel listings and booking pages
- `payments/` - Payment processing pages
- `treatments/` - Treatment listings and details

## URL Routing

### Main URLs
- `/` - Home page
- `/accounts/` - Authentication pages
- `/doctors/` - Doctor listings and profiles
- `/hospitals/` - Hospital listings and details
- `/treatments/` - Treatment listings and details
- `/book/` - Booking system
- `/payments/` - Payment processing
- `/hotels/` - Hotel management
- `/blogs/` - Blog content
- `/admin/` - Admin panel

### API URLs
- `/api/search/` - Search endpoints
- `/api/bookings/` - Booking endpoints
- `/api/payments/` - Payment endpoints

## Internationalization

### Supported Languages
- English (primary)
- Hindi (planned)

### Translation System
- Django i18n support
- Language switcher
- Translatable content
- Locale-specific formatting

## Future Enhancements

### Planned Features
- Telemedicine integration
- Mobile application
- Multi-language support
- Advanced analytics dashboard
- AI-powered recommendations
- Insurance integration
- Chat system for patient-doctor communication
- Video consultation capabilities
- Treatment comparison tool
- Medical record management
- Appointment reminders
- Loyalty program

### Technical Improvements
- Microservice architecture
- GraphQL API
- Real-time notifications
- Enhanced caching
- Improved search functionality
- Progressive Web App (PWA) features
- Performance monitoring
- Automated testing suite

## Troubleshooting

### Common Issues
1. **Database Connection**: Check DATABASE_URL environment variable
2. **Static Files**: Run `python manage.py collectstatic`
3. **Migrations**: Run `python manage.py migrate`
4. **Payment Gateway**: Verify RAZORPAY credentials
5. **Email Sending**: Configure SMTP settings
6. **File Uploads**: Check media directory permissions
7. **Performance**: Enable caching and optimize queries

### Debugging Tools
- Django Debug Toolbar
- Logging configuration
- Database query analysis
- Browser developer tools
- Network monitoring
- Error tracking services

## Maintenance

### Regular Tasks
- Database backups
- Log rotation
- Security updates
- Performance monitoring
- Content updates
- User support

### Monitoring
- Error tracking
- Performance metrics
- User activity logs
- System health checks
- Uptime monitoring
- Resource utilization

## Support and Contact

For technical support and inquiries, please contact:
- Email: tusharsinghkumar04@gmail.com
- Phone: 8851619647
- Location: New Delhi, India

## Brand Identity

Associated brands:
- codewithmrsingh
- cws

---

*This documentation provides a comprehensive overview of the TakeOpinion platform, covering its features, architecture, workflows, and technical implementation details.*