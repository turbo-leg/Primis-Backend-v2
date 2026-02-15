from fastapi.testclient import TestClient
from app.core.config import settings

def test_enroll_course(client: TestClient, db) -> None:
    import time
    # 1. Login as Student
    email = f"enroll_student_{time.time()}@example.com"
    password = "Password123!"
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": email, "password": password, "first_name": "Enroll", "last_name": "Student", "role": "student"})
    r = client.post(f"{settings.API_V1_STR}/auth/login", data={"username": email, "password": password})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Course (as Instructor)
    instr_email = f"enroll_instr_{time.time()}@example.com"
    client.post(f"{settings.API_V1_STR}/auth/register", json={"email": instr_email, "password": password, "first_name": "Instr", "last_name": "Uctor", "role": "instructor"})
    r_instr = client.post(f"{settings.API_V1_STR}/auth/login", data={"username": instr_email, "password": password})
    instr_token = r_instr.json()["access_token"]
    instr_headers = {"Authorization": f"Bearer {instr_token}"}

    course_data = {"title_en": "Physics 101", "title_mn": "Physics 101", "price": 0.0}
    r = client.post(f"{settings.API_V1_STR}/courses/", headers=instr_headers, json=course_data)
    assert r.status_code == 200
    course_id = r.json()["id"]

    # 3. Enroll (as Student)
    enroll_data = {"course_id": course_id}
    r = client.post(f"{settings.API_V1_STR}/enrollments/", headers=headers, json=enroll_data)
    assert r.status_code == 200
    data = r.json()
    assert data["course_id"] == course_id
    assert data["payment_status"] == "unpaid"
    assert data["status"] == "active"

    # 4. Verify Duplicate Enrollment fails
    r = client.post(f"{settings.API_V1_STR}/enrollments/", headers=headers, json=enroll_data)
    assert r.status_code == 400

    # 5. Get My Enrollments
    r = client.get(f"{settings.API_V1_STR}/enrollments/me", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    assert data[0]["course_id"] == course_id

    # 6. Get Specific Enrollment
    enrollment_id = data[0]["id"]
    r = client.get(f"{settings.API_V1_STR}/enrollments/{enrollment_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == enrollment_id
