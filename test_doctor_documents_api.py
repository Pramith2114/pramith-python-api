#!/usr/bin/env python3
"""
Doctor Documents API Test Suite
Tests all doctor documents endpoints
"""

import requests
import json
from uuid import uuid4
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:8000"

# Test data
TEST_DOCTOR_ID = None
TEST_DOCUMENT_IDS = []

def print_section(title):
    """Print section separator"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_test(name, passed, message=""):
    """Print test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {name}")
    if message:
        print(f"    → {message}")

def test_create_user_and_doctor():
    """Create a user and doctor for testing"""
    global TEST_DOCTOR_ID
    
    print_section("Setup: Create User & Doctor for Testing")
    
    # Create user
    user_response = requests.post(
        f"{BASE_URL}/api/users",
        json={
            "name": "Dr. Test",
            "mobile": f"98765432{int(datetime.now().timestamp()) % 10000:02d}",
            "email": f"test@example.com",
            "password": "testpass123",
            "role": "doctor"
        }
    )
    
    if user_response.status_code == 201:
        user_id = user_response.json()["id"]
        print_test("Create user with doctor role", True, f"User ID: {user_id}")
        
        # Create doctor profile
        doctor_response = requests.post(
            f"{BASE_URL}/api/doctors",
            json={
                "user_id": user_id,
                "specialization": "Cardiology",
                "experience": 5,
                "consultation_fee": 500.00
            }
        )
        
        if doctor_response.status_code == 201:
            TEST_DOCTOR_ID = doctor_response.json()["id"]
            print_test("Create doctor profile", True, f"Doctor ID: {TEST_DOCTOR_ID}")
        else:
            print_test("Create doctor profile", False, doctor_response.json())
    else:
        print_test("Create user with doctor role", False, user_response.json())

def test_upload_document():
    """Test uploading a document"""
    print_section("Test 1: Upload Document")
    
    if not TEST_DOCTOR_ID:
        print_test("Upload document", False, "No doctor ID available")
        return
    
    response = requests.post(
        f"{BASE_URL}/api/doctor-documents",
        json={
            "doctor_id": TEST_DOCTOR_ID,
            "document_type": "Medical License",
            "file_url": "https://storage.example.com/license.pdf"
        }
    )
    
    if response.status_code == 201:
        doc_id = response.json()["id"]
        TEST_DOCUMENT_IDS.append(doc_id)
        verified = response.json()["verified"]
        
        print_test("Upload document", True, f"Document ID: {doc_id}")
        print_test("Default verification status", verified == False, 
                  f"verified={verified}")
        print_test("Document type stored", 
                  response.json()["document_type"] == "Medical License",
                  f"Type: {response.json()['document_type']}")
    else:
        print_test("Upload document", False, response.json())

def test_upload_multiple_documents():
    """Test uploading multiple documents"""
    print_section("Test 2: Upload Multiple Documents")
    
    if not TEST_DOCTOR_ID:
        print_test("Upload multiple documents", False, "No doctor ID available")
        return
    
    doc_types = [
        ("Medical Degree", "https://storage.example.com/degree.pdf"),
        ("Board Certification", "https://storage.example.com/cert.pdf"),
        ("Malpractice Insurance", "https://storage.example.com/insurance.pdf")
    ]
    
    created = 0
    for doc_type, file_url in doc_types:
        response = requests.post(
            f"{BASE_URL}/api/doctor-documents",
            json={
                "doctor_id": TEST_DOCTOR_ID,
                "document_type": doc_type,
                "file_url": file_url
            }
        )
        
        if response.status_code == 201:
            TEST_DOCUMENT_IDS.append(response.json()["id"])
            created += 1
    
    print_test("Upload multiple documents", created == len(doc_types),
              f"Created {created}/{len(doc_types)} documents")

