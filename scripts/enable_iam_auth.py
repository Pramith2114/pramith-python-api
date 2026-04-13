#!/usr/bin/env python3
"""
Enable IAM Database Authentication on AWS RDS

This script helps you enable IAM authentication and grant the rds_iam role
to your database user using the AWS CLI.
"""

import subprocess
import sys


def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n📌 {description}")
    print(f"   Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ Success")
            if result.stdout:
                print(f"   Output: {result.stdout[:200]}")
            return True
        else:
            print(f"   ✗ Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"   ✗ Exception: {str(e)}")
        return False


def main():
    print("=" * 70)
    print("Enable IAM Database Authentication on AWS RDS")
    print("=" * 70)
    
    print("""
This guide will:
1. Enable IAM authentication on your RDS instance
2. Create/grant IAM role to your database user
3. Verify the setup

Prerequisites:
- AWS CLI installed and configured (aws configure)
- RDS instance running
- Database superuser credentials (for role grant)
""")
    
    # Get user input
    db_instance = input("\nEnter your RDS instance ID (e.g., database-1): ").strip()
    db_region = input("Enter AWS region (e.g., eu-north-1): ").strip()
    db_user = input("Enter database username (e.g., postgres): ").strip()
    
    if not all([db_instance, db_region, db_user]):
        print("❌ Missing required inputs")
        return 1
    
    print(f"\n{'=' * 70}")
    print(f"Configuration:")
    print(f"  Instance ID: {db_instance}")
    print(f"  Region: {db_region}")
    print(f"  Username: {db_user}")
    print(f"{'=' * 70}")
    
    # Step 1: Enable IAM authentication
    print("\n\n📍 STEP 1: Enable IAM Database Authentication")
    cmd = (
        f"aws rds modify-db-instance "
        f"--db-instance-identifier {db_instance} "
        f"--region {db_region} "
        f"--enable-iam-database-authentication "
        f"--apply-immediately"
    )
    step1_ok = run_command(cmd, "Enabling IAM database authentication...")
    
    if not step1_ok:
        print("""
⚠️  If you get "InvalidDBInstanceState" error, the instance may be:
   - Currently modifying
   - In an incompatible state
   - Already enabled
   
Try checking the console or waiting a few minutes and retrying.
""")
    
    # Step 2: Grant rds_iam role
    print("\n\n📍 STEP 2: Grant rds_iam Role to Database User")
    print(f"""
You need to connect to your RDS database and run:

    psql "host=<YOUR_RDS_ENDPOINT> port=5432 dbname=postgres \\
          user={db_user} sslmode=require"
    
Then execute:
    
    GRANT rds_iam TO {db_user};

Or use AWS CLI to get endpoint:
""")
    
    cmd = (
        f"aws rds describe-db-instances "
        f"--db-instance-identifier {db_instance} "
        f"--region {db_region} "
        f"--query 'DBInstances[0].Endpoint.Address' "
        f"--output text"
    )
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            endpoint = result.stdout.strip()
            print(f"\n🔗 Your RDS Endpoint: {endpoint}")
            print(f"\n📌 Run this command to connect:")
            print(f"   psql -h {endpoint} -U {db_user} -d postgres --sslmode=require")
            print(f"\n📌 Then in psql, run:")
            print(f"   GRANT rds_iam TO {db_user};")
        else:
            print(f"   Could not retrieve endpoint: {result.stderr}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 3: Verify
    print("\n\n📍 STEP 3: Verify IAM Authentication is Enabled")
    cmd = (
        f"aws rds describe-db-instances "
        f"--db-instance-identifier {db_instance} "
        f"--region {db_region} "
        f"--query 'DBInstances[0].IAMDatabaseAuthenticationEnabled' "
        f"--output text"
    )
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            status = result.stdout.strip()
            if status == "true":
                print(f"   ✓ IAM Authentication is ENABLED")
            else:
                print(f"   ⚠️  IAM Authentication is currently: {status}")
        else:
            print(f"   Error checking status: {result.stderr}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print(f"\n{'=' * 70}")
    print("Next Steps:")
    print("=" * 70)
    print("""
1. If IAM auth is not yet enabled, wait a few minutes for the change
   to take effect (you may need to reboot the instance)

2. Connect to your RDS and grant the rds_iam role:
   psql -h <YOUR_ENDPOINT> -U postgres -d postgres --sslmode=require
   GRANT rds_iam TO postgres;

3. Test your FastAPI app:
   uvicorn app.main:app --reload

4. Check the /health endpoint:
   curl http://localhost:8000/health
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
