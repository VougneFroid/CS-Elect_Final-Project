"""
Test script for JWT Authentication
Run this to test the authentication endpoints and protected routes.
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_authentication():
    """Test the complete authentication flow"""
    
    # Test 1: Register a new user
    print("\n🔹 TEST 1: Register a new user")
    register_data = {
        "username": "teasdpilot",
        "email": "testpilot@asdsdawe.com",
        "password": "e123123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    print_response("Registration Response", response)
    
    if response.status_code == 201:
        token = response.json().get('token')
        print(f"\n✅ Registration successful! Token received: {token[:50]}...")
    elif response.status_code == 409:
        print("\n⚠️  User already exists, trying to login instead...")
        # Test 2: Login with existing user
        login_data = {
            "username": "teasdpilot",
            "password": "e123123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print_response("Login Response", response)
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"\n✅ Login successful! Token received: {token[:50]}...")
        else:
            print("\n❌ Login failed!")
            return None
    else:
        print("\n❌ Registration failed!")
        return None
    
    # Test 3: Try to access protected endpoint WITHOUT token (should fail)
    print("\n\n🔹 TEST 3: Access protected endpoint WITHOUT token (should fail)")
    pilot_data = {
        "name": "Luke Skywalker",
        "flight_years": 10,
        "rank": "Commander",
        "mission_success": 98
    }
    response = requests.post(f"{BASE_URL}/api/pilots", json=pilot_data)
    print_response("Create Pilot WITHOUT Token", response)
    
    if response.status_code == 401:
        print("\n✅ Protected endpoint correctly rejected request without token!")
    else:
        print("\n❌ Security issue: Endpoint should require authentication!")
    
    # Test 4: Access protected endpoint WITH valid token (should succeed)
    print("\n\n🔹 TEST 4: Access protected endpoint WITH valid token")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(f"{BASE_URL}/api/pilots", json=pilot_data, headers=headers)
    print_response("Create Pilot WITH Token", response)
    
    if response.status_code == 201:
        print("\n✅ Successfully created pilot with authentication!")
        pilot_id = response.json().get('pilot', {}).get('id')
        return token, pilot_id
    else:
        print("\n❌ Failed to create pilot even with valid token!")
        return token, None
    
def test_public_endpoints():
    """Test that public endpoints work without authentication"""
    print("\n\n🔹 TEST 5: Access public endpoint (GET pilots) without token")
    response = requests.get(f"{BASE_URL}/api/pilots")
    print_response("Get All Pilots (Public)", response)
    
    if response.status_code == 200:
        print("\n✅ Public endpoint accessible without authentication!")
    else:
        print("\n❌ Public endpoint should be accessible!")

def test_update_and_delete(token, pilot_id):
    """Test UPDATE and DELETE operations with authentication"""
    if not pilot_id:
        print("\n⚠️  Skipping UPDATE/DELETE tests (no pilot ID)")
        return
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Test UPDATE
    print("\n\n🔹 TEST 6: Update pilot with authentication")
    update_data = {
        "rank": "General",
        "mission_success": 99
    }
    response = requests.put(f"{BASE_URL}/api/pilots/{pilot_id}", json=update_data, headers=headers)
    print_response("Update Pilot WITH Token", response)
    
    if response.status_code == 200:
        print("\n✅ Successfully updated pilot with authentication!")
    
    # Test DELETE
    print("\n\n🔹 TEST 7: Delete pilot with authentication")
    response = requests.delete(f"{BASE_URL}/api/pilots/{pilot_id}", headers=headers)
    print_response("Delete Pilot WITH Token", response)
    
    if response.status_code == 200:
        print("\n✅ Successfully deleted pilot with authentication!")

def test_invalid_token():
    """Test with invalid token"""
    print("\n\n🔹 TEST 8: Access protected endpoint with INVALID token")
    headers = {
        "Authorization": "Bearer invalid-token-12345"
    }
    pilot_data = {
        "name": "Invalid Test",
        "flight_years": 5,
        "rank": "Ensign",
        "mission_success": 50
    }
    response = requests.post(f"{BASE_URL}/api/pilots", json=pilot_data, headers=headers)
    print_response("Create Pilot with Invalid Token", response)
    
    if response.status_code == 401:
        print("\n✅ Invalid token correctly rejected!")
    else:
        print("\n❌ Security issue: Invalid token should be rejected!")

def main():
    """Run all authentication tests"""
    print("\n" + "="*60)
    print("🚀 JWT AUTHENTICATION TEST SUITE")
    print("="*60)
    print("\nMake sure the Flask app is running on http://localhost:5000")
    print("Press Ctrl+C to cancel, or Enter to continue...")
    input()
    
    try:
        # Test server is running
        response = requests.get(BASE_URL)
        print(f"\n✅ Server is running at {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to {BASE_URL}")
        print("Make sure to start the Flask app first: python app.py")
        return
    
    # Run tests
    result = test_authentication()
    if result:
        token, pilot_id = result
        test_public_endpoints()
        test_update_and_delete(token, pilot_id)
        test_invalid_token()
    
    print("\n\n" + "="*60)
    print("✅ TEST SUITE COMPLETED!")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
