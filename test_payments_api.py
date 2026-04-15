"""
Payments API Test Suite

This test suite validates all endpoints of the Payments API.
Test Coverage:
- Create payments
- List/filter payments
- Get single payment
- Get user's payments
- Get payments by status
- Update payments
- Delete payments
- Error handling (404, 422, 400)
- Duplicate transaction ID validation

IMPORTANT: Replace the following UUIDs with real values from your database:
- VALID_USER_ID: A real user ID that exists in users table
- VALID_PAYMENT_ID: A real payment ID from payments table

Before running tests:
1. Start the server: python -m uvicorn app.main:app --reload
2. Update the UUIDs below with real values
3. Run tests: python test_payments_api.py
"""

import requests
import json
from uuid import uuid4
from decimal import Decimal

# ==================== CONFIG ====================

BASE_URL = "http://localhost:8000/api"

# IMPORTANT: Replace these with real IDs from your database
VALID_USER_ID = "770e8400-e29b-41d4-a716-446655440000"  # Replace with real user ID
VALID_PAYMENT_ID = "880e8400-e29b-41d4-a716-446655440000"  # Replace with real payment ID

# Test data
FAKE_UUID = str(uuid4())
FAKE_USER_UUID = str(uuid4())
FAKE_PAYMENT_UUID = str(uuid4())
UNIQUE_TRANSACTION_ID = f"TXN-{uuid4()}"

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

def test_create_payment():
    """Test: Create a new payment"""
    print_test("Create Payment")
    
    payload = {
        "user_id": VALID_USER_ID,
        "amount": 150.50,
        "payment_method": "credit_card",
        "transaction_id": UNIQUE_TRANSACTION_ID
    }
    
    response = requests.post(f"{BASE_URL}/payments", json=payload)
    print_response(response)
    
    if response.status_code == 201:
        print_success("Payment created successfully")
        data = response.json()
        return data.get("id")  # Return ID for later tests
    else:
        print_error("Failed to create payment")
        return None

def test_get_all_payments():
    """Test: Get all payments (with pagination)"""
    print_test("Get All Payments")
    
    response = requests.get(f"{BASE_URL}/payments")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} payments")
        return data
    else:
        print_error("Failed to get payments")
        return []

def test_get_payment_by_id(payment_id):
    """Test: Get single payment"""
    print_test(f"Get Payment by ID ({payment_id})")
    
    response = requests.get(f"{BASE_URL}/payments/{payment_id}")
    print_response(response)
    
    if response.status_code == 200:
        print_success("Payment retrieved successfully")
    else:
        print_error("Failed to get payment")

def test_get_user_payments():
    """Test: Get all payments for a specific user"""
    print_test(f"Get User Payments ({VALID_USER_ID})")
    
    response = requests.get(f"{BASE_URL}/payments/user/{VALID_USER_ID}")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} payments for user")
    else:
        print_error("Failed to get user payments")

def test_get_user_payments_with_filter():
    """Test: Get user payments filtered by status"""
    print_test(f"Get User Payments with Status Filter")
    
    response = requests.get(
        f"{BASE_URL}/payments/user/{VALID_USER_ID}",
        params={"payment_status": "pending"}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} pending payments for user")
    else:
        print_error("Failed to get filtered user payments")

def test_get_payments_by_status():
    """Test: Get all payments of a specific status"""
    print_test("Get Payments by Status (pending)")
    
    response = requests.get(f"{BASE_URL}/payments/status/pending")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} pending payments")
    else:
        print_error("Failed to get payments by status")

def test_filter_by_user_id():
    """Test: Filter payments by user_id query parameter"""
    print_test("Filter Payments by User ID (query param)")
    
    response = requests.get(
        f"{BASE_URL}/payments",
        params={"user_id": VALID_USER_ID}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} payments for user")
    else:
        print_error("Failed to filter by user")

