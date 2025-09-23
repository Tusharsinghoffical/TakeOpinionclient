import requests

def test_profile_picture_feature():
    """Test the profile picture feature"""
    try:
        # First, let's check if the patient profile page loads
        response = requests.get('http://127.0.0.1:8000/accounts/patient/profile/', timeout=5)
        if response.status_code == 200:
            print("Patient profile page loads successfully")
            
            # Check if the profile picture section exists in the HTML
            if 'Profile Picture' in response.text:
                print("Profile picture section found in the page")
            else:
                print("Profile picture section not found in the page")
                
            # Check if the file input exists
            if 'profile_picture' in response.text:
                print("Profile picture file input found")
            else:
                print("Profile picture file input not found")
        else:
            print(f"Patient profile page failed to load. Status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Server is not running or not accessible")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Testing profile picture feature...")
    test_profile_picture_feature()
    print("Test completed!")