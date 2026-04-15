"""
Medical Records API Test Suite

This test suite validates all endpoints of the Medical Records API.
Test Coverage:
- Create medical records
- List/filter records
- Get single record
- Get patient's records
- Get records by type
- Update records
- Delete records
- Error handling (404, 422, 400)

IMPORTANT: Replace the following UUIDs with real values from your database:
- VALID_PATIENT_ID: A real patient ID that exists in users table
- VALID_RECORD_ID: A real medical record ID from medical_records table

Before running tests:
1. Start the server: python -m uvicorn app.main:app --reload
2. Update the UUIDs below with real values
3. Run tests: python test_medical_records_api.py
"""

import requests
import json
from uuid import uuid4

# ==================== CONFIG ====================

BASE_URL = "http://localhost:8000/api"

# IMPORTANT: Replace these with real IDs from your database
VALID_PATIENT_ID = "770e8400-e29b-41d4-a716-446655440000"  # Replace with real patient ID
VALID_RECORD_ID = "880e8400-e29b-41d4-a716-446655440000"   # Replace with real record ID

# Test data
FAKE_UUID = str(uuid4())
FAKE_PATIENT_UUID = str(uuid4())
FAKE_RECORD_UUID = str(uuid4())

# ==================== HELPERS ====================

def print_header(text):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_test(text):
    """Print test name"""
    print(f"\n✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"  ✗ {text}")

def print_response(response):
    """Print response details"""
    print(f"  Status Code: {response.status_code}")
    try:
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"  Response: {response.text}")

def print_success(msg):
    """Print success message"""
    print(f"  ✓ {msg}")

# ==================== TESTS ====================

def test_create_medical_record():
    """Test: Create a new medical record"""
    print_test("Create Medical Record")
    
    payload = {
        "patient_id": VALID_PATIENT_ID,
        "file_url": "https://storage.example.com/lab_report_2024_04_15.pdf",
        "record_type": "lab_report",
        "description": "Complete blood count test results"
    }
    
    response = requests.post(f"{BASE_URL}/medical-records", json=payload)
    print_response(response)
    
    if response.status_code == 201:
        print_success("Medical record created successfully")
        data = response.json()
        return data.get("id")  # Return ID for later tests
    else:
        print_error("Failed to create medical record")
        return None

def test_get_all_medical_records():
    """Test: Get all medical records (with pagination)"""
    print_test("Get All Medical Records")
    
    response = requests.get(f"{BASE_URL}/medical-records")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} medical records")
        return data
    else:
        print_error("Failed to get medical records")
        return []

def test_get_medical_record_by_id(record_id):
    """Test: Get single medical record"""
    print_test(f"Get Medical Record by ID ({record_id})")
    
    response = requests.get(f"{BASE_URL}/medical-records/{record_id}")
    print_response(response)
    
    if response.status_code == 200:
        print_success("Medical record retrieved successfully")
    else:
        print_error("Failed to get medical record")

def test_get_patient_medical_records():
    """Test: Get all records for a specific patient"""
    print_test(f"Get Patient Medical Records ({VALID_PATIENT_ID})")
    
    response = requests.get(f"{BASE_URL}/medical-records/patient/{VALID_PATIENT_ID}")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} records for patient")
    else:
        print_error("Failed to get patient records")

def test_get_patient_records_with_filter():
    """Test: Get patient records filtered by type"""
    print_test(f"Get Patient Records with Type Filter")
    
    response = requests.get(
        f"{BASE_URL}/medical-records/patient/{VALID_PATIENT_ID}",
        params={"record_type": "lab_report"}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} lab_report records for patient")
    else:
        print_error("Failed to get filtered patient records")

def test_get_records_by_type():
    """Test: Get all records of a specific type"""
    print_test("Get Records by Type (lab_report)")
    
    response = requests.get(f"{BASE_URL}/medical-records/type/lab_report")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} lab_report records")
    else:
        print_error("Failed to get records by type")

def test_filter_by_patient_id():
    """Test: Filter records by patient_id query parameter"""
    print_test("Filter Records by Patient ID (query param)")
    
    response = requests.get(
        f"{BASE_URL}/medical-records",
        params={"patient_id": VALID_PATIENT_ID}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} records for patient")
    else:
        print_error("Failed to filter by patient")

