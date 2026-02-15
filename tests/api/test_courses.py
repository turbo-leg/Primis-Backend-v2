from fastapi.testclient import TestClient
from app.core.config import settings

def test_create_course(client: TestClient, db) -> None:
    # 1. Login to get token
    login_data = {"username": "test@example.com", "password": "password123"}
    # Ensure user exists (relying on test database state or creating one if needed)
    # For robust tests, we should create a user here, but for now assuming the one from test_auth exists or we recreate
    # Let's create a fresh user for this test module to be safe
    user_data = {"email": "instructor@example.com", "password": "Password123!", "first_name": "Inst", "last_name": "Ructor"}
    client.post(f"{settings.API_V1_STR}/auth/register", json=user_data)
    
    r = client.post(f"{settings.API_V1_STR}/auth/login", data={"username": user_data["email"], "password": user_data["password"]})
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    # 2. Create Course
    course_data = {
        "title_en": "Intro to Calculus",
        "title_mn": "Calculus-iin undes",
        "description_en": "Basic calculus course",
        "price": 100.0,
        "is_published": True
    }
    r = client.post(f"{settings.API_V1_STR}/courses/", headers=headers, json=course_data)
    assert r.status_code == 200
    created_course = r.json()
    assert created_course["title_en"] == course_data["title_en"]
    assert "id" in created_course

def test_read_courses(client: TestClient) -> None:
    # Login
    login_data = {"username": "instructor@example.com", "password": "Password123!"}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    if r.status_code == 200:
        a_token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {a_token}"}
        
        r = client.get(f"{settings.API_V1_STR}/courses/", headers=headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
