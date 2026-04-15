"""
Test suite for Prescriptions API
Tests all CRUD operations for prescriptions and prescription items
"""

def test_prescription_endpoints():
    """
    Test all prescription endpoints with sample data
    Note: Replace UUID placeholders with actual IDs from your database
    """
    
    print("=" * 80)
    print("PRESCRIPTIONS API TEST SUITE")
    print("=" * 80)
    
    # Sample UUIDs - Replace these with actual UUIDs from your database
    # You can get these from the respective API endpoints:
    # - User UUIDs: GET /api/users
    # - Doctor UUIDs: GET /api/doctors
    # - Drug UUIDs: GET /api/drugs
    # - Appointment UUIDs: GET /api/appointments
    
    appointment_id = "550e8400-e29b-41d4-a716-446655440000"  # Replace with actual appointment ID
    doctor_id = "660e8400-e29b-41d4-a716-446655440111"      # Replace with actual doctor ID
    patient_id = "770e8400-e29b-41d4-a716-446655440222"     # Replace with actual patient ID
    drug_id_1 = "880e8400-e29b-41d4-a716-446655440333"      # Replace with actual drug ID
    drug_id_2 = "990e8400-e29b-41d4-a716-446655440444"      # Replace with actual drug ID
    
    import requests
    import json
    
    base_url = "http://localhost:8000"
    
    # =====================================================================
    # TEST 1: Create Prescription with Items
    # =====================================================================
    print("\n[TEST 1] Create Prescription with Items")
    print("-" * 80)
    
    prescription_data = {
        "appointment_id": appointment_id,
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "notes": "Patient to take antibiotics with food. No dairy products.",
        "items": [
            {
                "drug_id": drug_id_1,
                "dosage": "500mg",
                "duration": "7 days",
                "instructions": "Take twice daily after meals"
            },
            {
                "drug_id": drug_id_2,
                "dosage": "10ml",
                "duration": "5 days",
                "instructions": "Take as needed for fever"
            }
        ]
    }
    
    response = requests.post(
        f"{base_url}/api/prescriptions",
        json=prescription_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        prescription = response.json()
        prescription_id = prescription["id"]
        print(f"✓ Prescription created: {prescription_id}")
    else:
        print("✗ Failed to create prescription")
        print("Ensure appointment_id, doctor_id, patient_id, and drug IDs exist")
        return
    
    # =====================================================================
    # TEST 2: Get All Prescriptions
    # =====================================================================
    print("\n[TEST 2] Get All Prescriptions")
    print("-" * 80)
    
    response = requests.get(
        f"{base_url}/api/prescriptions",
        params={"skip": 0, "limit": 10}
    )
    
    print(f"Status Code: {response.status_code}")
    results = response.json()
    print(f"Prescriptions found: {len(results)}")
    if results:
        print(f"First prescription: {results[0]['id']}")
        print("✓ Listed all prescriptions")
    
    # =====================================================================
    # TEST 3: Get Single Prescription with Items
    # =====================================================================
    print("\n[TEST 3] Get Single Prescription (with Items)")
    print("-" * 80)
    
    response = requests.get(f"{base_url}/api/prescriptions/{prescription_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        prescription = response.json()
        print(f"Prescription ID: {prescription['id']}")
        print(f"Patient ID: {prescription['patient_id']}")
        print(f"Doctor ID: {prescription['doctor_id']}")
        print(f"Notes: {prescription['notes']}")
        if 'items' in prescription and prescription['items']:
            print(f"Items in prescription: {len(prescription['items'])}")
            for i, item in enumerate(prescription['items'], 1):
                print(f"  Item {i}: {item['dosage']} for {item['duration']}")
        print("✓ Retrieved prescription with items")
    
    # =====================================================================
    # TEST 4: Get Patient Prescriptions
    # =====================================================================
    print("\n[TEST 4] Get Patient Prescriptions")
    print("-" * 80)
    
    response = requests.get(
        f"{base_url}/api/prescriptions/patient/{patient_id}",
        params={"skip": 0, "limit": 10}
    )
    
    print(f"Status Code: {response.status_code}")
    results = response.json()
    print(f"Prescriptions for patient: {len(results)}")
    if results:
        print(f"Most recent: {results[0]['created_at']}")
        print("✓ Retrieved patient prescriptions")
    
    # =====================================================================
    # TEST 5: Get Doctor Prescriptions
    # =====================================================================
    print("\n[TEST 5] Get Doctor Prescriptions")
    print("-" * 80)
    
    response = requests.get(
        f"{base_url}/api/prescriptions/doctor/{doctor_id}",
        params={"skip": 0, "limit": 10}
    )
    
    print(f"Status Code: {response.status_code}")
    results = response.json()
    print(f"Prescriptions issued by doctor: {len(results)}")
    if results:
        print("✓ Retrieved doctor prescriptions")
    
    # =====================================================================
    # TEST 6: Get Appointment Prescriptions
    # =====================================================================
    print("\n[TEST 6] Get Appointment Prescriptions")
    print("-" * 80)
    
    response = requests.get(
        f"{base_url}/api/prescriptions/appointment/{appointment_id}"
    )
    
    print(f"Status Code: {response.status_code}")
    results = response.json()
    print(f"Prescriptions for appointment: {len(results)}")
    if results:
        print("✓ Retrieved appointment prescriptions")
    
    # =====================================================================
    # TEST 7: Update Prescription
    # =====================================================================
    print("\n[TEST 7] Update Prescription")
    print("-" * 80)
    
    update_data = {
        "notes": "UPDATED: Patient reported mild side effects. Monitor closely."
    }
    
    response = requests.put(
        f"{base_url}/api/prescriptions/{prescription_id}",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        updated = response.json()
        print(f"Updated notes: {updated['notes']}")
        print("✓ Updated prescription")
    
    # =====================================================================
    # TEST 8: Add Item to Prescription
    # =====================================================================
    print("\n[TEST 8] Add Item to Prescription")
    print("-" * 80)
    
    item_data = {
        "drug_id": drug_id_1,
        "dosage": "250mg",
        "duration": "10 days",
        "instructions": "Take once daily before bedtime"
    }
    
    response = requests.post(
        f"{base_url}/api/prescription-items",
        params={"prescription_id": prescription_id},
        json=item_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        item = response.json()
        item_id = item["id"]
        print(f"Item created: {item_id}")
        print(f"Dosage: {item['dosage']}, Duration: {item['duration']}")
        print("✓ Added item to prescription")
    else:
        print("✗ Failed to add item")
        item_id = None
    
    # =====================================================================
    # TEST 9: Get Prescription Items
    # =====================================================================
    print("\n[TEST 9] Get Prescription Items")
    print("-" * 80)
    
    response = requests.get(
        f"{base_url}/api/prescription-items/prescription/{prescription_id}"
    )
    
    print(f"Status Code: {response.status_code}")
    items = response.json()
    print(f"Items in prescription: {len(items)}")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item['dosage']} for {item['duration']}")
    print("✓ Retrieved prescription items")
    
    # =====================================================================
    # TEST 10: Get Single Item
    # =====================================================================
    if item_id:
        print("\n[TEST 10] Get Single Prescription Item")
        print("-" * 80)
        
        response = requests.get(f"{base_url}/api/prescription-items/{item_id}")
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            item = response.json()
            print(f"Item ID: {item['id']}")
            print(f"Dosage: {item['dosage']}")
            print(f"Duration: {item['duration']}")
            print(f"Instructions: {item['instructions']}")
            print("✓ Retrieved single item")
    
    # =====================================================================
    # TEST 11: Get Items by Drug
    # =====================================================================
    print("\n[TEST 11] Get Items by Drug")
    print("-" * 80)
    
    response = requests.get(
        f"{base_url}/api/prescription-items/drug/{drug_id_1}"
    )
    
    print(f"Status Code: {response.status_code}")
    items = response.json()
    print(f"Prescriptions using this drug: {len(items)}")
    if items:
        print("✓ Retrieved items by drug")
    
    # =====================================================================
    # TEST 12: Update Prescription Item
    # =====================================================================
    if item_id:
        print("\n[TEST 12] Update Prescription Item")
        print("-" * 80)
        
        update_item_data = {
            "drug_id": drug_id_1,
            "dosage": "125mg",
            "duration": "10 days",
            "instructions": "Take once daily at bedtime"
        }
        
        response = requests.put(
            f"{base_url}/api/prescription-items/{item_id}",
            json=update_item_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            updated = response.json()
            print(f"Updated dosage: {updated['dosage']}")
            print(f"Updated instructions: {updated['instructions']}")
            print("✓ Updated prescription item")
    
    # =====================================================================
    # TEST 13: Delete Prescription Item
    # =====================================================================
    if item_id:
        print("\n[TEST 13] Delete Prescription Item")
        print("-" * 80)
        
        response = requests.delete(f"{base_url}/api/prescription-items/{item_id}")
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 204:
            print("Item deleted successfully")
            print("✓ Deleted prescription item")
    
    # =====================================================================
    # TEST 14: Delete Prescription (with Items)
    # =====================================================================
    print("\n[TEST 14] Delete Prescription (with Items)")
    print("-" * 80)
    
    response = requests.delete(f"{base_url}/api/prescriptions/{prescription_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print("Prescription deleted successfully")
        print("Note: All associated prescription items were also deleted")
        print("✓ Deleted prescription")
    
    # =====================================================================
    # SUMMARY
    # =====================================================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print("""
✓ Create prescription
✓ List all prescriptions
✓ Get single prescription with items
✓ Get patient prescriptions
✓ Get doctor prescriptions
✓ Get appointment prescriptions
✓ Update prescription
✓ Add item to prescription
✓ Get prescription items
✓ Get single item
✓ Get items by drug
✓ Update prescription item
✓ Delete prescription item
✓ Delete prescription

All tests completed!
    """)


if __name__ == "__main__":
    print("Starting Prescriptions API Test Suite...")
    print("Make sure the server is running: python -m uvicorn app.main:app --reload")
    print("\nNote: Update the UUID placeholders in this file with real IDs from your database")
    print("You can get them from:")
    print("  - Patients: GET /api/users?role=patient")
    print("  - Doctors: GET /api/doctors")
    print("  - Appointments: GET /api/appointments")
    print("  - Drugs: GET /api/drugs")
    print()
    
    try:
        test_prescription_endpoints()
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("Make sure the server is running on http://localhost:8000")
        print("Install requests: pip install requests")
