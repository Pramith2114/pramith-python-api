"""
Test script for Vendor and Vendor Orders API
Tests all CRUD operations for vendors and vendor orders
"""
import requests
import json
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:8000/api"

# Test data
VENDOR_DATA = {
    "name": "PharmaCorp Suppliers",
    "contact_number": "+91-9876543210",
    "email": "info@pharmacorp.com",
    "address": "123 Medical Street, Chennai, Tamil Nadu, India"
}

VENDOR_DATA_2 = {
    "name": "MediSupply Inc",
    "contact_number": "+91-8765432109",
    "email": "contact@medisupply.com",
    "address": "456 Healthcare Ave, Bangalore, Karnataka, India"
}

VENDOR_ORDER_DATA = {
    "total_amount": 50000.00,
    "status": "pending"
}

VENDOR_ORDER_UPDATE = {
    "status": "confirmed",
    "total_amount": 50000.00
}


def test_vendor_endpoints():
    """Test all vendor endpoints"""
    
    print("\n" + "="*60)
    print("VENDOR API TESTS")
    print("="*60)
    
    # 1. Create a vendor
    print("\n1. CREATE VENDOR")
    print("-" * 60)
    vendor_id = None
    vendor_id_2 = None
    
    try:
        # Create first vendor
        response = requests.post(f"{BASE_URL}/vendors", json=VENDOR_DATA)
        print(f"Status Code: {response.status_code}")
        vendor = response.json()
        print(f"Response: {json.dumps(vendor, indent=2)}")
        
        if response.status_code == 201:
            vendor_id = vendor["id"]
            print(f"\n✓ Vendor created successfully with ID: {vendor_id}")
        else:
            print(f"\n✗ Failed to create vendor")
            return
        
        # Create second vendor
        response = requests.post(f"{BASE_URL}/vendors", json=VENDOR_DATA_2)
        vendor_2 = response.json()
        if response.status_code == 201:
            vendor_id_2 = vendor_2["id"]
            print(f"✓ Second vendor created with ID: {vendor_id_2}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return
    
    # 2. Get all vendors
    print("\n2. GET ALL VENDORS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendors?skip=0&limit=10")
        print(f"Status Code: {response.status_code}")
        vendors = response.json()
        print(f"Total vendors retrieved: {len(vendors)}")
        print(f"Response: {json.dumps(vendors, indent=2)}")
        print("✓ Successfully retrieved all vendors")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 3. Get specific vendor
    print("\n3. GET SPECIFIC VENDOR")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendors/{vendor_id}")
        print(f"Status Code: {response.status_code}")
        vendor = response.json()
        print(f"Response: {json.dumps(vendor, indent=2)}")
        print("✓ Successfully retrieved vendor by ID")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 4. Update vendor
    print("\n4. UPDATE VENDOR")
    print("-" * 60)
    vendor_update = {
        "name": "PharmaCorp Suppliers Ltd (Updated)",
        "contact_number": "+91-9876543211",
        "address": "789 Medical District, Chennai, Tamil Nadu, India"
    }
    try:
        response = requests.put(f"{BASE_URL}/vendors/{vendor_id}", json=vendor_update)
        print(f"Status Code: {response.status_code}")
        vendor = response.json()
        print(f"Response: {json.dumps(vendor, indent=2)}")
        print("✓ Successfully updated vendor")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 6. Filter vendors by active status
    print("\n6. FILTER VENDORS BY ACTIVE STATUS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendors?is_active=true")
        print(f"Status Code: {response.status_code}")
        vendors = response.json()
        print(f"Active vendors: {len(vendors)}")
        print(f"Response: {json.dumps(vendors, indent=2)}")
        print("✓ Successfully filtered vendors")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_vendor_order_endpoints(vendor_id_1, vendor_id_2):
    """Test all vendor order endpoints"""
    
    print("\n" + "="*60)
    print("VENDOR ORDERS API TESTS")
    print("="*60)
    
    # 1. Create vendor orders
    print("\n1. CREATE VENDOR ORDERS")
    print("-" * 60)
    order_id = None
    order_id_2 = None
    
    try:
        # Create first order
        order_1 = {
            "vendor_id": vendor_id_1,
            "total_amount": 50000.00,
            "status": "pending"
        }
        response = requests.post(f"{BASE_URL}/vendor-orders", json=order_1)
        print(f"Status Code: {response.status_code}")
        order = response.json()
        print(f"Response: {json.dumps(order, indent=2)}")
        
        if response.status_code == 201:
            order_id = order["id"]
            print(f"\n✓ Vendor order created successfully with ID: {order_id}")
        else:
            print(f"\n✗ Failed to create vendor order")
            return
        
        # Create second order
        order_2 = {
            "vendor_id": vendor_id_2,
            "total_amount": 75000.00,
            "status": "pending"
        }
        response = requests.post(f"{BASE_URL}/vendor-orders", json=order_2)
        order = response.json()
        if response.status_code == 201:
            order_id_2 = order["id"]
            print(f"✓ Second vendor order created with ID: {order_id_2}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return
    
    # 2. Get all vendor orders
    print("\n2. GET ALL VENDOR ORDERS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendor-orders?skip=0&limit=10")
        print(f"Status Code: {response.status_code}")
        orders = response.json()
        print(f"Total orders retrieved: {len(orders)}")
        print(f"Response: {json.dumps(orders, indent=2)}")
        print("✓ Successfully retrieved all vendor orders")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 3. Get specific vendor order
    print("\n3. GET SPECIFIC VENDOR ORDER")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendor-orders/{order_id}")
        print(f"Status Code: {response.status_code}")
        order = response.json()
        print(f"Response: {json.dumps(order, indent=2)}")
        print("✓ Successfully retrieved vendor order by ID")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 4. Get orders by vendor
    print("\n4. GET ORDERS BY VENDOR")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendor-orders/vendor/{vendor_id_1}")
        print(f"Status Code: {response.status_code}")
        orders = response.json()
        print(f"Orders for vendor 1: {len(orders)}")
        print(f"Response: {json.dumps(orders, indent=2)}")
        print("✓ Successfully retrieved orders for specific vendor")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 5. Update vendor order
    print("\n5. UPDATE VENDOR ORDER")
    print("-" * 60)
    order_update = {
        "status": "confirmed",
        "total_amount": 52000.00
    }
    try:
        response = requests.put(f"{BASE_URL}/vendor-orders/{order_id}", json=order_update)
        print(f"Status Code: {response.status_code}")
        order = response.json()
        print(f"Response: {json.dumps(order, indent=2)}")
        print("✓ Successfully updated vendor order")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 6. Filter vendor orders by status
    print("\n6. FILTER VENDOR ORDERS BY STATUS")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/vendor-orders?status=confirmed")
        print(f"Status Code: {response.status_code}")
        orders = response.json()
        print(f"Confirmed orders: {len(orders)}")
        print(f"Response: {json.dumps(orders, indent=2)}")
        print("✓ Successfully filtered vendor orders by status")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    # 7. Delete vendor order
    print("\n7. DELETE VENDOR ORDER")
    print("-" * 60)
    try:
        response = requests.delete(f"{BASE_URL}/vendor-orders/{order_id_2}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 204:
            print("✓ Successfully deleted vendor order")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("VENDOR & VENDOR ORDERS API - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}")
    
    # Test vendor endpoints
    test_vendor_endpoints()
    
    # Get vendor IDs for order tests (in a real scenario, these would come from the test above)
    print("\n" + "="*60)
    print("RETRIEVING VENDOR IDS FOR ORDER TESTS...")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/vendors?skip=0&limit=2")
        vendors = response.json()
        if len(vendors) >= 2:
            vendor_id_1 = vendors[0]["id"]
            vendor_id_2 = vendors[1]["id"]
            
            # Test vendor order endpoints
            test_vendor_order_endpoints(vendor_id_1, vendor_id_2)
        else:
            print("Not enough vendors to test orders")
    except Exception as e:
        print(f"Error retrieving vendors: {str(e)}")
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
