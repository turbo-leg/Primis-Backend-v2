from fastapi.testclient import TestClient
from app.core.config import settings
from app.models.attendance import AttendanceStatus

def test_mark_attendance(client: TestClient, db) -> None:
    # 1. Login
    login_data = {"username": "instructor@example.com", "password": "Password123!"}
    # Ensure user
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": "instructor@example.com", "password": "Password123!", "first_name": "Inst", "last_name": "Ructor"})
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    a_token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    
    # 2. Get User ID
    r = client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    user_id = r.json()["id"]

    # 3. Create Course
    course_data = {"title_en": "Chem 101", "title_mn": "Chem 101", "price": 0.0}
    r = client.post(f"{settings.API_V1_STR}/courses/", headers=headers, json=course_data)
    course_id = r.json()["id"]

    # 4. Create Session
    session_data = {
        "course_id": course_id, 
        "instructor_id": user_id, 
        "start_time": "2026-02-14T10:00:00Z",
        "end_time": "2026-02-14T11:00:00Z"
    }
    r = client.post(f"{settings.API_V1_STR}/classes/", headers=headers, json=session_data)
    session_id = r.json()["id"]

    # 5. Mark Attendance
    attendance_data = {
        "session_id": session_id,
        "student_id": user_id, # Self attendance for simplicity in test
        "status": AttendanceStatus.PRESENT
    }
    r = client.post(f"{settings.API_V1_STR}/attendance/", headers=headers, json=attendance_data)
    assert r.status_code == 200
    assert r.json()["status"] == "present"
