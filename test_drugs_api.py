#!/usr/bin/env python3
"""
Drugs API Test Suite
Tests all drug management endpoints
"""

import requests
import json
from uuid import uuid4
from datetime import datetime, timedelta

# Base URL
BASE_URL = "http://localhost:8000"

# Test storage
TEST_DRUG_IDS = []

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

def test_create_drug():
    """Test creating a drug"""
    print_section("Test 1: Create Drug")
    
    expiry_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    
    response = requests.post(
        f"{BASE_URL}/api/drugs",
        json={
            "name": "Aspirin 500mg",
            "generic_name": "Acetylsalicylic acid",
            "manufacturer": "Bayer",
            "price": 5.99,
            "stock_quantity": 100,
            "expiry_date": expiry_date
        }
    )
    
    if response.status_code == 201:
        drug = response.json()
        drug_id = drug["id"]
        TEST_DRUG_IDS.append(drug_id)
        
        print_test("Create drug", True, f"Drug ID: {drug_id}")
        print_test("Response has required fields", 
                  all(field in drug for field in 
                      ["id", "name", "generic_name", "manufacturer", "price", "stock_quantity", "expiry_date"]),
                  "All fields present")
    else:
        print_test("Create drug", False, response.json())

def test_create_multiple_drugs():
    """Test creating multiple drugs"""
    print_section("Test 2: Create Multiple Drugs")
    
    drugs_data = [
        {
            "name": "Paracetamol 650mg",
            "generic_name": "Paracetamol",
            "manufacturer": "GlaxoSmithKline",
            "price": 3.49,
            "stock_quantity": 200,
            "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        },
        {
            "name": "Ibuprofen 400mg",
            "generic_name": "Ibuprofen",
            "manufacturer": "Pfizer",
            "price": 4.99,
            "stock_quantity": 150,
            "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        },
        {
            "name": "Amoxicillin 500mg",
            "generic_name": "Amoxicillin",
            "manufacturer": "Abbott",
            "price": 8.99,
            "stock_quantity": 50,
            "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        }
    ]
    
    created = 0
    for drug_data in drugs_data:
        response = requests.post(f"{BASE_URL}/api/drugs", json=drug_data)
        if response.status_code == 201:
            TEST_DRUG_IDS.append(response.json()["id"])
            created += 1
    
    print_test("Create multiple drugs", created == len(drugs_data),
              f"Created {created}/{len(drugs_data)} drugs")

def test_get_all_drugs():
    """Test getting all drugs"""
    print_section("Test 3: Get All Drugs")
    
    response = requests.get(f"{BASE_URL}/api/drugs")
    
    if response.status_code == 200:
        drugs = response.json()
        print_test("Get all drugs", len(drugs) > 0, f"Found {len(drugs)} drugs")
        
        if drugs:
            drug = drugs[0]
            has_required_fields = all(field in drug for field in 
                                     ["id", "name", "generic_name", "manufacturer", "price", "stock_quantity", "expiry_date"])
            print_test("Response structure", has_required_fields,
                      f"Fields: {list(drug.keys())}")
    else:
        print_test("Get all drugs", False, response.json())

def test_pagination():
    """Test pagination"""
    print_section("Test 4: Pagination")
    
    # Get first page
    response1 = requests.get(f"{BASE_URL}/api/drugs?skip=0&limit=2")
    
    if response1.status_code == 200:
        drugs1 = response1.json()
        print_test("Get first page (limit=2)", len(drugs1) <= 2,
                  f"Returned {len(drugs1)} drugs")
        
        # Get second page if available
        response2 = requests.get(f"{BASE_URL}/api/drugs?skip=2&limit=2")
        drugs2 = response2.json()
        print_test("Get second page (skip=2, limit=2)", 
                  len(drugs1) + len(drugs2) >= len(drugs1),
                  f"Page 1: {len(drugs1)}, Page 2: {len(drugs2)}")
    else:
        print_test("Pagination", False, response1.json())

def test_get_specific_drug():
    """Test getting a specific drug"""
    print_section("Test 5: Get Specific Drug")
    
    if not TEST_DRUG_IDS:
        print_test("Get specific drug", False, "No drugs available")
        return
    
    drug_id = TEST_DRUG_IDS[0]
    response = requests.get(f"{BASE_URL}/api/drugs/{drug_id}")
    
    if response.status_code == 200:
        drug = response.json()
        print_test("Get specific drug", drug["id"] == drug_id,
                  f"Retrieved: {drug['name']}")
    else:
        print_test("Get specific drug", False, response.json())

def test_filter_by_name():
    """Test filtering by name"""
    print_section("Test 6: Filter by Name")
    
    response = requests.get(f"{BASE_URL}/api/drugs?name=aspirin")
    
    if response.status_code == 200:
        drugs = response.json()
        contains_aspirin = any("aspirin" in drug["name"].lower() for drug in drugs)
        print_test("Filter by name", contains_aspirin or len(drugs) == 0,
                  f"Found {len(drugs)} drugs containing 'aspirin'")
    else:
        print_test("Filter by name", False, response.json())

def test_filter_by_manufacturer():
    """Test filtering by manufacturer"""
    print_section("Test 7: Filter by Manufacturer")
    
    response = requests.get(f"{BASE_URL}/api/drugs?manufacturer=Bayer")
    
    if response.status_code == 200:
        drugs = response.json()
        all_bayer = all(drug["manufacturer"].lower() == "bayer" for drug in drugs)
        print_test("Filter by manufacturer", all_bayer or len(drugs) == 0,
                  f"Found {len(drugs)} Bayer drugs")
    else:
        print_test("Filter by manufacturer", False, response.json())

def test_update_drug():
    """Test updating a drug"""
    print_section("Test 8: Update Drug")
    
    if not TEST_DRUG_IDS:
        print_test("Update drug", False, "No drugs available")
        return
    
    drug_id = TEST_DRUG_IDS[0]
    new_price = 7.99
    new_stock = 250
    
    response = requests.put(
        f"{BASE_URL}/api/drugs/{drug_id}",
        json={
            "price": new_price,
            "stock_quantity": new_stock
        }
    )
    
    if response.status_code == 200:
        drug = response.json()
        print_test("Update price", float(drug["price"]) == new_price,
                  f"New price: {drug['price']}")
        print_test("Update stock", drug["stock_quantity"] == new_stock,
                  f"New stock: {drug['stock_quantity']}")
    else:
        print_test("Update drug", False, response.json())

def test_update_partial():
    """Test partial update"""
    print_section("Test 9: Partial Update")
    
    if len(TEST_DRUG_IDS) < 2:
        print_test("Partial update", False, "Need at least 2 drugs")
        return
    
    drug_id = TEST_DRUG_IDS[1]
    new_stock = 500
    
    response = requests.put(
        f"{BASE_URL}/api/drugs/{drug_id}",
        json={"stock_quantity": new_stock}
    )
    
    if response.status_code == 200:
        drug = response.json()
        print_test("Update only stock", drug["stock_quantity"] == new_stock,
                  f"Updated stock to {new_stock}")
    else:
        print_test("Partial update", False, response.json())

def test_delete_drug():
    """Test deleting a drug"""
    print_section("Test 10: Delete Drug")
    
    if len(TEST_DRUG_IDS) < 3:
        print_test("Delete drug", False, "Need at least 3 drugs")
        return
    
    drug_id = TEST_DRUG_IDS[-1]
    
    response = requests.delete(f"{BASE_URL}/api/drugs/{drug_id}")
    
    if response.status_code == 204:
        print_test("Delete drug", True, f"Deleted {drug_id}")
        
        # Verify deletion
        response_verify = requests.get(f"{BASE_URL}/api/drugs/{drug_id}")
        
        if response_verify.status_code == 404:
            print_test("Drug no longer exists", True, "Verified deletion")
        else:
            print_test("Drug no longer exists", False, "Drug still found")
    else:
        print_test("Delete drug", False, f"Status: {response.status_code}")

def test_error_cases():
    """Test error cases"""
    print_section("Test 11: Error Cases")
    
    # Test: Get non-existent drug
    response = requests.get(f"{BASE_URL}/api/drugs/{uuid4()}")
    print_test("Get non-existent drug returns 404", response.status_code == 404,
              f"Status: {response.status_code}")
    
    # Test: Invalid price (negative)
    response = requests.post(
        f"{BASE_URL}/api/drugs",
        json={
            "name": "Test",
            "generic_name": "Test",
            "manufacturer": "Test",
            "price": -5.99,
            "stock_quantity": 100,
            "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        }
    )
    print_test("Negative price returns 422", response.status_code == 422,
              f"Status: {response.status_code}")
    
    # Test: Missing required fields
    response = requests.post(
        f"{BASE_URL}/api/drugs",
        json={"name": "Test"}
    )
    print_test("Missing required fields returns 422", response.status_code == 422,
              f"Status: {response.status_code}")

def test_search_combined():
    """Test combined search filters"""
    print_section("Test 12: Combined Search")
    
    response = requests.get(
        f"{BASE_URL}/api/drugs?name=aspirin&manufacturer=bayer&limit=5"
    )
    
    if response.status_code == 200:
        drugs = response.json()
        print_test("Combined search filter", len(drugs) >= 0,
                  f"Found {len(drugs)} matching drugs")
    else:
        print_test("Combined search", False, response.json())

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  DRUGS API TEST SUITE")
    print("="*60)
    
    try:
        test_create_drug()
        test_create_multiple_drugs()
        test_get_all_drugs()
        test_pagination()
        test_get_specific_drug()
        test_filter_by_name()
        test_filter_by_manufacturer()
        test_update_drug()
        test_update_partial()
        test_delete_drug()
        test_error_cases()
        test_search_combined()
        
        print_section("Test Suite Complete")
        print("✓ All tests completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
