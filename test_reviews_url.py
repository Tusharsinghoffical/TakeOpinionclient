"""
Test script to verify the reviews URL fix
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.urls import reverse

def test_reviews_url():
    print("Testing reviews URL fix...")
    
    try:
        # Try to reverse the reviews page URL
        url = reverse('accounts:reviews_page')
        print(f"Accounts reviews page URL: {url}")
        
        print("Reviews URL fix verified successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_reviews_url()