import requests
import time

def test_new_booking_page():
    """Test the new booking page functionality"""
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test accessing the new booking page
        print("Testing new booking page...")
        response = requests.get(f"{base_url}/book/new/")
        
        if response.status_code == 200:
            print("✓ New booking page loads successfully")
        else:
            print(f"✗ Failed to load new booking page. Status code: {response.status_code}")
            return False
            
        # Test API endpoints
        print("\nTesting API endpoints...")
        
        # Test doctors API (using a sample treatment ID)
        doctors_response = requests.get(f"{base_url}/book/api/doctors/1/")
        if doctors_response.status_code == 200:
            print("✓ Doctors API endpoint works")
        else:
            print(f"⚠ Doctors API endpoint returned status code: {doctors_response.status_code}")
            
        # Test hospitals API (using a sample treatment ID)
        hospitals_response = requests.get(f"{base_url}/book/api/hospitals/1/")
        if hospitals_response.status_code == 200:
            print("✓ Hospitals API endpoint works")
        else:
            print(f"⚠ Hospitals API endpoint returned status code: {hospitals_response.status_code}")
            
        # Test rooms API (using a sample hospital ID)
        rooms_response = requests.get(f"{base_url}/book/api/rooms/1/")
        if rooms_response.status_code == 200:
            print("✓ Rooms API endpoint works")
        else:
            print(f"⚠ Rooms API endpoint returned status code: {rooms_response.status_code}")
            
        print("\nAll tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Make sure the Django development server is running.")
        return False
    except Exception as e:
        print(f"✗ An error occurred during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_new_booking_page()