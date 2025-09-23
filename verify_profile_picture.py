import requests
import re

def verify_profile_picture_feature():
    """Verify the profile picture feature implementation"""
    try:
        # Check if the patient profile page loads
        response = requests.get('http://127.0.0.1:8000/accounts/patient/profile/', timeout=5)
        
        if response.status_code == 200:
            print("✓ Patient profile page loads successfully")
            
            # Check for key elements in the profile picture section
            content = response.text
            
            # Check for profile picture section
            if 'Profile Picture' in content:
                print("✓ Profile picture section found")
            else:
                print("✗ Profile picture section not found")
                
            # Check for file input
            if 'profile_picture' in content and 'type="file"' in content:
                print("✓ Profile picture file input found")
            else:
                print("✗ Profile picture file input not found")
                
            # Check for upload button
            if 'Upload Picture' in content:
                print("✓ Upload picture button found")
            else:
                print("✗ Upload picture button not found")
                
            # Check for form with proper enctype
            if 'enctype="multipart/form-data"' in content:
                print("✓ Form has proper enctype for file uploads")
            else:
                print("✗ Form missing proper enctype for file uploads")
                
            # Check for profile picture display area
            if 'bg-light rounded-circle' in content:
                print("✓ Profile picture display area found")
            else:
                print("✗ Profile picture display area not found")
                
            # Check for conditional rendering (profile picture vs default icon)
            if '{% if user_profile.profile_picture %}' in content:
                print("✓ Conditional rendering for profile picture found")
            else:
                print("✗ Conditional rendering for profile picture not found")
                
        else:
            print(f"✗ Patient profile page failed to load. Status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running or not accessible")
    except requests.exceptions.Timeout:
        print("✗ Request timed out")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def verify_template_structure():
    """Verify the template structure"""
    try:
        # Read the template file directly
        with open(r'c:\Users\tusha\Desktop\Client 2\accounts\templates\accounts\patient_profile.html', 'r') as f:
            content = f.read()
            
        print("\n--- Template Structure Verification ---")
        
        # Check for required sections
        if '<!-- Profile Picture Upload Form -->' in content:
            print("✓ Profile picture upload form section marker found")
        else:
            print("✗ Profile picture upload form section marker not found")
            
        # Check for file input field
        if 'id="profile_picture"' in content and 'type="file"' in content:
            print("✓ Profile picture file input field found")
        else:
            print("✗ Profile picture file input field not found")
            
        # Check for form tag with proper attributes
        if '<form method="POST" enctype="multipart/form-data"' in content:
            print("✓ Form tag with proper attributes found")
        else:
            print("✗ Form tag with proper attributes not found")
            
        # Check for CSS styling
        if '.bg-light.rounded-circle' in content:
            print("✓ Custom CSS styling found")
        else:
            print("✗ Custom CSS styling not found")
            
    except FileNotFoundError:
        print("✗ Template file not found")
    except Exception as e:
        print(f"✗ Error reading template file: {e}")

if __name__ == "__main__":
    print("Verifying profile picture feature implementation...")
    verify_profile_picture_feature()
    verify_template_structure()
    print("\nVerification completed!")