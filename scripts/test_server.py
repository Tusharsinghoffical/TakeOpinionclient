import requests
import time

def test_server():
    try:
        print("Testing server connection...")
        response = requests.get('http://127.0.0.1:8000/', timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Length: {len(response.text)} characters")
        if response.status_code == 200:
            print("✅ Server is responding correctly!")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    test_server()