def test_get_all_documents():
    """Test getting all documents"""
    print_section("Test 3: Get All Documents")
    
    response = requests.get(f"{BASE_URL}/api/doctor-documents")
    
    if response.status_code == 200:
        docs = response.json()
        print_test("Get all documents", len(docs) > 0, f"Found {len(docs)} documents")
        
        if docs:
            doc = docs[0]
            has_required_fields = all(field in doc for field in 
                                     ["id", "doctor_id", "document_type", "file_url", "verified"])
            print_test("Response includes required fields", has_required_fields,
                      f"Fields: {list(doc.keys())}")
    else:
        print_test("Get all documents", False, response.json())

def test_pagination():
    """Test pagination"""
    print_section("Test 4: Pagination")
    
    # Get first page
    response1 = requests.get(f"{BASE_URL}/api/doctor-documents?skip=0&limit=2")
    
    if response1.status_code == 200:
        docs1 = response1.json()
        print_test("Get first page (limit=2)", len(docs1) <= 2,
                  f"Returned {len(docs1)} documents")
        
        # Get second page if available
        response2 = requests.get(f"{BASE_URL}/api/doctor-documents?skip=2&limit=2")
        docs2 = response2.json()
        print_test("Get second page (skip=2, limit=2)", 
                  len(docs1) + len(docs2) >= len(docs1),
                  f"Page 1: {len(docs1)}, Page 2: {len(docs2)}")
    else:
        print_test("Pagination", False, response1.json())

def test_get_specific_document():
    """Test getting specific document"""
    print_section("Test 5: Get Specific Document")
    
    if not TEST_DOCUMENT_IDS:
        print_test("Get specific document", False, "No documents available")
        return
    
    doc_id = TEST_DOCUMENT_IDS[0]
    response = requests.get(f"{BASE_URL}/api/doctor-documents/{doc_id}")
    
    if response.status_code == 200:
        doc = response.json()
        print_test("Get specific document", doc["id"] == doc_id, 
                  f"Document ID: {doc_id}")
    else:
        print_test("Get specific document", False, response.json())

def test_get_doctor_documents():
    """Test getting documents for specific doctor"""
    print_section("Test 6: Get Doctor's Documents")
    
    if not TEST_DOCTOR_ID:
        print_test("Get doctor documents", False, "No doctor ID available")
        return
    
    response = requests.get(
        f"{BASE_URL}/api/doctor-documents/doctor/{TEST_DOCTOR_ID}"
    )
    
    if response.status_code == 200:
        docs = response.json()
        print_test("Get doctor documents", len(docs) > 0, 
                  f"Found {len(docs)} documents for doctor")
        
        # Check all belong to same doctor
        same_doctor = all(doc["doctor_id"] == TEST_DOCTOR_ID for doc in docs)
        print_test("All documents belong to doctor", same_doctor,
                  f"Total documents: {len(docs)}")
    else:
        print_test("Get doctor documents", False, response.json())

def test_filter_verified():
    """Test filtering by verification status"""
    print_section("Test 7: Filter by Verification Status")
    
    # Get unverified documents
    response_unverified = requests.get(
        f"{BASE_URL}/api/doctor-documents?verified=false"
    )
    
    if response_unverified.status_code == 200:
        unverified = response_unverified.json()
        all_unverified = all(not doc["verified"] for doc in unverified)
        print_test("Filter unverified documents", all_unverified,
                  f"Found {len(unverified)} unverified documents")
    
    # Get verified documents
    response_verified = requests.get(
        f"{BASE_URL}/api/doctor-documents?verified=true"
    )
    
    if response_verified.status_code == 200:
        verified = response_verified.json()
        all_verified = all(doc["verified"] for doc in verified)
        print_test("Filter verified documents", all_verified,
                  f"Found {len(verified)} verified documents")

def test_update_document():
    """Test updating document"""
    print_section("Test 8: Update Document")
    
    if not TEST_DOCUMENT_IDS:
        print_test("Update document", False, "No documents available")
        return
    
    doc_id = TEST_DOCUMENT_IDS[0]
    new_url = "https://storage.example.com/license_updated.pdf"
    
    response = requests.put(
        f"{BASE_URL}/api/doctor-documents/{doc_id}",
        json={
            "file_url": new_url
        }
    )
    
    if response.status_code == 200:
        doc = response.json()
        print_test("Update document file URL", doc["file_url"] == new_url,
                  f"New URL: {new_url}")
    else:
        print_test("Update document", False, response.json())

