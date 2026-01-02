import requests
import random
import string

BASE_URL = "http://localhost:8000"

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + "@test.com"

def test_registration_and_login():
    email = random_email()
    password = "testpassword123"

    print(f"Testing Registration for {email}...")
    reg_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": email, "password": password}
    )

    if reg_response.status_code == 201:
        print("Registration: SUCCESS")
        user_data = reg_response.json()
        print(f"User ID: {user_data['id']}")
    else:
        print(f"Registration: FAILED ({reg_response.status_code})")
        print(reg_response.text)
        return

    print("Testing Login...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": email, "password": password}
    )

    if login_response.status_code == 200:
        print("Login: SUCCESS")
        token_data = login_response.json()
        print(f"Token: {token_data['access_token'][:20]}...")
    else:
        print(f"Login: FAILED ({login_response.status_code})")
        print(login_response.text)

if __name__ == "__main__":
    test_registration_and_login()
