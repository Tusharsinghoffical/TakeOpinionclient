import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from feedbacks.models import Feedback
from django.db.models import Sum, Count

def verify_statistics():
    # Get all approved feedback
    feedback_list = Feedback.objects.filter(is_approved=True)
    
    # Calculate real-time statistics
    total_reviews = feedback_list.count()
    
    # Calculate average rating
    if total_reviews > 0:
        # Calculate weighted average rating
        rating_sum = feedback_list.aggregate(
            total_rating=Sum('rating')
        )['total_rating'] or 0
        average_rating = round(rating_sum / total_reviews, 1)
        
        # Calculate percentage of 4+ star reviews (would recommend)
        high_rating_count = feedback_list.filter(rating__gte=4).count()
        recommend_percentage = round((high_rating_count / total_reviews) * 100)
    else:
        average_rating = 0
        recommend_percentage = 0
    
    print(f"Total Reviews: {total_reviews}")
    print(f"Average Rating: {average_rating}")
    print(f"Recommend Percentage: {recommend_percentage}%")

if __name__ == '__main__':
    verify_statistics()