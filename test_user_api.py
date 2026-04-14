#!/usr/bin/env python3
"""
Test script for User API endpoints
Run this script to test all user API functionality
"""

import requests
import json
from typing import Dict, Any
import time

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 5


class UserAPITester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.created_users = []
        self.session = requests.Session()
        
    def print_result(self, endpoint: str, method: str, status_code: int, success: bool, data: Dict[str, Any] = None):
        """Pretty print API test results"""
        status_indicator = "✓" if success else "✗"
        print(f"\n{status_indicator} [{method}] {endpoint}")
        print(f"  Status Code: {status_code}")
        if data:
            print(f"  Response: {json.dumps(data, indent=4, default=str)}")
    
    def test_create_user(self, user_data: Dict[str, Any]):
        """Test creating a new user"""
        endpoint = "/api/users"
        try:
            response = self.session.post(
                f"{self.base_url}{endpoint}",
                json=user_data,
                timeout=TIMEOUT
            )
            success = response.status_code == 201
            data = response.json() if response.text else None
            
            self.print_result(endpoint, "POST", response.status_code, success, data)
            
            if success and data:
                self.created_users.append(data)
                return data
            return None
        except Exception as e:
            print(f"✗ [POST] {endpoint}")
            print(f"  Error: {str(e)}")
            return None
    
    def test_get_all_users(self, skip: int = 0, limit: int = 10, role: str = None):
        """Test getting all users"""
        endpoint = "/api/users"
        params = {"skip": skip, "limit": limit}
        if role:
            params["role"] = role
        
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
    
    def test_get_user_by_id(self, user_id: str):
        """Test getting a user by ID"""
        endpoint = f"/api/users/{user_id}"
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
    
    def test_get_user_by_mobile(self, mobile: str):
        """Test getting a user by mobile number"""
        endpoint = f"/api/users/mobile/{mobile}"
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
    
    def test_update_user(self, user_id: str, update_data: Dict[str, Any]):
        """Test updating a user"""
        endpoint = f"/api/users/{user_id}"
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
    
    def test_verify_user(self, user_id: str):
        """Test verifying a user"""
        endpoint = f"/api/users/{user_id}/verify"
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
    
    def test_delete_user(self, user_id: str):
        """Test deleting a user"""
        endpoint = f"/api/users/{user_id}"
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
    
    def test_duplicate_mobile(self):
        """Test creating a user with duplicate mobile number"""
        print("\n" + "="*70)
        print("Testing Duplicate Mobile Detection")
        print("="*70)
        
        user_data = {
            "name": "Duplicate Test",
            "mobile": "9999999999",
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "role": "patient"
        }
        
        # Create first user
        print("\n→ Creating first user...")
        user1 = self.test_create_user(user_data)
        
        if user1:
            # Try to create second user with same mobile
            print("\n→ Attempting to create user with duplicate mobile...")
            user_data["email"] = "different@example.com"
            user2 = self.test_create_user(user_data)
            
            if user2 is None:
                print("✓ Duplicate mobile detection working correctly")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("USER API TEST SUITE")
        print("="*70)
        
        # Test 1: Create Users
        print("\n" + "="*70)
        print("1. Testing User Creation")
        print("="*70)
        
        users_to_create = [
            {
                "name": "John Doe",
                "mobile": "9876543210",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "patient"
            },
            {
                "name": "Dr. Jane Smith",
                "mobile": "9876543211",
                "email": "jane@example.com",
                "password": "drpassword123",
                "role": "doctor"
            },
            {
                "name": "Admin User",
                "mobile": "9876543212",
                "email": "admin@example.com",
                "password": "adminpass123",
                "role": "admin"
            }
        ]
        
        for user_data in users_to_create:
            print(f"\n→ Creating user: {user_data['name']}")
            self.test_create_user(user_data)
        
        # Test 2: Get All Users
        print("\n" + "="*70)
        print("2. Testing Get All Users")
        print("="*70)
        print("\n→ Retrieving all users...")
        self.test_get_all_users()
        
        # Test 3: Get Users by Role
        print("\n" + "="*70)
        print("3. Testing Get Users by Role")
        print("="*70)
        print("\n→ Retrieving doctors only...")
        self.test_get_all_users(role="doctor")
        
        # Test 4: Get User by ID
        if self.created_users:
            print("\n" + "="*70)
            print("4. Testing Get User by ID")
            print("="*70)
            user_id = self.created_users[0]["id"]
            print(f"\n→ Retrieving user by ID: {user_id}")
            self.test_get_user_by_id(user_id)
        
        # Test 5: Get User by Mobile
        if self.created_users:
            print("\n" + "="*70)
            print("5. Testing Get User by Mobile")
            print("="*70)
            mobile = self.created_users[0]["mobile"]
            print(f"\n→ Retrieving user by mobile: {mobile}")
            self.test_get_user_by_mobile(mobile)
        
        # Test 6: Update User
        if self.created_users:
            print("\n" + "="*70)
            print("6. Testing Update User")
            print("="*70)
            user_id = self.created_users[0]["id"]
            print(f"\n→ Updating user: {user_id}")
            self.test_update_user(user_id, {
                "name": "John Doe Updated",
                "role": "doctor"
            })
        
        # Test 7: Verify User
        if self.created_users:
            print("\n" + "="*70)
            print("7. Testing Verify User")
            print("="*70)
            user_id = self.created_users[0]["id"]
            print(f"\n→ Verifying user: {user_id}")
            self.test_verify_user(user_id)
        
        # Test 8: Duplicate Mobile Detection
        self.test_duplicate_mobile()
        
        # Test 9: Delete User
        if len(self.created_users) > 0:
            print("\n" + "="*70)
            print("8. Testing Delete User")
            print("="*70)
            user_id = self.created_users[-1]["id"]
            print(f"\n→ Deleting user: {user_id}")
            self.test_delete_user(user_id)
        
        print("\n" + "="*70)
        print("TEST SUITE COMPLETED")
        print("="*70 + "\n")


def main():
    """Main test runner"""
    print("\n🚀 Starting User API Tests")
    print(f"Target: {BASE_URL}")
    print("\nMake sure the FastAPI server is running!")
    print("Run: uvicorn app.main:app --reload")
    print("\nWaiting a moment before tests...\n")
    
    time.sleep(1)
    
    try:
        tester = UserAPITester()
        tester.run_all_tests()
    except Exception as e:
        print(f"\n❌ Test Error: {str(e)}")
        print("\nMake sure the FastAPI server is running on http://localhost:8000")


if __name__ == "__main__":
    main()
