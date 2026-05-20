#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Docker
Tests all API endpoints with environment variables
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 10

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        self.test_data = {
            "user_id": None,
            "doctor_id": None,
            "appointment_id": None,
            "prescription_id": None,
            "payment_id": None,
            "access_token": None
        }

    def log(self, level: str, message: str):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def test(self, method: str, endpoint: str, name: str, 
              data: Optional[Dict] = None, expected_status: int = 200, required_fields: Optional[list] = None):
        """Execute a single API test"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Add auth token if available
        if self.test_data["access_token"]:
            headers["Authorization"] = f"Bearer {self.test_data['access_token']}"
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers, timeout=TIMEOUT)
            elif method == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=TIMEOUT)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=TIMEOUT)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=TIMEOUT)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Check status code
            success = response.status_code == expected_status
            
            # Check required fields
            if success and required_fields and response.text:
                try:
                    resp_data = response.json()
                    if isinstance(resp_data, dict):
                        missing_fields = [f for f in required_fields if f not in resp_data]
                        if missing_fields:
                            success = False
                            status_text = f"Missing fields: {missing_fields}"
                        else:
                            status_text = "✓ Pass"
                    else:
                        status_text = "✓ Pass"
                except:
                    status_text = "✓ Pass"
            else:
                status_text = "✓ Pass" if success else f"Expected {expected_status}, got {response.status_code}"
            
            # Store result
            color = Colors.GREEN if success else Colors.RED
            self.results.append({
                "test": name,
                "status": "PASS" if success else "FAIL",
                "method": method,
                "endpoint": endpoint,
                "status_code": response.status_code
            })
            
            print(f"{color}[{method:6}] {name:40} {response.status_code} - {status_text}{Colors.END}")
            
            return response if success else None
            
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}[{method:6}] {name:40} CONNECTION ERROR - API not accessible{Colors.END}")
            self.results.append({
                "test": name,
                "status": "FAIL",
                "method": method,
                "endpoint": endpoint,
                "error": "Connection error"
            })
            return None
        except Exception as e:
            print(f"{Colors.RED}[{method:6}] {name:40} ERROR - {str(e)}{Colors.END}")
            self.results.append({
                "test": name,
                "status": "FAIL",
                "method": method,
                "endpoint": endpoint,
                "error": str(e)
            })
            return None

    def run_health_checks(self):
        """Test health endpoints"""
        print(f"\n{Colors.BLUE}=== HEALTH CHECKS ==={Colors.END}")
        self.test("GET", "/health", "Root Health Check")
        self.test("GET", "/api/auth/health", "Auth Health Check")

    def run_auth_tests(self):
        """Test authentication endpoints"""
        print(f"\n{Colors.BLUE}=== AUTHENTICATION ==={Colors.END}")
        
        # Register user
        register_data = {
            "name": "Test User",
            "mobile": "+919876543210",
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "password": "TestPassword123!",
            "username": f"testuser_{int(datetime.now().timestamp())}",
            "role": "patient"
        }
        response = self.test("POST", "/api/auth/register", "Register User", register_data, 201, 
                           required_fields=["id", "email", "username"])
        if response:
            try:
                user_data = response.json()
                self.test_data["user_id"] = user_data.get("id")
            except:
                pass
        
        # Login
        login_data = {
            "username": register_data["username"],
            "password": register_data["password"]
        }
        response = self.test("POST", "/api/auth/login", "Login User", login_data, 200, 
                           required_fields=["access_token", "token_type"])
        if response:
            try:
                auth_data = response.json()
                self.test_data["access_token"] = auth_data.get("access_token")
            except:
                pass

    def run_user_tests(self):
        """Test user endpoints"""
        print(f"\n{Colors.BLUE}=== USER MANAGEMENT ==={Colors.END}")
        
        # Create user
        user_data = {
            "name": "Alice Smith",
            "mobile": f"+9198765432{int(datetime.now().timestamp()) % 100:02d}",
            "email": f"alice_{datetime.now().timestamp()}@example.com",
            "password": "password123",
            "role": "patient"
        }
        response = self.test("POST", "/api/users", "Create User", user_data, 201, 
                           required_fields=["id", "name", "email"])
        if response:
            try:
                user = response.json()
                self.test_data["user_id"] = user.get("id")
            except:
                pass
        
        # List users
        self.test("GET", "/api/users", "List All Users", expected_status=200)
        
        # Get user by ID (if we have one)
        if self.test_data["user_id"]:
            self.test("GET", f"/api/users/{self.test_data['user_id']}", "Get User by ID", expected_status=200)

    def run_doctor_tests(self):
        """Test doctor endpoints"""
        print(f"\n{Colors.BLUE}=== DOCTOR MANAGEMENT ==={Colors.END}")
        
        if not self.test_data["user_id"]:
            print(f"{Colors.YELLOW}Skipping doctor tests - no user ID available{Colors.END}")
            return
        
        # Create doctor
        doctor_data = {
            "user_id": self.test_data["user_id"],
            "specialization": "Cardiology",
            "experience": 10,
            "consultation_fee": 500.00
        }
        response = self.test("POST", "/api/doctors", "Create Doctor", doctor_data, 201,
                           required_fields=["id", "specialization"])
        if response:
            try:
                doctor = response.json()
                self.test_data["doctor_id"] = doctor.get("id")
            except:
                pass
        
        # List doctors
        self.test("GET", "/api/doctors", "List All Doctors", expected_status=200)
        
        # Get doctor by ID
        if self.test_data["doctor_id"]:
            self.test("GET", f"/api/doctors/{self.test_data['doctor_id']}", "Get Doctor by ID", expected_status=200)

    def run_appointment_tests(self):
        """Test appointment endpoints"""
        print(f"\n{Colors.BLUE}=== APPOINTMENT MANAGEMENT ==={Colors.END}")
        
        if not self.test_data["user_id"] or not self.test_data["doctor_id"]:
            print(f"{Colors.YELLOW}Skipping appointment tests - missing user or doctor ID{Colors.END}")
            return
        
        # Create appointment
        appointment_data = {
            "patient_id": self.test_data["user_id"],
            "doctor_id": self.test_data["doctor_id"],
            "appointment_date": "2026-05-01",
            "time_slot": "10:00-10:30",
            "notes": "Regular checkup"
        }
        response = self.test("POST", "/api/appointments", "Create Appointment", appointment_data, 201,
                           required_fields=["id", "status"])
        if response:
            try:
                appt = response.json()
                self.test_data["appointment_id"] = appt.get("id")
            except:
                pass
        
        # List appointments
        self.test("GET", "/api/appointments", "List All Appointments", expected_status=200)
        
        # Get appointment by ID
        if self.test_data["appointment_id"]:
            self.test("GET", f"/api/appointments/{self.test_data['appointment_id']}", "Get Appointment by ID", expected_status=200)

    def run_otp_tests(self):
        """Test OTP verification endpoints"""
        print(f"\n{Colors.BLUE}=== OTP VERIFICATION ==={Colors.END}")
        
        otp_data = {
            "mobile": "+919876543210",
            "otp": "123456",
            "expires_at": "2026-04-17T11:40:00"
        }
        self.test("POST", "/api/otp-verification", "Create OTP", otp_data, 201)
        self.test("GET", "/api/otp-verification", "List OTPs", expected_status=200)

    def run_payment_tests(self):
        """Test payment endpoints"""
        print(f"\n{Colors.BLUE}=== PAYMENT MANAGEMENT ==={Colors.END}")
        
        if not self.test_data["user_id"]:
            print(f"{Colors.YELLOW}Skipping payment tests - no user ID available{Colors.END}")
            return
        
        payment_data = {
            "user_id": self.test_data["user_id"],
            "amount": 500.00,
            "payment_method": "credit_card",
            "transaction_id": "TXN001234567"
        }
        response = self.test("POST", "/api/payments", "Create Payment", payment_data, 201)
        if response:
            try:
                payment = response.json()
                self.test_data["payment_id"] = payment.get("id")
            except:
                pass
        
        self.test("GET", "/api/payments", "List All Payments", expected_status=200)

    def print_summary(self):
        """Print test summary"""
        print(f"\n{Colors.BLUE}{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}{Colors.END}")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = total - passed
        
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {failed}{Colors.END}")
        
        if failed > 0:
            print(f"\n{Colors.YELLOW}Failed Tests:{Colors.END}")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']} ({result['method']} {result['endpoint']})")
        
        print(f"\n{'='*60}\n")

    def run_all_tests(self):
        """Run all test suites"""
        print(f"\n{Colors.BLUE}{'='*60}")
        print("PRAMITH API - COMPREHENSIVE TEST SUITE")
        print(f"Base URL: {self.base_url}")
        print(f"{'='*60}{Colors.END}\n")
        
        self.run_health_checks()
        self.run_auth_tests()
        self.run_user_tests()
        self.run_doctor_tests()
        self.run_appointment_tests()
        self.run_otp_tests()
        self.run_payment_tests()
        
        self.print_summary()
        
        # Return exit code
        return 0 if all(r["status"] == "PASS" for r in self.results) else 1

if __name__ == "__main__":
    tester = APITester(BASE_URL)
    exit_code = tester.run_all_tests()
    exit(exit_code)
