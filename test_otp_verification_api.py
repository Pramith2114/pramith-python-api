"""
Test suite for OTP Verification API
Tests all CRUD operations and verification functionality
"""
import requests
import json
from datetime import datetime, timedelta
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

# OTP Verification endpoints
OTP_VERIFICATION_BASE = f"{BASE_URL}/api/otp-verification"

def test_create_otp():
    """Test creating a new OTP verification record"""
    print("\n" + "="*60)
    print("TEST: Create OTP Verification")
    print("="*60)
    
    # Generate OTP expiration time (valid for 10 minutes)
    expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    
    payload = {
        "mobile": "+919876543210",
        "otp": "123456",
        "expires_at": expires_at
    }
    
    response = requests.post(OTP_VERIFICATION_BASE, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json() if response.status_code == 201 else None


def test_get_all_otp():
    """Test retrieving all OTP verification records"""
    print("\n" + "="*60)
    print("TEST: Get All OTP Verification Records")
    print("="*60)
    
    response = requests.get(OTP_VERIFICATION_BASE)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_otp_by_mobile(mobile: str):
    """Test retrieving OTP records by mobile number"""
    print("\n" + "="*60)
    print(f"TEST: Get OTP by Mobile ({mobile})")
    print("="*60)
    
    response = requests.get(f"{OTP_VERIFICATION_BASE}/by-mobile/{mobile}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_verify_otp(mobile: str, otp: str):
    """Test OTP verification"""
    print("\n" + "="*60)
    print(f"TEST: Verify OTP")
    print("="*60)
    
    payload = {
        "mobile": mobile,
        "otp": otp
    }
    
    response = requests.post(f"{OTP_VERIFICATION_BASE}/verify", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_get_otp_by_id(otp_id: str):
    """Test retrieving a specific OTP record"""
    print("\n" + "="*60)
    print(f"TEST: Get OTP by ID ({otp_id})")
    print("="*60)
    
    response = requests.get(f"{OTP_VERIFICATION_BASE}/{otp_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_filter_otp_by_status(is_verified: bool):
    """Test filtering OTP records by verification status"""
    print("\n" + "="*60)
    print(f"TEST: Filter OTP by Verification Status (is_verified={is_verified})")
    print("="*60)
    
    response = requests.get(f"{OTP_VERIFICATION_BASE}?is_verified={is_verified}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_update_otp(otp_id: str):
    """Test updating an OTP record"""
    print("\n" + "="*60)
    print(f"TEST: Update OTP ({otp_id})")
    print("="*60)
    
    payload = {
        "is_verified": True
    }
    
    response = requests.put(f"{OTP_VERIFICATION_BASE}/{otp_id}", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_delete_otp(otp_id: str):
    """Test deleting an OTP record"""
    print("\n" + "="*60)
    print(f"TEST: Delete OTP ({otp_id})")
    print("="*60)
    
    response = requests.delete(f"{OTP_VERIFICATION_BASE}/{otp_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text if response.text else 'No content (204)'}")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("OTP VERIFICATION API TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Create OTP
        otp_record = test_create_otp()
        
        if otp_record:
            otp_id = otp_record.get('id')
            mobile = otp_record.get('mobile')
            otp = otp_record.get('otp')
            
            # Wait a moment
            time.sleep(1)
            
            # Test 2: Get all OTPs
            test_get_all_otp()
            
            # Test 3: Get OTP by ID
            test_get_otp_by_id(otp_id)
            
            # Test 4: Get OTP by mobile
            test_get_otp_by_mobile(mobile)
            
            # Test 5: Filter by status (unverified)
            test_filter_otp_by_status(False)
            
            # Test 6: Verify OTP
            test_verify_otp(mobile, otp)
            
            # Test 7: Filter by status (verified)
            test_filter_otp_by_status(True)
            
            # Test 8: Update OTP
            new_expires = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
            test_update_otp(otp_id)
            
            # Test 9: Test invalid OTP
            test_verify_otp(mobile, "000000")
            
            # Create another OTP for deletion test
            expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
            payload = {
                "mobile": "+919876543211",
                "otp": "654321",
                "expires_at": expires_at
            }
            response = requests.post(OTP_VERIFICATION_BASE, json=payload)
            if response.status_code == 201:
                delete_id = response.json().get('id')
                test_delete_otp(delete_id)
            
            print("\n" + "="*60)
            print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
            print("="*60)
        else:
            print("✗ Failed to create initial OTP record")
            
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("Make sure the API server is running at http://localhost:8000")


if __name__ == "__main__":
    run_all_tests()