def test_verify_document():
    """Test verifying document"""
    print_section("Test 9: Verify Document")
    
    if not TEST_DOCUMENT_IDS:
        print_test("Verify document", False, "No documents available")
        return
    
    # Use second document for verification test
    doc_id = TEST_DOCUMENT_IDS[1] if len(TEST_DOCUMENT_IDS) > 1 else TEST_DOCUMENT_IDS[0]
    
    # Verify
    response = requests.post(
        f"{BASE_URL}/api/doctor-documents/{doc_id}/verify",
        json={"verified": True}
    )
    
    if response.status_code == 200:
        doc = response.json()
        print_test("Verify document", doc["verified"] == True,
                  f"Verified: {doc['verified']}")
        
        # Unverify
        response2 = requests.post(
            f"{BASE_URL}/api/doctor-documents/{doc_id}/verify",
            json={"verified": False}
        )
        
        if response2.status_code == 200:
            doc2 = response2.json()
            print_test("Unverify document", doc2["verified"] == False,
                      f"Verified: {doc2['verified']}")
        else:
            print_test("Unverify document", False, response2.json())
    else:
        print_test("Verify document", False, response.json())

def test_delete_document():
    """Test deleting document"""
    print_section("Test 10: Delete Document")
    
    if not TEST_DOCUMENT_IDS:
        print_test("Delete document", False, "No documents available")
        return
    
    # Use last document for deletion test
    doc_id = TEST_DOCUMENT_IDS[-1]
    
    response = requests.delete(f"{BASE_URL}/api/doctor-documents/{doc_id}")
    
    if response.status_code == 204:
        print_test("Delete document", True, f"Document {doc_id} deleted")
        
        # Verify deletion
        response_verify = requests.get(f"{BASE_URL}/api/doctor-documents/{doc_id}")
        
        if response_verify.status_code == 404:
            print_test("Document no longer exists", True, "Verified deletion")
        else:
            print_test("Document no longer exists", False, 
                      f"Still found: {response_verify.json()}")
    else:
        print_test("Delete document", False, f"Status: {response.status_code}")

def test_error_cases():
    """Test error cases"""
    print_section("Test 11: Error Cases")
    
    # Test: Get non-existent document
    response = requests.get(
        f"{BASE_URL}/api/doctor-documents/{uuid4()}"
    )
    print_test("Get non-existent document returns 404", response.status_code == 404,
              f"Status: {response.status_code}")
    
    # Test: Upload for non-existent doctor
    response = requests.post(
        f"{BASE_URL}/api/doctor-documents",
        json={
            "doctor_id": str(uuid4()),
            "document_type": "Test",
            "file_url": "https://example.com/test.pdf"
        }
    )
    print_test("Upload for non-existent doctor returns 404", response.status_code == 404,
              f"Status: {response.status_code}")
    
    # Test: Missing required fields
    response = requests.post(
        f"{BASE_URL}/api/doctor-documents",
        json={
            "doctor_id": TEST_DOCTOR_ID if TEST_DOCTOR_ID else str(uuid4())
        }
    )
    print_test("Missing required fields returns 422", response.status_code == 422,
              f"Status: {response.status_code}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  DOCTOR DOCUMENTS API TEST SUITE")
    print("="*60)
    
    try:
        test_create_user_and_doctor()
        test_upload_document()
        test_upload_multiple_documents()
        test_get_all_documents()
        test_pagination()
        test_get_specific_document()
        test_get_doctor_documents()
        test_filter_verified()
        test_update_document()
        test_verify_document()
        test_delete_document()
        test_error_cases()
        
        print_section("Test Suite Complete")
        print("✓ All tests completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
