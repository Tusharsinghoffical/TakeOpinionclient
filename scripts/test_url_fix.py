"""
Test script to verify the URL fix for the accounts namespace
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.urls import reverse

def test_accounts_namespace():
    print("Testing accounts namespace fix...")
    
    try:
        # Try to reverse the admin dashboard URL
        url = reverse('accounts:admin_dashboard')
        print(f"Accounts admin dashboard URL: {url}")
        
        # Try to reverse the patient dashboard URL
        url = reverse('accounts:patient_dashboard')
        print(f"Accounts patient dashboard URL: {url}")
        
        print("URL namespace fix verified successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_accounts_namespace()