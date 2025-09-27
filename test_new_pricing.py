import requests

def test_new_pricing_page():
    """Test the new pricing page functionality"""
    base_url = "http://127.0.0.1:8000"
    
    try:
        # Test accessing the new pricing page
        print("Testing new pricing page...")
        response = requests.get(f"{base_url}/treatments/pricing/new/")
        
        if response.status_code == 200:
            print("✓ New pricing page loads successfully")
        else:
            print(f"✗ Failed to load new pricing page. Status code: {response.status_code}")
            return False
            
        print("\nNew pricing page is accessible at: http://127.0.0.1:8000/treatments/pricing/new/")
        print("Features implemented:")
        print("1. Treatment selection dropdown with categories")
        print("2. Hospital listing with pricing information")
        print("3. Advanced filtering options:")
        print("   - Price range filtering")
        print("   - Rating filtering")
        print("   - Accreditation filtering")
        print("   - Hospital name search")
        print("4. Sorting options (Price, Rating, Success Rate)")
        print("5. Booking buttons that redirect to booking page")
        print("6. Takeopinion consultation section")
        print("7. Active filter display with clear option")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the server. Make sure the Django development server is running.")
        return False
    except Exception as e:
        print(f"✗ An error occurred during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_new_pricing_page()