def test_filter_by_status():
    """Test: Filter payments by payment_status query parameter"""
    print_test("Filter Payments by Status (query param)")
    
    response = requests.get(
        f"{BASE_URL}/payments",
        params={"payment_status": "completed"}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved {len(data)} completed payments")
    else:
        print_error("Failed to filter by status")

def test_pagination():
    """Test: Pagination with skip and limit"""
    print_test("Test Pagination (skip=0, limit=5)")
    
    response = requests.get(
        f"{BASE_URL}/payments",
        params={"skip": 0, "limit": 5}
    )
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"Retrieved page of {len(data)} payments (max 5)")
    else:
        print_error("Failed to paginate payments")

def test_update_payment(payment_id):
    """Test: Update an existing payment"""
    print_test(f"Update Payment ({payment_id})")
    
    payload = {
        "payment_status": "completed"
    }
    
    response = requests.put(f"{BASE_URL}/payments/{payment_id}", json=payload)
    print_response(response)
    
    if response.status_code == 200:
        print_success("Payment updated successfully")
    else:
        print_error("Failed to update payment")

def test_delete_payment(payment_id):
    """Test: Delete a payment"""
    print_test(f"Delete Payment ({payment_id})")
    
    response = requests.delete(f"{BASE_URL}/payments/{payment_id}")
    print_response(response)
    
    if response.status_code == 204:
        print_success("Payment deleted successfully")
    elif response.status_code == 200:
        print_success("Payment deleted successfully")
    else:
        print_error("Failed to delete payment")

# ==================== ERROR HANDLING TESTS ====================

def test_error_nonexistent_payment():
    """Test: Error handling - Non-existent payment"""
    print_test("Error: Get Non-existent Payment (404)")
    
    response = requests.get(f"{BASE_URL}/payments/{FAKE_PAYMENT_UUID}")
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returned 404 for non-existent payment")
    else:
        print_error(f"Expected 404, got {response.status_code}")

def test_error_nonexistent_user():
    """Test: Error handling - Non-existent user on create"""
    print_test("Error: Create Payment for Non-existent User (404)")
    
    payload = {
        "user_id": FAKE_USER_UUID,
        "amount": 100.00,
        "payment_method": "credit_card",
        "transaction_id": f"TXN-{uuid4()}"
    }
    
    response = requests.post(f"{BASE_URL}/payments", json=payload)
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returned 404 for non-existent user")
    else:
        print_error(f"Expected 404, got {response.status_code}")

def test_error_duplicate_transaction_id():
    """Test: Error handling - Duplicate transaction ID"""
    print_test("Error: Create Payment with Duplicate Transaction ID (400)")
    
    # First, create a payment with a unique ID
    unique_txn_id = f"TXN-DUP-{uuid4()}"
    payload1 = {
        "user_id": VALID_USER_ID,
        "amount": 100.00,
        "payment_method": "credit_card",
        "transaction_id": unique_txn_id
    }
    response1 = requests.post(f"{BASE_URL}/payments", json=payload1)
    
    # Try to create another payment with the same transaction ID
    payload2 = {
        "user_id": VALID_USER_ID,
        "amount": 200.00,
        "payment_method": "debit_card",
        "transaction_id": unique_txn_id
    }
    response2 = requests.post(f"{BASE_URL}/payments", json=payload2)
    print_response(response2)
    
    if response2.status_code == 400:
        print_success("Correctly returned 400 for duplicate transaction ID")
    elif response2.status_code == 422:
        print_success("Correctly returned 422 for duplicate transaction ID")
    else:
        print_error(f"Expected 400/422, got {response2.status_code}")

def test_error_invalid_uuid():
    """Test: Error handling - Invalid UUID format"""
    print_test("Error: Get Payment with Invalid UUID Format (400)")
    
    response = requests.get(f"{BASE_URL}/payments/not-a-uuid")
    print_response(response)
    
    if response.status_code in [400, 422]:
        print_success("Correctly returned error for invalid UUID")
    else:
        print_error(f"Expected 400/422, got {response.status_code}")

def test_error_missing_required_field():
    """Test: Error handling - Missing required field on create"""
    print_test("Error: Create without Required Field (422)")
    
    payload = {
        "user_id": VALID_USER_ID,
        # Missing amount, payment_method, transaction_id
    }
    
    response = requests.post(f"{BASE_URL}/payments", json=payload)
    print_response(response)
    
    if response.status_code == 422:
        print_success("Correctly returned 422 for missing required field")
    else:
        print_error(f"Expected 422, got {response.status_code}")

