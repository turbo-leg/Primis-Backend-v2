from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.core.config import settings

def test_create_class_session(client: TestClient, db) -> None:
    # 1. Login
    login_data = {"username": "instructor@example.com", "password": "password123"}
    # Ensure user exists (relying on previous tests or DB state)
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": "instructor@example.com", "password": "password123", "first_name": "Inst", "last_name": "Ructor"})
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    a_token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    
    # 2. Get User ID (Need it for instructor_id)
    r = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    user_id = r.json()["id"]

    # 3. Create Course (Need it for course_id)
    course_data = {
        "title_en": "Math 101",
        "title_mn": "Math 101",
        "price": 50.0
    }
    r = client.post(f"{settings.API_V1_STR}/courses/", headers=headers, json=course_data)
    course_id = r.json()["id"]

    # 4. Create Session
    session_data = {
        "course_id": course_id,
        "instructor_id": user_id,
        "name": "Lecture 1",
        "start_time": datetime.utcnow().isoformat(),
        "end_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "location": "Room 101"
    }
    r = client.post(f"{settings.API_V1_STR}/classes/", headers=headers, json=session_data)
    assert r.status_code == 200
    created_session = r.json()
    assert created_session["name"] == session_data["name"]
    assert created_session["course_id"] == course_id

def test_read_sessions(client: TestClient) -> None:
    login_data = {"username": "instructor@example.com", "password": "password123"}
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    if r.status_code == 200:
        a_token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {a_token}"}
        
        r = client.get(f"{settings.API_V1_STR}/classes/", headers=headers)
        assert r.status_code == 200
        assert isinstance(r.json(), list)
