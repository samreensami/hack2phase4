import requests
import random
import string

BASE_URL = "http://localhost:8000"

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + "@test.com"

def test_task_lifecycle():
    email = random_email()
    password = "password123"

    # 1. Register and Login
    requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    login_res = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Task
    print("Testing Create Task...")
    create_res = requests.post(
        f"{BASE_URL}/tasks/",
        json={"title": "Test Task", "description": "Testing CRUD", "category": "Work"},
        headers=headers
    )
    task_id = create_res.json()["id"]
    print(f"Create: SUCCESS (ID: {task_id})")

    # 3. Get Tasks
    print("Testing Get Tasks...")
    get_res = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    tasks = get_res.json()
    if any(t["id"] == task_id for t in tasks):
        print(f"Get: SUCCESS (Found {len(tasks)} tasks)")

    # 4. Update Task
    print("Testing Update Task...")
    update_res = requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json={"title": "Updated Task", "status": True},
        headers=headers
    )
    if update_res.json()["status"] == True:
        print("Update: SUCCESS")

    # 5. Delete Task
    print("Testing Delete Task...")
    del_res = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    if del_res.status_code == 204:
        print("Delete: SUCCESS")

if __name__ == "__main__":
    test_task_lifecycle()
