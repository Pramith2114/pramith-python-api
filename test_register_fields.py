import os
os.chdir('/Users/apple/pythonPramith-api/pramith-python-api')

from fastapi.testclient import TestClient
from app.main import app
from app.database import create_all_tables, drop_all_tables, SessionLocal
from app.models import User

client = TestClient(app)

# Reset DB
drop_all_tables()
create_all_tables()


def test_register_persists_name_and_role():
    payload = {
        "name": "priya",
        "mobile": "9876543212",
        "email": "priya@gmail.com",
        "role": "doctor",
        "password": "priya123",
        "username": "priya",
        "mobile_number": "9876543212"
    }

    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 201, resp.text
    data = resp.json()

    # Response should reflect name and role
    assert data.get('name') == 'priya', f"Expected name 'priya' in response, got {data.get('name')}"
    assert data.get('role') == 'doctor', f"Expected role 'doctor' in response, got {data.get('role')}"

    # Verify in DB
    db = SessionLocal()
    user = db.query(User).filter(User.username == 'priya').first()
    assert user is not None, "User not found in DB"
    assert user.name == 'priya', f"DB name mismatch: {user.name}"
    assert user.role == 'doctor', f"DB role mismatch: {user.role}"
    db.close()