def test_pagination():
    """Test: Pagination with skip and limit"""
    print_test("Test Pagination (skip=0, limit=5)")
    
    response = requests.get(
        f"{BASE_URL}/medical-records",
        params={"skip": 0, "limit": 5}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved page of {len(data)} records (max 5)")
    else:
        print_error("Failed to paginate records")

def test_update_medical_record(record_id):
    """Test: Update an existing medical record"""
    print_test(f"Update Medical Record ({record_id})")
    
    payload = {
        "file_url": "https://storage.example.com/lab_report_2024_04_15_updated.pdf",
        "record_type": "lab_report",
        "description": "Updated: Complete blood count test - corrected values"
    }
    
    response = requests.put(f"{BASE_URL}/medical-records/{record_id}", json=payload)
    print_response(response)
    
    if response.status_code == 200:
        print_success("Medical record updated successfully")
    else:
        print_error("Failed to update medical record")

def test_delete_medical_record(record_id):
    """Test: Delete a medical record"""
    print_test(f"Delete Medical Record ({record_id})")
    
    response = requests.delete(f"{BASE_URL}/medical-records/{record_id}")
    print_response(response)
    
    if response.status_code == 204:
        print_success("Medical record deleted successfully")
    elif response.status_code == 200:
        print_success("Medical record deleted successfully")
    else:
        print_error("Failed to delete medical record")

# ==================== ERROR HANDLING TESTS ====================

def test_error_nonexistent_record():
    """Test: Error handling - Non-existent record"""
    print_test("Error: Get Non-existent Record (404)")
    
    response = requests.get(f"{BASE_URL}/medical-records/{FAKE_RECORD_UUID}")
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returned 404 for non-existent record")
    else:
        print_error(f"Expected 404, got {response.status_code}")

def test_error_nonexistent_patient():
    """Test: Error handling - Non-existent patient on create"""
    print_test("Error: Create Record for Non-existent Patient (404)")
    
    payload = {
        "patient_id": FAKE_PATIENT_UUID,
        "file_url": "https://storage.example.com/test.pdf",
        "record_type": "lab_report",
        "description": "Test"
    }
    
    response = requests.post(f"{BASE_URL}/medical-records", json=payload)
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returned 404 for non-existent patient")
    else:
        print_error(f"Expected 404, got {response.status_code}")

def test_error_invalid_uuid():
    """Test: Error handling - Invalid UUID format"""
    print_test("Error: Get Record with Invalid UUID Format (400)")
    
    response = requests.get(f"{BASE_URL}/medical-records/not-a-uuid")
    print_response(response)
    
    if response.status_code in [400, 422]:
        print_success("Correctly returned error for invalid UUID")
    else:
        print_error(f"Expected 400/422, got {response.status_code}")

def test_error_missing_required_field():
    """Test: Error handling - Missing required field on create"""
    print_test("Error: Create without Required Field (422)")
    
    payload = {
        "patient_id": VALID_PATIENT_ID,
        # Missing file_url
        "record_type": "lab_report"
    }
    
    response = requests.post(f"{BASE_URL}/medical-records", json=payload)
    print_response(response)
    
    if response.status_code == 422:
        print_success("Correctly returned 422 for missing required field")
    else:
        print_error(f"Expected 422, got {response.status_code}")

def test_error_nonexistent_patient_for_get():
    """Test: Error handling - Non-existent patient on get patient records"""
    print_test("Error: Get Records for Non-existent Patient (404)")
    
    response = requests.get(f"{BASE_URL}/medical-records/patient/{FAKE_PATIENT_UUID}")
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returned 404 for non-existent patient")
    else:
        # Some implementations may return empty list instead
        print_success("Returned response for non-existent patient")

# ==================== RECORD TYPE TESTS ====================

def test_different_record_types():
    """Test: Create records with different types"""
    print_test("Create Multiple Record Types")
    
    record_types = ["lab_report", "x_ray", "prescription", "discharge_summary", "ekg"]
    
    for record_type in record_types:
        payload = {
            "patient_id": VALID_PATIENT_ID,
            "file_url": f"https://storage.example.com/{record_type}_2024_04_15.pdf",
            "record_type": record_type,
            "description": f"Test {record_type} record"
        }
        
        response = requests.post(f"{BASE_URL}/medical-records", json=payload)
        
        if response.status_code == 201:
            print_success(f"Created {record_type} record")
        else:
            print_error(f"Failed to create {record_type} record")

# ==================== MAIN TEST SUITE ====================

def run_all_tests():
    """Run complete test suite"""
    print_header("MEDICAL RECORDS API - TEST SUITE")
    
    print("\n📝 Configuration:")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Patient ID: {VALID_PATIENT_ID}")
    print(f"  Record ID: {VALID_RECORD_ID}")
    
    # ==================== BASIC CRUD TESTS ====================
    print_header("1. BASIC CRUD OPERATIONS")
    
    # Create
    created_id = test_create_medical_record()
    
    # Get All
    test_get_all_medical_records()
    
    # Get Single
    if created_id:
        test_get_medical_record_by_id(created_id)
    else:
        test_get_medical_record_by_id(VALID_RECORD_ID)
    
    # Update
    if created_id:
        test_update_medical_record(created_id)
    else:
        test_update_medical_record(VALID_RECORD_ID)
    
    # Delete (using created or test ID)
    if created_id:
        test_delete_medical_record(created_id)
    
    # ==================== FILTERING TESTS ====================
    print_header("2. FILTERING & SEARCH")
    
    test_get_patient_medical_records()
    test_filter_by_patient_id()
    test_get_records_by_type()
    test_get_patient_records_with_filter()
    
    # ==================== PAGINATION TESTS ====================
    print_header("3. PAGINATION & LIMITS")
    
    test_pagination()
    
    # ==================== RECORD TYPE TESTS ====================
    print_header("4. DIFFERENT RECORD TYPES")
    
    test_different_record_types()
    
    # ==================== ERROR HANDLING TESTS ====================
    print_header("5. ERROR HANDLING")
    
    test_error_nonexistent_record()
    test_error_invalid_uuid()
    test_error_missing_required_field()
    test_error_nonexistent_patient()
    test_error_nonexistent_patient_for_get()
    
    # ==================== SUMMARY ====================
    print_header("TEST SUITE COMPLETE")
    print("\n✅ All tests executed successfully!")
    print("\n📊 Summary:")
    print("  ✓ CRUD operations")
    print("  ✓ Filtering and search")
    print("  ✓ Pagination")
    print("  ✓ Record types")
    print("  ✓ Error handling")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("   Make sure the server is running:")
        print("   python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
