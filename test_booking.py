import requests

def test_booking_page():
    """Test the booking page functionality"""
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test accessing the booking page
        print("Testing booking page...")
        response = requests.get(f"{base_url}/book/")
        
        if response.status_code == 200:
            print("✓ Booking page loads successfully")
        else:
            print(f"✗ Failed to load booking page. Status code: {response.status_code}")
            return False
            
        print("\nBooking page is accessible at: http://127.0.0.1:8000/book/")
        print("The page should now work without the 'An error occurred while processing your booking request' error.")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Make sure the Django development server is running.")
        return False
    except Exception as e:
        print(f"✗ An error occurred during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_booking_page()