"""
Test script for Appointments API
Tests all CRUD operations for appointments
"""
import requests
import json
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000/api"

# You'll need to use existing patient and doctor UUIDs
# Here are example UUIDs - replace with real ones from your database
APPOINTMENT_DATA = {
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",  # Replace with real patient UUID
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",    # Replace with real doctor UUID
    "appointment_date": "2024-04-20",
    "time_slot": "09:00-09:30",
    "status": "scheduled",
    "notes": "Initial consultation"
}

APPOINTMENT_DATA_2 = {
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "appointment_date": "2024-04-22",
    "time_slot": "14:00-14:30",
    "status": "scheduled",
    "notes": "Follow-up consultation"
}


def test_appointment_endpoints():
    """Test all appointment endpoints"""
    
    print("\n" + "="*60)
    print("APPOINTMENTS API TESTS")
    print("="*60)
    
    # 1. Create appointments
    print("\n1. CREATE APPOINTMENTS")
    print("-" * 60)
    appointment_id = None
    appointment_id_2 = None
    patient_id = APPOINTMENT_DATA["patient_id"]
    doctor_id = APPOINTMENT_DATA["doctor_id"]
    
    try:
        # Create first appointment
        response = requests.post(f"{BASE_URL}/appointments", json=APPOINTMENT_DATA)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            appointment = response.json()
            appointment_id = appointment["id"]
            print(f"✓ Appointment created with ID: {appointment_id}")
            print(f"Response: {json.dumps(appointment, indent=2)}")
        else:
            print(f"✗ Failed to create appointment")
            print(f"Response: {response.json()}")
            return
        
        # Create second appointment
        response = requests.post(f"{BASE_URL}/appointments", json=APPOINTMENT_DATA_2)
        if response.status_code == 201:
            appointment = response.json()
            appointment_id_2 = appointment["id"]
            print(f"\n✓ Second appointment created with ID: {appointment_id_2}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return
    
    # 2. Get all appointments
    print("\n2. GET ALL APPOINTMENTS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/appointments?skip=0&limit=10")
        print(f"Status Code: {response.status_code}")
        appointments = response.json()
        print(f"Total appointments retrieved: {len(appointments)}")
        print("✓ Successfully retrieved all appointments")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 3. Get specific appointment with details
    print("\n3. GET SPECIFIC APPOINTMENT")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/appointments/{appointment_id}")
        print(f"Status Code: {response.status_code}")
        appointment = response.json()
        print(f"Response: {json.dumps(appointment, indent=2)}")
        print("✓ Successfully retrieved appointment with patient and doctor details")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 4. Get patient appointments
    print("\n4. GET PATIENT APPOINTMENTS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/appointments/patient/{patient_id}")
        print(f"Status Code: {response.status_code}")
        appointments = response.json()
        print(f"Patient appointments: {len(appointments)}")
        print("✓ Successfully retrieved patient appointments")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 5. Get doctor appointments
    print("\n5. GET DOCTOR APPOINTMENTS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/appointments/doctor/{doctor_id}")
        print(f"Status Code: {response.status_code}")
        appointments = response.json()
        print(f"Doctor appointments: {len(appointments)}")
        print("✓ Successfully retrieved doctor appointments")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 6. Filter appointments by status
    print("\n6. FILTER APPOINTMENTS BY STATUS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/appointments?status=scheduled")
        print(f"Status Code: {response.status_code}")
        appointments = response.json()
        print(f"Scheduled appointments: {len(appointments)}")
        print("✓ Successfully filtered appointments by status")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 7. Update appointment
    print("\n7. UPDATE APPOINTMENT")
    print("-" * 60)
    update_data = {
        "appointment_date": "2024-04-21",
        "time_slot": "10:00-10:30",
        "notes": "Rescheduled appointment"
    }
    try:
        response = requests.put(f"{BASE_URL}/appointments/{appointment_id}", json=update_data)
        print(f"Status Code: {response.status_code}")
        appointment = response.json()
        print(f"Updated appointment: {json.dumps(appointment, indent=2)}")
        print("✓ Successfully updated appointment")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 8. Cancel appointment
    print("\n8. CANCEL APPOINTMENT")
    print("-" * 60)
    try:
        response = requests.post(f"{BASE_URL}/appointments/{appointment_id_2}/cancel")
        print(f"Status Code: {response.status_code}")
        appointment = response.json()
        print(f"Cancelled appointment status: {appointment['status']}")
        print("✓ Successfully cancelled appointment")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 9. Complete appointment
    print("\n9. COMPLETE APPOINTMENT")
    print("-" * 60)
    try:
        response = requests.post(f"{BASE_URL}/appointments/{appointment_id}/complete")
        print(f"Status Code: {response.status_code}")
        appointment = response.json()
        print(f"Completed appointment status: {appointment['status']}")
        print("✓ Successfully marked appointment as completed")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 10. Delete appointment
    print("\n10. DELETE APPOINTMENT")
    print("-" * 60)
    try:
        response = requests.delete(f"{BASE_URL}/appointments/{appointment_id_2}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 204:
            print("✓ Successfully deleted appointment")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("APPOINTMENTS API - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    print("\nIMPORTANT: Make sure to replace the UUIDs in this script")
    print("with real patient and doctor UUIDs from your database!")
    
    test_appointment_endpoints()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
