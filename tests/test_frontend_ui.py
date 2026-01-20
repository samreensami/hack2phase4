"""
Test script to verify frontend UI pages are loading correctly
"""
import requests
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

FRONTEND_URL = "http://localhost:3000"

def test_page(url, page_name):
    """Test if a page loads and has content"""
    try:
        response = requests.get(url, timeout=30)  # Increased timeout for Next.js compilation
        if response.status_code == 200:
            print(f"✅ {page_name}: Loaded successfully (Status: {response.status_code})")
            # Check if it's HTML content
            if 'text/html' in response.headers.get('Content-Type', ''):
                print(f"   - Content Type: HTML")
                print(f"   - Content Size: {len(response.text)} bytes")
                return True
            else:
                print(f"   - Content Type: {response.headers.get('Content-Type')}")
                return True
        else:
            print(f"❌ {page_name}: Failed (Status: {response.status_code})")
            return False
    except requests.exceptions.Timeout:
        print(f"❌ {page_name}: Timeout (page took too long to load)")
        return False
    except Exception as e:
        print(f"❌ {page_name}: Error - {e}")
        return False

def main():
    print("=" * 70)
    print("  Frontend UI Test - Checking All Pages")
    print("=" * 70)
    print()

    pages = [
        (f"{FRONTEND_URL}/", "Home/Root Page"),
        (f"{FRONTEND_URL}/login", "Login Page"),
        (f"{FRONTEND_URL}/register", "Register Page"),
        (f"{FRONTEND_URL}/dashboard", "Dashboard Page (will redirect if not logged in)"),
    ]

    results = []
    for url, name in pages:
        print(f"\nTesting: {name}")
        print(f"URL: {url}")
        result = test_page(url, name)
        results.append((name, result))
        print()

    print("=" * 70)
    print("  Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Total: {passed}/{total} pages working correctly")

    if passed == total:
        print("\n🎉 All frontend pages are accessible!")
        print("\nYou can now:")
        print("  1. Go to http://localhost:3001/register to create an account")
        print("  2. Login at http://localhost:3001/login")
        print("  3. Manage your tasks at http://localhost:3001/dashboard")
    else:
        print("\n⚠️  Some pages had issues. Check the logs above.")

if __name__ == "__main__":
    main()
