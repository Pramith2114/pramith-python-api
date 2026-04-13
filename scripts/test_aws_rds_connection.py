#!/usr/bin/env python3
"""
Quick AWS RDS Connection Test Script

This script tests your AWS RDS connection without running the full application.
Useful for debugging connection issues.

Usage:
    python scripts/test_aws_rds_connection.py
"""

import sys
import os
from pathlib import Path
from sqlalchemy import text

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_aws_credentials():
    """Test if AWS credentials are configured"""
    print("🔍 Checking AWS Credentials...")
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials:
            print("✓ AWS credentials found")
            print(f"  Region: {session.region_name}")
            return True
        else:
            print("✗ No AWS credentials found")
            print("  Configure with: aws configure")
            return False
    except Exception as e:
        print(f"✗ Error checking credentials: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing Database Connection...")
    try:
        from app.database import engine
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"✓ Database connection successful!")
            print(f"  Query result: {value}")
            return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("  Make sure dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


def test_models():
    """Test if models can be imported and tables can be created"""
    print("\n🔍 Testing Models...")
    try:
        from app.database import engine, create_all_tables
        from app.models import Base
        
        print("✓ Models imported successfully")
        print(f"  Tables defined: {list(Base.metadata.tables.keys())}")
        
        # Try to create tables (idempotent operation)
        create_all_tables()
        print("✓ Tables created/verified in database")
        return True
    except Exception as e:
        print(f"✗ Error with models: {e}")
        return False


def test_health_endpoint():
    """Test application health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    try:
        import asyncio
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed")
            print(f"  Status: {data.get('status')}")
            print(f"  Database: {data.get('database')}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing health endpoint: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("AWS RDS Connection Test")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    results = {
        "AWS Credentials": test_aws_credentials(),
        "Database Connection": test_database_connection(),
        "Models": test_models(),
        "Health Endpoint": test_health_endpoint(),
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Everything looks good! Your AWS RDS connection is working.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
