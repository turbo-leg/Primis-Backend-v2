from fastapi.testclient import TestClient
from app.core.config import settings
from app.models.attendance import AttendanceStatus

def test_mark_attendance(client: TestClient, db) -> None:
    # 1. Login
    login_data = {"username": "instructor_new@example.com", "password": "Password123!"}
    # Ensure user
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": "instructor_new@example.com", "password": "Password123!", "first_name": "Inst", "last_name": "Ructor", "role": "instructor"})
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
    from datetime import datetime, timedelta, timezone
    session_data = {
        "course_id": course_id, 
        "instructor_id": user_id, 
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }
    r = client.post(f"{settings.API_V1_STR}/classes/", headers=headers, json=session_data)
    session_id = r.json()["id"]

    # 5. Mark Attendance
    attendance_data = {
        "session_id": session_id,
        "student_id": user_id, 
        "status": AttendanceStatus.PRESENT
    }
    r = client.post(f"{settings.API_V1_STR}/attendance/", headers=headers, json=attendance_data)
    assert r.status_code == 200
    assert r.json()["status"] == "present"

    # 6. Read Session Attendance
    r = client.get(f"{settings.API_V1_STR}/attendance/session/{session_id}", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # 7. Read Student Attendance (Self)
    r = client.get(f"{settings.API_V1_STR}/attendance/student/{user_id}", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_attendance_permissions(client: TestClient, db) -> None:
    # Create a student user
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": "student@example.com", "password": "Password123!", "first_name": "Stu", "last_name": "Dent"})
    r = client.post(f"{settings.API_V1_STR}/auth/login", data={"username": "student@example.com", "password": "Password123!"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Try to mark attendance (should fail)
    attendance_data = {
        "session_id": 1,
        "student_id": 1, 
        "status": AttendanceStatus.PRESENT
    }
    r = client.post(f"{settings.API_V1_STR}/attendance/", headers=headers, json=attendance_data)
    assert r.status_code == 403
