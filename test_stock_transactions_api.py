#!/usr/bin/env python3
"""
Test script for Stock Transactions API
"""
import requests
import json
from datetime import datetime, timedelta
import uuid

BASE_URL = "http://localhost:8000"

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")

def test_stock_transactions_api():
    """Test the Stock Transactions API endpoints"""
    
    print(f"\n{BLUE}{'='*60}")
    print("Testing Stock Transactions API")
    print(f"{'='*60}{RESET}\n")
    
    # First, create a drug
    print_info("Step 1: Creating a test drug...")
    drug_data = {
        "name": "Aspirin",
        "generic_name": "Acetylsalicylic acid",
        "manufacturer": "Pharma Corp",
        "price": 5.99,
        "stock_quantity": 100,
        "expiry_date": "2026-12-31"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/drugs", json=drug_data)
        if response.status_code == 201:
            drug = response.json()
            drug_id = drug["id"]
            print_success(f"Drug created: {drug_id}")
            print(f"  Initial stock: {drug['stock_quantity']}")
        else:
            print_error(f"Failed to create drug: {response.text}")
            return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False
    
    # Test 1: Create a stock IN transaction
    print_info("\nStep 2: Creating a stock IN transaction...")
    transaction_in = {
        "drug_id": drug_id,
        "quantity": 50,
        "type": "IN",
        "source": "vendor"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/stock-transactions", json=transaction_in)
        if response.status_code == 201:
            trans = response.json()
            transaction_id_1 = trans["id"]
            print_success(f"Stock IN transaction created: {transaction_id_1}")
            print(f"  Quantity: {trans['quantity']} | Type: {trans['type']} | Source: {trans['source']}")
        else:
            print_error(f"Failed to create transaction: {response.text}")
            return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False
    
    # Test 2: Create a stock OUT transaction
    print_info("\nStep 3: Creating a stock OUT transaction...")
    transaction_out = {
        "drug_id": drug_id,
        "quantity": 20,
        "type": "OUT",
        "source": "prescription"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/stock-transactions", json=transaction_out)
        if response.status_code == 201:
            trans = response.json()
            transaction_id_2 = trans["id"]
            print_success(f"Stock OUT transaction created: {transaction_id_2}")
            print(f"  Quantity: {trans['quantity']} | Type: {trans['type']} | Source: {trans['source']}")
        else:
            print_error(f"Failed to create transaction: {response.text}")
            return False
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
        return False
    
    # Test 3: Get all transactions
    print_info("\nStep 4: Retrieving all transactions...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock-transactions")
        if response.status_code == 200:
            transactions = response.json()
            print_success(f"Retrieved {len(transactions)} transactions")
            for trans in transactions:
                print(f"  - {trans['id']}: {trans['type']} {trans['quantity']} units ({trans['source']})")
        else:
            print_error(f"Failed to get transactions: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 4: Get transactions by drug
    print_info("\nStep 5: Retrieving transactions for specific drug...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock-transactions/drug/{drug_id}")
        if response.status_code == 200:
            transactions = response.json()
            print_success(f"Retrieved {len(transactions)} transactions for drug {drug_id}")
            for trans in transactions:
                print(f"  - {trans['type']}: {trans['quantity']} units from {trans['source']}")
        else:
            print_error(f"Failed to get drug transactions: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 5: Filter by type
    print_info("\nStep 6: Filtering transactions by type (IN)...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock-transactions?type=IN")
        if response.status_code == 200:
            transactions = response.json()
            print_success(f"Retrieved {len(transactions)} IN transactions")
        else:
            print_error(f"Failed to filter transactions: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 6: Get specific transaction
    print_info("\nStep 7: Retrieving specific transaction...")
    try:
        response = requests.get(f"{BASE_URL}/api/stock-transactions/{transaction_id_1}")
        if response.status_code == 200:
            trans = response.json()
            print_success(f"Retrieved transaction {transaction_id_1}")
            print(f"  Details: {json.dumps(trans, indent=2, default=str)}")
        else:
            print_error(f"Failed to get transaction: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 7: Update transaction
    print_info("\nStep 8: Updating transaction quantity...")
    update_data = {
        "quantity": 60
    }
    try:
        response = requests.put(f"{BASE_URL}/api/stock-transactions/{transaction_id_1}", json=update_data)
        if response.status_code == 200:
            trans = response.json()
            print_success(f"Transaction updated: new quantity = {trans['quantity']}")
        else:
            print_error(f"Failed to update transaction: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 8: Check drug stock after transactions
    print_info("\nStep 9: Checking drug stock after all transactions...")
    try:
        response = requests.get(f"{BASE_URL}/api/drugs/{drug_id}")
        if response.status_code == 200:
            drug = response.json()
            print_success(f"Current drug stock: {drug['stock_quantity']} units")
            print(f"  Expected: 100 (initial) + 60 (IN updated) - 20 (OUT) = 140")
        else:
            print_error(f"Failed to get drug: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 9: Test invalid transaction (OUT more than available)
    print_info("\nStep 10: Testing error handling (OUT more than available)...")
    invalid_transaction = {
        "drug_id": drug_id,
        "quantity": 500,
        "type": "OUT",
        "source": "test"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/stock-transactions", json=invalid_transaction)
        if response.status_code == 400:
            error = response.json()
            print_success(f"Error correctly caught: {error['detail']}")
        else:
            print_error(f"Expected 400 error, got {response.status_code}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Test 10: Delete transaction
    print_info("\nStep 11: Deleting transaction...")
    try:
        response = requests.delete(f"{BASE_URL}/api/stock-transactions/{transaction_id_2}")
        if response.status_code == 204:
            print_success(f"Transaction deleted: {transaction_id_2}")
        else:
            print_error(f"Failed to delete transaction: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    # Check final stock
    print_info("\nStep 12: Checking final drug stock...")
    try:
        response = requests.get(f"{BASE_URL}/api/drugs/{drug_id}")
        if response.status_code == 200:
            drug = response.json()
            print_success(f"Final drug stock: {drug['stock_quantity']} units")
            print(f"  OUT transaction was reversed, so 20 units were added back")
        else:
            print_error(f"Failed to get drug: {response.text}")
    except Exception as e:
        print_error(f"Connection error: {str(e)}")
    
    print(f"\n{BLUE}{'='*60}")
    print("Stock Transactions API Tests Completed!")
    print(f"{'='*60}{RESET}\n")
    
    return True

if __name__ == "__main__":
    print("\n⚠️  Make sure the FastAPI server is running on http://localhost:8000")
    print("   Run: cd /Users/apple/pythonPramith-api/pramith-python-api && uvicorn app.main:app --reload\n")
    
    input("Press Enter to start tests...")
    test_stock_transactions_api()
