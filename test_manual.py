from app import app, mysql
import json

# Test direct model call
with app.app_context():
    try:
        from models import pilot
        result = pilot.get_all(mysql)
        print(f"Direct model call - Success! Got {len(result)} pilots")
    except Exception as e:
        print(f"Direct model call - Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

# Test via API
print("\n--- Testing API ---")
with app.test_client() as client:
    response = client.get('/api/pilots')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Data: {response.data.decode()}")
    else:
        print(f"Error: {response.data.decode()}")

