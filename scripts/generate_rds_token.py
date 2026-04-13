#!/usr/bin/env python3
"""
AWS RDS Token Generation Example

This script demonstrates how to generate AWS RDS authentication tokens
for secure connections to your PostgreSQL database.

It's equivalent to the bash command:
    export RDSHOST="database-1.cluster-cj2sqc0u6bdr.eu-north-1.rds.amazonaws.com"
    aws rds generate-db-auth-token \\
        --hostname $RDSHOST \\
        --port 5432 \\
        --username postgres \\
        --region eu-north-1

"""

import sys
import argparse
from datetime import datetime


def generate_token(hostname, port, username, region):
    """
    Generate AWS RDS authentication token.
    
    Args:
        hostname: RDS endpoint (e.g., database-1.cluster-xxx.rds.amazonaws.com)
        port: Database port (default 5432)
        username: Database user
        region: AWS region (e.g., eu-north-1)
    
    Returns:
        Authentication token (valid for 15 minutes)
    """
    try:
        import boto3
    except ImportError:
        print("❌ Error: boto3 is not installed")
        print("   Install with: pip install boto3")
        sys.exit(1)
    
    try:
        client = boto3.client("rds", region_name=region)
        token = client.generate_db_auth_token(
            DBHostname=hostname,
            Port=port,
            DBUser=username,
            Region=region,
        )
        return token
    except Exception as e:
        print(f"❌ Error generating token: {e}")
        sys.exit(1)


def print_connection_examples(hostname, port, username, region, token):
    """Print connection examples for various tools"""
    
    print("\n" + "=" * 70)
    print(f"Generated Token (expires in 15 minutes)")
    print("=" * 70)
    print(f"\n{token}\n")
    
    print("=" * 70)
    print("Connection Examples")
    print("=" * 70)
    
    # psql example
    print("\n1️⃣  Using psql:")
    print(f"""
psql \\
  --host={hostname} \\
  --port={port} \\
  --user={username} \\
  --dbname=postgres \\
  --sslmode=require \\
  --password
# Paste the token when prompted for password
""")
    
    # Python example
    print("\n2️⃣  Using Python (psycopg2):")
    print(f"""
import psycopg2

conn = psycopg2.connect(
    host="{hostname}",
    port={port},
    user="{username}",
    password="{token}",
    database="postgres",
    sslmode="require"
)
cursor = conn.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchone())
cursor.close()
conn.close()
""")
    
    # SQLAlchemy example
    print("\n3️⃣  Using SQLAlchemy:")
    print(f"""
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql://{{username}}:{{token}}"
    f"@{{hostname}}:{{port}}/postgres",
    connect_args={{"sslmode": "require"}}
)

with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.fetchone())
""")
    
    # Environment variable example
    print("\n4️⃣  Using environment variables:")
    print(f"""
export RDS_HOST="{hostname}"
export RDS_PORT={port}
export RDS_USER="{username}"
export RDS_REGION="{region}"
export RDS_TOKEN="{token}"

psql \\
  --host=$RDS_HOST \\
  --port=$RDS_PORT \\
  --user=$RDS_USER \\
  --sslmode=require \\
  --password
# Enter $RDS_TOKEN as password
""")


def main():
    parser = argparse.ArgumentParser(
        description="Generate AWS RDS authentication token",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using command line arguments
  python scripts/generate_rds_token.py \\
    --host database-1.cluster-cj2sqc0u6bdr.eu-north-1.rds.amazonaws.com \\
    --user postgres \\
    --region eu-north-1
  
  # Using environment variables (from .env)
  python scripts/generate_rds_token.py --from-env
        """
    )
    
    parser.add_argument(
        "--host",
        help="RDS hostname (e.g., database-1.cluster-xxx.rds.amazonaws.com)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5432,
        help="Database port (default: 5432)"
    )
    parser.add_argument(
        "--user",
        help="Database username"
    )
    parser.add_argument(
        "--region",
        help="AWS region (e.g., eu-north-1)"
    )
    parser.add_argument(
        "--from-env",
        action="store_true",
        help="Read configuration from .env file"
    )
    parser.add_argument(
        "--output",
        choices=["full", "token-only", "json"],
        default="full",
        help="Output format (default: full)"
    )
    
    args = parser.parse_args()
    
    # Load from environment or arguments
    if args.from_env:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        hostname = os.getenv("RDS_HOST")
        port = int(os.getenv("RDS_PORT", "5432"))
        username = os.getenv("RDS_USERNAME")
        region = os.getenv("AWS_REGION")
        
        if not all([hostname, username, region]):
            print("❌ Error: Missing required environment variables")
            print("   Make sure .env file has: RDS_HOST, RDS_USERNAME, AWS_REGION")
            sys.exit(1)
    else:
        if not all([args.host, args.user, args.region]):
            parser.print_help()
            sys.exit(1)
        
        hostname = args.host
        port = args.port
        username = args.user
        region = args.region
    
    # Generate token
    print(f"\n🔄 Generating token for {username}@{hostname}:{port} in {region}...\n")
    token = generate_token(hostname, port, username, region)
    
    # Output based on format
    if args.output == "token-only":
        print(token)
    elif args.output == "json":
        import json
        output = {
            "token": token,
            "hostname": hostname,
            "port": port,
            "username": username,
            "region": region,
            "expires_in_seconds": 900,  # 15 minutes
            "generated_at": datetime.utcnow().isoformat()
        }
        print(json.dumps(output, indent=2))
    else:  # full
        print_connection_examples(hostname, port, username, region, token)
    
    print("\n" + "=" * 70)
    print("⏱️  Token is valid for 15 minutes")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
