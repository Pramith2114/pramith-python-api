# AWS RDS Database Connection Guide

This guide explains how to connect your FastAPI application to AWS RDS PostgreSQL with IAM authentication.

## Overview

There are two ways to authenticate with AWS RDS:

1. **IAM Authentication (Recommended)** - Uses temporary, auto-rotating credentials
2. **Static Password** - Uses traditional username/password

## Prerequisites

- AWS Account with RDS PostgreSQL instance
- AWS CLI installed and configured
- Python 3.10+
- boto3 package installed

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
# Or just the AWS dependency:
pip install boto3
```

### 2. Configure AWS Credentials

AWS RDS IAM authentication requires AWS credentials. Set them up using one of these methods:

#### Option A: AWS CLI Configuration (Recommended)
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., eu-north-1)
# Enter your default output format (json)
```

Configuration is stored in `~/.aws/credentials` and `~/.aws/config`

#### Option B: Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="eu-north-1"
```

#### Option C: IAM Role (for EC2/Lambda/ECS)
If running on AWS infrastructure, attach an IAM role with policy:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "rds-db:connect"
            ],
            "Resource": [
                "arn:aws:rds:eu-north-1:ACCOUNT-ID:db:database-1"
            ]
        }
    ]
}
```

### 3. Configure Environment Variables

Create a `.env` file in your project root:

```bash
# AWS RDS Configuration
USE_AWS_RDS=true
RDS_HOST=database-1.cluster-cj2sqc0u6bdr.eu-north-1.rds.amazonaws.com
RDS_PORT=5432
RDS_DATABASE=postgres
RDS_USERNAME=postgres
AWS_REGION=eu-north-1
USE_IAM_AUTH=true
```

Replace the values with your actual RDS details:
- `RDS_HOST` - Your RDS endpoint
- `RDS_USERNAME` - Database user (must have IAM authentication enabled)
- `RDS_DATABASE` - Database name
- `AWS_REGION` - AWS region where RDS is hosted

### 4. Enable IAM Authentication for Database User

In your RDS instance, create a database user with IAM authentication:

```bash
# Connect to your RDS instance
psql "host=$RDSHOST port=5432 dbname=postgres user=postgres sslmode=require"

# Create IAM-authenticated user (PostgreSQL)
CREATE USER iam_user;
GRANT rds_iam TO iam_user;

# Create a regular user for initial setup (use static password)
CREATE USER postgres WITH PASSWORD 'your-password';
ALTER USER postgres CREATEDB;
```

Or use the RDS console to modify user settings.

### 5. Test the Connection

Run this Python script to verify your connection:

```python
from app.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✓ Database connection successful!")
except Exception as e:
    print(f"✗ Connection failed: {e}")
```

## Usage in Application

Once configured, your FastAPI routes automatically use the database connection:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserCreate

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## Manual Connection Test (Advanced)

To manually test your RDS connection from the command line:

```bash
# Set variables
export RDSHOST="database-1.cluster-cj2sqc0u6bdr.eu-north-1.rds.amazonaws.com"
export RDS_USER="postgres"
export AWS_REGION="eu-north-1"

# Generate auth token (valid for 15 minutes)
export TOKEN=$(aws rds generate-db-auth-token \
  --hostname $RDSHOST \
  --port 5432 \
  --username $RDS_USER \
  --region $AWS_REGION)

# Connect with psql
psql "host=$RDSHOST port=5432 dbname=postgres user=$RDS_USER sslmode=require password=$TOKEN"
```

## Security Best Practices

1. **Don't use static passwords** - Always use IAM authentication when possible
2. **Rotate credentials** - IAM tokens automatically expire after 15 minutes
3. **Use SSL/TLS** - Always enabled for AWS RDS connections
4. **Limit database user privileges** - Create dedicated users with minimal permissions
5. **Store secrets securely** - Use AWS Secrets Manager, not `.env` files in production
6. **Enable encryption** - Enable at-rest and in-transit encryption for your RDS instance

## Troubleshooting

### "Access Denied" / "Unknown User"
- Verify the database user exists and has IAM authentication enabled
- Check AWS credentials are correctly configured
- Ensure IAM policy includes `rds-db:connect` permission

### "Connection Timeout"
- Check RDS security group allows inbound traffic on port 5432
- Verify RDS instance is publicly accessible (if needed)
- Check network connectivity with: `telnet $RDSHOST 5432`

### "SSL Certificate Verify Failed"
- Ensure `sslmode=require` is set in connection string
- Update psycopg2: `pip install --upgrade psycopg2-binary`
- Download and use RDS CA certificate:
  ```bash
  wget https://truststore.pem.rds.amazonaws.com/global/global-bundle.pem
  # Set in .env: RDS_SSL_CERT_PATH=/path/to/global-bundle.pem
  ```

### "Token Expired"
- IAM tokens expire after 15 minutes; if connection pooling is enabled, tokens are regenerated automatically
- Ensure `pool_pre_ping=True` is set in database.py (already configured)

## Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your RDS details
cp .env.example .env
# Edit .env with your RDS configuration

# Run the application
uvicorn app.main:app --reload

# Test the health check
curl http://localhost:8000/health
```

## Environment-Specific Configuration

### Development (Local PostgreSQL)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/pramith_db
```

### Staging (AWS RDS with IAM)
```env
USE_AWS_RDS=true
RDS_HOST=staging-db.cluster-xxx.eu-north-1.rds.amazonaws.com
RDS_USERNAME=app_user
USE_IAM_AUTH=true
```

### Production (AWS RDS with IAM + Secrets Manager)
Use AWS Secrets Manager to store database credentials instead of `.env` files:

```python
import json
import boto3

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])
```

## References

- [AWS RDS IAM Authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [SQLAlchemy PostgreSQL Documentation](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [boto3 RDS Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.generate_db_auth_token)
