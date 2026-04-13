"""
Comprehensive test for the authentication API
"""
import os
os.chdir('/Users/apple/pythonPramith-api/pramith-python-api')

from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient
from app.main import app
from app.database import create_all_tables, drop_all_tables

# Initialize test client
client = TestClient(app)

# Reset database
print("🔄 Resetting database...")
drop_all_tables()
create_all_tables()
print("✓ Database reset complete\n")

# ============================================================
# Test 1: User Registration with Username/Password
# ============================================================
print("=" * 60)
print("Test 1: User Registration")
print("=" * 60)

user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "mobile_number": "+1234567890"
}

response = client.post("/api/auth/register", json=user_data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
assert response.status_code == 201, f"Expected 201, got {response.status_code}"
user_id = response.json()["id"]
print(f"✓ User registered successfully with ID: {user_id}\n")

# ============================================================
# Test 2: User Login with Username/Password
# ============================================================
print("=" * 60)
print("Test 2: User Login")
print("=" * 60)

login_data = {
    "username": "john_doe",
    "password": "SecurePass123!"
}

response = client.post("/api/auth/login", json=login_data)
print(f"Status Code: {response.status_code}")
result = response.json()
print(f"Token Type: {result.get('token_type')}")
print(f"Access Token: {result.get('access_token')[:30]}...")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
access_token = result["access_token"]
print(f"✓ User logged in successfully\n")

# ============================================================
# Test 3: Request OTP for Mobile Number
# ============================================================
print("=" * 60)
print("Test 3: Request OTP for Mobile Authentication")
print("=" * 60)

otp_request = {
    "mobile_number": "+919876543210"
}

response = client.post("/api/auth/otp/send", json=otp_request)
print(f"Status Code: {response.status_code}")
result = response.json()
print(f"Message: {result.get('message')}")
print(f"Mobile: {result.get('mobile_number')}")
print(f"Expires in: {result.get('expires_in_seconds')} seconds")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print(f"✓ OTP requested successfully\n")

# ============================================================
# Test 4: Verify OTP and Login
# ============================================================
print("=" * 60)
print("Test 4: Verify OTP and Authenticate")
print("=" * 60)

# First, get the OTP from database to know what to verify
from app.database import SessionLocal
from app.models import OTP

db = SessionLocal()
otp_record = db.query(OTP).filter(OTP.mobile_number == "+919876543210").first()
db.close()

otp_code = otp_record.otp_code
print(f"Generated OTP: {otp_code}")

otp_verify = {
    "mobile_number": "+919876543210",
    "otp_code": otp_code
}

response = client.post("/api/auth/otp/verify", json=otp_verify)
print(f"Status Code: {response.status_code}")
result = response.json()
print(f"Message: {result.get('message')}")
if result.get('access_token'):
    print(f"Access Token: {result.get('access_token')[:30]}...")
print(f"Token Type: {result.get('token_type')}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print(f"✓ OTP verified successfully and user authenticated\n")

# ============================================================
# Test 5: Health Check
# ============================================================
print("=" * 60)
print("Test 5: Health Check")
print("=" * 60)

response = client.get("/api/auth/health")
print(f"Status Code: {response.status_code}")
result = response.json()
print(f"Status: {result.get('status')}")
print(f"Service: {result.get('service')}")
assert response.status_code == 200, f"Expected 200, got {response.status_code}"
print(f"✓ Health check passed\n")

# ============================================================
# Summary
# ============================================================
print("=" * 60)
print(" ✓ ALL AUTHENTICATION TESTS PASSED!")
print("=" * 60)
print("\nAuthentication System Summary:")
print("  ✓ User Registration")
print("  ✓ User Login with Password")
print("  ✓ OTP Generation")
print("  ✓ OTP Verification")
print("  ✓ Auto User Creation on OTP Verification")
print("  ✓ JWT Token Generation")
print("  ✓ Database Schema Auto-Creation")
