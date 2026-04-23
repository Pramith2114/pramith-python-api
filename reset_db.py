#!/usr/bin/env python3
"""
Fix database schema by dropping and recreating all tables
Run this script to reset your database schema
"""

import os
import sys
from sqlalchemy import text

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.database import engine, drop_all_tables, create_all_tables


def reset_database():
    """Drop all existing tables and recreate them with correct schema"""
    
    print("⚠️  WARNING: This will delete ALL data from your database!")
    confirm = input("Type 'yes' to proceed: ")
    
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return
    
    try:
        print("\n🗑️  Dropping all existing tables...")
        drop_all_tables()
        print("✓ Tables dropped successfully")
        
        print("\n📊 Creating new tables with correct schema...")
        create_all_tables()
        print("✓ Tables created successfully")
        
        print("\n✅ Database schema has been reset!")
        print("You can now use the API without errors.\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure your AWS RDS database is running")
        print("2. Check that RDS_HOST, RDS_USERNAME, RDS_PASSWORD are correct in .env")
        print("3. Check database permissions")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE SCHEMA RESET TOOL")
    print("=" * 60)
    print(f"\nDatabase: {settings.RDS_HOST}:{settings.RDS_PORT}/{settings.RDS_DATABASE}")
    print(f"User: {settings.RDS_USERNAME}\n")
    
    success = reset_database()
    sys.exit(0 if success else 1)
