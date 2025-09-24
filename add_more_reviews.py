import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from doctors.models import Doctor
from feedbacks.models import Feedback

def create_more_reviews():
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
    
    # Create more test reviews with different ratings
    reviews_data = [
        {
            'title': 'Outstanding Care',
            'comment': 'The doctor provided exceptional care and attention to my needs.',
            'rating': 5
        },
        {
            'title': 'Good Service',
            'comment': 'Satisfied with the treatment and professionalism.',
            'rating': 4
        },
        {
            'title': 'Average Experience',
            'comment': 'The service was okay, nothing special.',
            'rating': 3
        },
        {
            'title': 'Below Expectations',
            'comment': 'I was not satisfied with the care provided.',
            'rating': 2
        },
        {
            'title': 'Poor Service',
            'comment': 'The experience was disappointing overall.',
            'rating': 1
        },
        {
            'title': 'Excellent Doctor',
            'comment': 'Highly recommend this doctor for their expertise.',
            'rating': 5
        },
        {
            'title': 'Good Hospital',
            'comment': 'The facilities and staff were very helpful.',
            'rating': 4
        },
        {
            'title': 'Decent Treatment',
            'comment': 'The treatment was adequate but could be improved.',
            'rating': 3
        },
        {
            'title': 'Great Staff',
            'comment': 'The nursing staff was particularly attentive.',
            'rating': 5
        },
        {
            'title': 'Satisfactory Visit',
            'comment': 'My visit was fine, no major complaints.',
            'rating': 4
        },
        {
            'title': 'Wonderful Experience',
            'comment': 'Everything about my visit was perfect.',
            'rating': 5
        },
        {
            'title': 'Could Be Better',
            'comment': 'There were some issues that need addressing.',
            'rating': 2
        },
        {
            'title': 'Fantastic Care',
            'comment': 'The level of care exceeded my expectations.',
            'rating': 5
        },
        {
            'title': 'Good, Not Great',
            'comment': 'It was a decent experience but not outstanding.',
            'rating': 3
        },
        {
            'title': 'Highly Recommend',
            'comment': 'I would definitely come back and recommend to others.',
            'rating': 5
        }
    ]
    
    # Create the reviews
    for i, review_data in enumerate(reviews_data):
        # Add some variation in creation dates
        created_at = datetime.now() - timedelta(days=random.randint(0, 30))
        
        feedback = Feedback.objects.create(
            patient=user_profile,
            feedback_type='doctor',
            doctor=doctor,
            rating=review_data['rating'],
            title=review_data['title'],
            comment=review_data['comment'],
            is_approved=True
        )
        # Update created_at to have some variation
        feedback.created_at = created_at
        feedback.save()
    
    print(f"Created {len(reviews_data)} additional test reviews.")

if __name__ == '__main__':
    create_more_reviews()