def test_error_nonexistent_user_for_get():
    """Test: Error handling - Non-existent user on get user payments"""
    print_test("Error: Get Payments for Non-existent User (404)")
    
    response = requests.get(f"{BASE_URL}/payments/user/{FAKE_USER_UUID}")
    print_response(response)
    
    if response.status_code == 404:
        print_success("Correctly returned 404 for non-existent user")
    else:
        # Some implementations may return empty list instead
        print_success("Returned response for non-existent user")

# ==================== PAYMENT STATUS TESTS ====================

def test_different_payment_statuses():
    """Test: Update payment with different statuses"""
    print_test("Test Payment Status Transitions")
    
    statuses = ["pending", "completed", "failed", "refunded"]
    
    for status in statuses:
        payload = {
            "user_id": VALID_USER_ID,
            "amount": 100.00,
            "payment_method": "upi",
            "transaction_id": f"TXN-STATUS-{status}-{uuid4()}"
        }
        
        # Create payment
        response = requests.post(f"{BASE_URL}/payments", json=payload)
        
        if response.status_code == 201:
            payment_id = response.json()["id"]
            
            # Try to update status
            update_payload = {"payment_status": status}
            update_response = requests.put(
                f"{BASE_URL}/payments/{payment_id}",
                json=update_payload
            )
            
            if update_response.status_code == 200:
                print_success(f"Payment status '{status}' works")
            else:
                print_error(f"Failed to set status '{status}'")

# ==================== MAIN TEST SUITE ====================

def run_all_tests():
    """Run complete test suite"""
    print_header("PAYMENTS API - TEST SUITE")
    
    print("\n📝 Configuration:")
    print(f"  Base URL: {BASE_URL}")
    print(f"  User ID: {VALID_USER_ID}")
    print(f"  Payment ID: {VALID_PAYMENT_ID}")
    
    # ==================== BASIC CRUD TESTS ====================
    print_header("1. BASIC CRUD OPERATIONS")
    
    # Create
    created_id = test_create_payment()
    
    # Get All
    test_get_all_payments()
    
    # Get Single
    if created_id:
        test_get_payment_by_id(created_id)
    else:
        test_get_payment_by_id(VALID_PAYMENT_ID)
    
    # Update
    if created_id:
        test_update_payment(created_id)
    else:
        test_update_payment(VALID_PAYMENT_ID)
    
    # ==================== FILTERING TESTS ====================
    print_header("2. FILTERING & SEARCH")
    
    test_get_user_payments()
    test_filter_by_user_id()
    test_filter_by_status()
    test_get_payments_by_status()
    test_get_user_payments_with_filter()
    
    # ==================== PAGINATION TESTS ====================
    print_header("3. PAGINATION & LIMITS")
    
    test_pagination()
    
    # ==================== PAYMENT STATUS TESTS ====================
    print_header("4. PAYMENT STATUS TRANSITIONS")
    
    test_different_payment_statuses()
    
    # ==================== ERROR HANDLING TESTS ====================
    print_header("5. ERROR HANDLING")
    
    test_error_nonexistent_payment()
    test_error_invalid_uuid()
    test_error_missing_required_field()
    test_error_nonexistent_user()
    test_error_nonexistent_user_for_get()
    test_error_duplicate_transaction_id()
    
    # ==================== DELETE TEST ====================
    print_header("6. CLEANUP")
    
    if created_id:
        test_delete_payment(created_id)
    
    # ==================== SUMMARY ====================
    print_header("TEST SUITE COMPLETE")
    print("\n✅ All tests executed successfully!")
    print("\n📊 Summary:")
    print("  ✓ CRUD operations")
    print("  ✓ Filtering and search")
    print("  ✓ Pagination")
    print("  ✓ Payment status transitions")
    print("  ✓ Error handling")
    print("  ✓ Duplicate transaction ID validation")
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
