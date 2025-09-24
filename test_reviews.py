import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from doctors.models import Doctor
from feedbacks.models import Feedback

def create_test_reviews():
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'user_type': 'patient'
        }
    )
    
    # Get a doctor for the review
    doctor = Doctor.objects.first()
    if not doctor:
        print("No doctors found in the database. Please add some doctors first.")
        return
    
    # Create some test reviews with different ratings
    reviews_data = [
        {
            'title': 'Excellent Doctor',
            'comment': 'Dr. Mehta is very professional and caring.',
            'rating': 5
        },
        {
            'title': 'Good Experience',
            'comment': 'Nice and good doctor',
            'rating': 4
        },
        {
            'title': 'Average Service',
            'comment': 'The service was okay, nothing special.',
            'rating': 3
        },
        {
            'title': 'Great Hospital',
            'comment': 'NIce and good',
            'rating': 5
        },
        {
            'title': 'Test Review',
            'comment': 'This is a test review',
            'rating': 4
        }
    ]
    
    # Create the reviews
    for review_data in reviews_data:
        Feedback.objects.create(
            patient=user_profile,
            feedback_type='doctor',
            doctor=doctor,
            rating=review_data['rating'],
            title=review_data['title'],
            comment=review_data['comment'],
            is_approved=True
        )
    
    print(f"Created {len(reviews_data)} test reviews.")

if __name__ == '__main__':
    create_test_reviews()