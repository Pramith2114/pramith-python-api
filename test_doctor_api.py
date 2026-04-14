#!/usr/bin/env python3
"""
Test script for Doctor API endpoints
Run this script to test all doctor API functionality
"""

import requests
import json
from typing import Dict, Any
import time
from uuid import UUID

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 5


class DoctorAPITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.created_users = []
        self.created_doctors = []
        self.session = requests.Session()
        
    def print_result(self, endpoint: str, method: str, status_code: int, success: bool, data: Dict[str, Any] = None):
        """Pretty print API test results"""
        status_indicator = "✓" if success else "✗"
        print(f"\n{status_indicator} [{method}] {endpoint}")
        print(f"  Status Code: {status_code}")
        if data:
            print(f"  Response: {json.dumps(data, indent=4, default=str)}")
    
    def create_test_user(self, name: str, role: str = "doctor"):
        """Create a test user for doctor profile"""
        user_data = {
            "name": name,
            "mobile": f"987654{len(self.created_users):04d}",
            "email": f"{name.lower().replace(' ', '')}@example.com",
            "password": "testpassword123",
            "role": role
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/users",
                json=user_data,
                timeout=TIMEOUT
            )
            if response.status_code == 201:
                user = response.json()
                self.created_users.append(user)
                return user
            return None
        except Exception as e:
            print(f"✗ Failed to create test user: {str(e)}")
            return None
    
    def test_create_doctor(self, user_id: str, specialization: str, experience: int, fee: float):
        """Test creating a new doctor"""
        endpoint = "/api/doctors"
        doctor_data = {
            "user_id": user_id,
            "specialization": specialization,
            "experience": experience,
            "consultation_fee": fee
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=doctor_data,
                timeout=TIMEOUT
            )
            success = response.status_code == 201
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "POST", response.status_code, success, data)
            
            if success and data:
                self.created_doctors.append(data)
                return data
            return None
        except Exception as e:
            print(f"✗ [POST] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_get_all_doctors(self, skip: int = 0, limit: int = 10, status: str = None):
        """Test getting all doctors"""
        endpoint = "/api/doctors"
        params = {"skip": skip, "limit": limit}
        if status:
            params["verification_status"] = status
        
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=TIMEOUT
            )
            success = response.status_code == 200
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "GET", response.status_code, success, data)
            return data
        except Exception as e:
            print(f"✗ [GET] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_get_doctor_by_id(self, doctor_id: str):
        """Test getting a doctor by ID"""
        endpoint = f"/api/doctors/{doctor_id}"
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                timeout=TIMEOUT
            )
            success = response.status_code == 200
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "GET", response.status_code, success, data)
            return data
        except Exception as e:
            print(f"✗ [GET] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_get_doctor_by_user(self, user_id: str):
        """Test getting a doctor by user ID"""
        endpoint = f"/api/doctors/user/{user_id}"
        try:
            response = self.session.get(
                f"{self.base_url}{endpoint}",
                timeout=TIMEOUT
            )
            success = response.status_code == 200
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "GET", response.status_code, success, data)
            return data
        except Exception as e:
            print(f"✗ [GET] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_update_doctor(self, doctor_id: str, update_data: Dict[str, Any]):
        """Test updating a doctor"""
        endpoint = f"/api/doctors/{doctor_id}"
        try:
            response = self.session.put(
                f"{self.base_url}{endpoint}",
                json=update_data,
                timeout=TIMEOUT
            )
            success = response.status_code == 200
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "PUT", response.status_code, success, data)
            return data
        except Exception as e:
            print(f"✗ [PUT] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_approve_doctor(self, doctor_id: str):
        """Test approving a doctor"""
        endpoint = f"/api/doctors/{doctor_id}/approve"
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                timeout=TIMEOUT
            )
            success = response.status_code == 200
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "POST", response.status_code, success, data)
            return data
        except Exception as e:
            print(f"✗ [POST] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_reject_doctor(self, doctor_id: str):
        """Test rejecting a doctor"""
        endpoint = f"/api/doctors/{doctor_id}/reject"
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                timeout=TIMEOUT
            )
            success = response.status_code == 200
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "POST", response.status_code, success, data)
            return data
        except Exception as e:
            print(f"✗ [POST] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_delete_doctor(self, doctor_id: str):
        """Test deleting a doctor"""
        endpoint = f"/api/doctors/{doctor_id}"
        try:
            response = self.session.delete(
                f"{self.base_url}{endpoint}",
                timeout=TIMEOUT
            )
            success = response.status_code == 204
            
            self.print_result(endpoint, "DELETE", response.status_code, success)
            return success
        except Exception as e:
            print(f"✗ [DELETE] {endpoint}")
            print(f"  Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("DOCTOR API TEST SUITE")
        print("="*70)
        
        # Test 1: Create Test Users
        print("\n" + "="*70)
        print("1. Creating Test Users")
        print("="*70)
        
        test_users = [
            ("Dr. John Smith", "doctor"),
            ("Dr. Jane Doe", "doctor"),
            ("Dr. Mike Johnson", "doctor"),
        ]
        
        for name, role in test_users:
            print(f"\n→ Creating user: {name}")
            user = self.create_test_user(name, role)
            if user:
                print(f"  Created: {user['id']}")
        
        # Test 2: Create Doctor Profiles
        print("\n" + "="*70)
        print("2. Creating Doctor Profiles")
        print("="*70)
        
        if self.created_users:
            doctors_data = [
                ("Cardiology", 5, 500.00),
                ("Pediatrics", 10, 400.00),
                ("Orthopedics", 8, 600.00),
            ]
            
            for i, (spec, xp, fee) in enumerate(doctors_data):
                if i < len(self.created_users):
                    user = self.created_users[i]
                    print(f"\n→ Creating doctor profile for {user['name']}")
                    doctor = self.test_create_doctor(
                        user['id'],
                        specialization=spec,
                        experience=xp,
                        fee=fee
                    )
        
        # Test 3: Get All Doctors
        print("\n" + "="*70)
        print("3. Getting All Doctors")
        print("="*70)
        print("\n→ Retrieving all doctors...")
        self.test_get_all_doctors()
        
        # Test 4: Get Doctor by ID
        if self.created_doctors:
            print("\n" + "="*70)
            print("4. Getting Doctor by ID")
            print("="*70)
            doctor_id = self.created_doctors[0]["id"]
            print(f"\n→ Retrieving doctor by ID: {doctor_id}")
            self.test_get_doctor_by_id(doctor_id)
        
        # Test 5: Get Doctor by User ID
        if self.created_doctors:
            print("\n" + "="*70)
            print("5. Getting Doctor by User ID")
            print("="*70)
            user_id = self.created_doctors[0]["user_id"]
            print(f"\n→ Retrieving doctor by user ID: {user_id}")
            self.test_get_doctor_by_user(user_id)
        
        # Test 6: Filter by Verification Status
        print("\n" + "="*70)
        print("6. Filtering by Verification Status")
        print("="*70)
        print("\n→ Getting pending doctors...")
        self.test_get_all_doctors(status="pending")
        
        # Test 7: Update Doctor
        if self.created_doctors:
            print("\n" + "="*70)
            print("7. Updating Doctor Profile")
            print("="*70)
            doctor_id = self.created_doctors[0]["id"]
            print(f"\n→ Updating doctor: {doctor_id}")
            self.test_update_doctor(doctor_id, {
                "experience": 12,
                "consultation_fee": 600.00
            })
        
        # Test 8: Approve Doctor
        if self.created_doctors:
            print("\n" + "="*70)
            print("8. Approving Doctor")
            print("="*70)
            doctor_id = self.created_doctors[0]["id"]
            print(f"\n→ Approving doctor: {doctor_id}")
            self.test_approve_doctor(doctor_id)
        
        # Test 9: Get Approved Doctors
        print("\n" + "="*70)
        print("9. Getting Approved Doctors")
        print("="*70)
        print("\n→ Retrieving approved doctors...")
        self.test_get_all_doctors(status="approved")
        
        # Test 10: Reject Doctor
        if len(self.created_doctors) > 1:
            print("\n" + "="*70)
            print("10. Rejecting Doctor")
            print("="*70)
            doctor_id = self.created_doctors[1]["id"]
            print(f"\n→ Rejecting doctor: {doctor_id}")
            self.test_reject_doctor(doctor_id)
        
        # Test 11: Delete Doctor
        if len(self.created_doctors) > 2:
            print("\n" + "="*70)
            print("11. Deleting Doctor")
            print("="*70)
            doctor_id = self.created_doctors[2]["id"]
            print(f"\n→ Deleting doctor: {doctor_id}")
            self.test_delete_doctor(doctor_id)
        
        print("\n" + "="*70)
        print("TEST SUITE COMPLETED")
        print("="*70 + "\n")


def main():
    """Main test runner"""
    print("\n🚀 Starting Doctor API Tests")
    print(f"Target: {BASE_URL}")
    print("\nMake sure the FastAPI server is running!")
    print("Run: uvicorn app.main:app --reload")
    print("\nWaiting a moment before tests...\n")
    
    time.sleep(1)
    
    try:
        tester = DoctorAPITester()
        tester.run_all_tests()
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("\nMake sure the FastAPI server is running on http://localhost:8000")


if __name__ == "__main__":
    main()
