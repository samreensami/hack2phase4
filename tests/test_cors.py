"""
Quick CORS test between frontend and backend
"""
import requests
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("  Testing CORS: Frontend (3005) -> Backend (8000)")
print("=" * 60)

# Test 1: Backend health check
print("\n1. Testing Backend Health...")
try:
    response = requests.get("http://localhost:8000/")
    print(f"   ✅ Backend responding: {response.json()}")
except Exception as e:
    print(f"   ❌ Backend error: {e}")

# Test 2: CORS preflight simulation
print("\n2. Testing CORS Configuration...")
headers = {
    "Origin": "http://localhost:3005",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type"
}
try:
    response = requests.options("http://localhost:8000/auth/login", headers=headers)
    print(f"   ✅ CORS preflight OK: {response.status_code}")
    print(f"   Allowed Origin: {response.headers.get('access-control-allow-origin', 'Not set')}")
except Exception as e:
    print(f"   ❌ CORS error: {e}")

# Test 3: Actual API call from frontend origin
print("\n3. Testing Real API Call...")
headers = {"Origin": "http://localhost:3005", "Content-Type": "application/json"}
data = {"email": "test@example.com", "password": "test123"}
try:
    response = requests.post("http://localhost:8000/auth/register", json=data, headers=headers)
    if response.status_code in [201, 400]:  # 201 = created, 400 = already exists
        print(f"   ✅ API call successful: {response.status_code}")
        cors_header = response.headers.get('access-control-allow-origin')
        print(f"   CORS Header: {cors_header}")
        if cors_header == "http://localhost:3005":
            print("   ✅ CORS configured correctly for port 3005")
        else:
            print(f"   ⚠️  CORS might not include port 3005: {cors_header}")
    else:
        print(f"   ⚠️  Unexpected status: {response.status_code}")
except Exception as e:
    print(f"   ❌ API call error: {e}")

print("\n" + "=" * 60)
print("  CORS Test Complete")
print("=" * 60)
