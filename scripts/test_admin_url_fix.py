#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.urls import reverse
from django.template import Context, Template

# Add the project directory to the Python path
sys.path.append('c:\\Users\\tusha\\Desktop\\Client 2')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

def test_url_resolution():
    """Test that the admin dashboard URL resolves correctly with namespacing"""
    try:
        # Test URL resolution
        admin_dashboard_url = reverse('accounts:admin_dashboard')
        print(f"✓ accounts:admin_dashboard resolves to: {admin_dashboard_url}")
        
        login_url = reverse('accounts:login')
        print(f"✓ accounts:login resolves to: {login_url}")
        
        signup_url = reverse('accounts:signup')
        print(f"✓ accounts:signup resolves to: {signup_url}")
        
        logout_url = reverse('accounts:logout')
        print(f"✓ accounts:logout resolves to: {logout_url}")
        
        doctor_profile_url = reverse('accounts:doctor_profile')
        print(f"✓ accounts:doctor_profile resolves to: {doctor_profile_url}")
        
        patient_portal_url = reverse('accounts:patient_portal')
        print(f"✓ accounts:patient_portal resolves to: {patient_portal_url}")
        
        patient_profile_url = reverse('accounts:patient_profile')
        print(f"✓ accounts:patient_profile resolves to: {patient_profile_url}")
        
        return True
    except Exception as e:
        print(f"✗ URL resolution failed: {e}")
        return False

def test_template_rendering():
    """Test that the template with namespaced URLs renders correctly"""
    try:
        # Create a mock user with profile
        from django.contrib.auth.models import User
        from django.contrib.auth.models import AnonymousUser
        
        # Test with admin user
        admin_user = User(username='admin')
        admin_user.userprofile = type('obj', (object,), {'user_type': 'admin'})()
        
        template_str = """
        <a href="{% url 'accounts:admin_dashboard' %}">Admin Dashboard</a>
        <a href="{% url 'accounts:doctor_profile' %}">Doctor Profile</a>
        <a href="{% url 'accounts:patient_portal' %}">Patient Portal</a>
        <a href="{% url 'accounts:login' %}">Login</a>
        """
        
        template = Template(template_str)
        context = Context({'user': admin_user})
        rendered = template.render(context)
        
        print("✓ Template with namespaced URLs renders correctly")
        print(f"Rendered template snippet: {rendered[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Template rendering failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing URL resolution fixes...")
    print("=" * 50)
    
    url_success = test_url_resolution()
    print()
    template_success = test_template_rendering()
    
    print("\n" + "=" * 50)
    if url_success and template_success:
        print("✓ All tests passed! The URL namespacing fixes should work correctly.")
    else:
        print("✗ Some tests failed. Please check the implementation.")