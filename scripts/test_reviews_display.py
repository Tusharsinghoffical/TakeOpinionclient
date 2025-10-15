#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.template.loader import render_to_string

# Add the project directory to the Python path
sys.path.append('c:\\Users\\tusha\\Desktop\\Client 2')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

def test_footer_reviews_display():
    """Test that the footer patient stories section renders correctly"""
    try:
        # Render the base template to check if it works
        rendered = render_to_string('base.html', {
            'user': type('obj', (object,), {
                'is_authenticated': False
            })()
        })
        
        # Check if our patient stories content is in the rendered template
        if 'Patient Stories' in rendered and 'Michael Johnson' in rendered and 'Sarah Williams' in rendered:
            print("✓ Footer patient stories section renders correctly")
            return True
        else:
            print("✗ Footer patient stories section not found in rendered template")
            return False
    except Exception as e:
        print(f"✗ Footer reviews display test failed: {e}")
        return False

def test_hospital_reviews_display():
    """Test that hospital detail page renders reviews correctly"""
    try:
        # Create a mock hospital object
        hospital = type('obj', (object,), {
            'id': 1,
            'name': 'Test Hospital',
            'slug': 'test-hospital',
            'rating': 4.7
        })()
        
        # Render the hospital detail template
        rendered = render_to_string('hospitals/detail.html', {
            'hospital': hospital
        })
        
        # Check if hospital reviews section is in the rendered template
        if 'Patient Reviews' in rendered and 'Michael Johnson' in rendered:
            print("✓ Hospital detail page reviews section renders correctly")
            return True
        else:
            print("✗ Hospital detail page reviews section not found in rendered template")
            return False
    except Exception as e:
        print(f"✗ Hospital reviews display test failed: {e}")
        return False

def test_doctor_reviews_display():
    """Test that doctor detail page renders reviews correctly"""
    try:
        # Create a mock doctor object
        doctor = type('obj', (object,), {
            'id': 1,
            'name': 'Smith',
            'slug': 'dr-smith',
            'rating': 4.8,
            'review_count': 120
        })()
        
        # Render the doctor detail template
        rendered = render_to_string('doctors/detail.html', {
            'doctor': doctor
        })
        
        # Check if doctor reviews section is in the rendered template
        if 'Patient Reviews' in rendered and 'Dr. Smith' in rendered:
            print("✓ Doctor detail page reviews section renders correctly")
            return True
        else:
            print("✗ Doctor detail page reviews section not found in rendered template")
            return False
    except Exception as e:
        print(f"✗ Doctor reviews display test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing patient reviews display implementation...")
    print("=" * 50)
    
    footer_success = test_footer_reviews_display()
    print()
    hospital_success = test_hospital_reviews_display()
    print()
    doctor_success = test_doctor_reviews_display()
    
    print("\n" + "=" * 50)
    if footer_success and hospital_success and doctor_success:
        print("✓ All tests passed! The patient reviews display implementation should work correctly.")
        print("\nKey improvements made:")
        print("1. Horizontal format for patient success stories in footer")
        print("2. Patient reviews displayed on hospital detail pages")
        print("3. Patient reviews displayed on doctor detail pages")
        print("4. Video and image testimonials integrated")
        print("5. Links to full reviews page with filtering")
    else:
        print("✗ Some tests failed. Please check the implementation.")