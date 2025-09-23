import requests
import time

def check_server():
    """Check if the Django server is running"""
    try:
        response = requests.get('http://127.0.0.1:8000/accounts/reviews/', timeout=5)
        print(f"Server is running. Status code: {response.status_code}")
        print(f"Page title: {response.text[:100]}...")
        return True
    except requests.exceptions.ConnectionError:
        print("Server is not running or not accessible")
        return False
    except requests.exceptions.Timeout:
        print("Request timed out")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    print("Checking if the Django server is running...")
    success = check_server()
    if success:
        print("Server check completed successfully!")
    else:
        print("Server check failed!")