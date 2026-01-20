"""
Test script for registration and login flow
"""
import requests
import json
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("\n=== Testing Registration ===")
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "testuser@example.com",
        "password": "SecurePassword123"
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            user_data = response.json()
            print(f"✅ Registration Success!")
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            return True
        elif response.status_code == 400:
            print(f"⚠️  User already exists (expected if running multiple times)")
            return True
        else:
            print(f"❌ Registration Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\n=== Testing Login ===")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "testuser@example.com",  # OAuth2 uses 'username' field
        "password": "SecurePassword123"
    }

    try:
        response = requests.post(url, data=data)  # Note: form data, not JSON
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login Success!")
            print(f"   Access Token: {token_data['access_token'][:50]}...")
            print(f"   Token Type: {token_data['token_type']}")
            return token_data['access_token']
        else:
            print(f"❌ Login Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_create_task(token):
    """Test creating a task with JWT token"""
    print("\n=== Testing Task Creation ===")
    url = f"{BASE_URL}/dashboard/tasks/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": "Test Task from API",
        "description": "This task was created via the test script",
        "status": False,  # False = pending, True = completed
        "category": "testing"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            task_data = response.json()
            print(f"✅ Task Created Successfully!")
            print(f"   Task ID: {task_data['id']}")
            print(f"   Title: {task_data['title']}")
            print(f"   Status: {task_data['status']}")
            print(f"   Category: {task_data['category']}")
            return task_data['id']
        else:
            print(f"❌ Task Creation Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_tasks(token):
    """Test getting all tasks"""
    print("\n=== Testing Get All Tasks ===")
    url = f"{BASE_URL}/dashboard/tasks/"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Retrieved {len(tasks)} task(s)")
            for task in tasks:
                print(f"   - [{task['id']}] {task['title']} ({task['status']})")
            return True
        else:
            print(f"❌ Get Tasks Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("  Task Web App - Full Flow Test")
    print("=" * 60)

    # Test Registration
    if not test_registration():
        print("\n❌ Registration test failed. Stopping.")
        return

    # Test Login
    token = test_login()
    if not token:
        print("\n❌ Login test failed. Stopping.")
        return

    # Test Create Task
    task_id = test_create_task(token)
    if not task_id:
        print("\n❌ Task creation test failed. Stopping.")
        return

    # Test Get Tasks
    if not test_get_tasks(token):
        print("\n❌ Get tasks test failed.")
        return

    print("\n" + "=" * 60)
    print("  ✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nYour Task Web App is fully functional:")
    print("  - Backend API: http://localhost:8000")
    print("  - Frontend UI: http://localhost:3001")
    print("  - API Docs: http://localhost:8000/docs")
    print("\nYou can now:")
    print("  1. Register at http://localhost:3001/register")
    print("  2. Login at http://localhost:3001/login")
    print("  3. Manage tasks at http://localhost:3001/dashboard")

if __name__ == "__main__":
    main()