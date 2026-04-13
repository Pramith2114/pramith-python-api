# Fix: Enable IAM Authentication on AWS RDS

## Problem
Your RDS instance doesn't have IAM database authentication enabled yet.

Error: `FATAL: PAM authentication failed for user "postgres"`

## Solution: 3 Steps

### Step 1: Enable IAM Authentication on RDS Instance

Using AWS CLI:
```bash
aws rds modify-db-instance \
  --db-instance-identifier database-1 \
  --region eu-north-1 \
  --enable-iam-database-authentication \
  --apply-immediately
```

Or via AWS Console:
1. Go to RDS → Databases
2. Click on your database
3. Click **Modify**
4. Scroll to **Database authentication**
5. Select **Enable IAM database authentication**
6. Click **Continue** → **Apply immediately**

⏳ **Wait 2-5 minutes** for the change to take effect

### Step 2: Check If IAM Auth is Enabled

```bash
aws rds describe-db-instances \
  --db-instance-identifier database-1 \
  --region eu-north-1 \
  --query 'DBInstances[0].IAMDatabaseAuthenticationEnabled' \
  --output text
```

Expected output: `true`

### Step 3: Grant rds_iam Role to Your Database User

First, get your RDS endpoint:
```bash
aws rds describe-db-instances \
  --db-instance-identifier database-1 \
  --region eu-north-1 \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text
```

Connect to your database (using regular password authentication first):
```bash
psql -h database-1.cluster-cj2sqc0u6bdr.eu-north-1.rds.amazonaws.com \
     -U postgres \
     -d postgres \
     --sslmode=require
```

When prompted for password, use the original postgres password (not the IAM token).

Then run this SQL command:
```sql
GRANT rds_iam TO postgres;
```

Verify the role was granted:
```sql
SELECT usename, usecanlogin FROM pg_user WHERE usename = 'postgres';
SELECT rolname FROM pg_roles WHERE oid IN (
  SELECT memberid FROM pg_auth_members 
  WHERE roleid = (SELECT oid FROM pg_roles WHERE rolname = 'rds_iam')
);
```

## Testing the Setup

### Option 1: Run the Auto-Setup Script
```bash
source .venv/bin/activate
python scripts/enable_iam_auth.py
```

### Option 2: Manual Test
```bash
source .venv/bin/activate

# Test token generation
python -c "
from app.database import get_database_url
try:
    url = get_database_url()
    print('✓ Token generated successfully!')
except Exception as e:
    print(f'✗ Failed: {e}')
"
```

### Option 3: Start the App
```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/health

Expected response:
```json
{"status": "ok", "database": "connected"}
```

## Troubleshooting

### "Still getting PAM authentication failed"
- ✓ Confirm IAM auth is enabled (Step 2 should return `true`)
- ✓ Confirm rds_iam role was granted to the user
- ✓ Wait a few more minutes and try again
- ✓ Check RDS instance status (might need reboot)

### "database user does not have required CONNECT permission"
- The user doesn't have rds_iam role
- Run: `GRANT rds_iam TO postgres;`

### "Connection timeout"
- Check RDS security group allows port 5432
- Verify RDS instance is publicly accessible
- Test with: `telnet <endpoint> 5432`

### "SSL certificate verify failed"
Update psycopg2:
```bash
pip install --upgrade psycopg2-binary
```

## What Happens Next

Once IAM auth is enabled and the role is granted:

1. Your FastAPI app will generate temporary tokens automatically
2. Each token is valid for 15 minutes
3. Tokens auto-rotate in the connection pool
4. No passwords stored in `.env` - much more secure! 🔐

## References

- [AWS RDS IAM Authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [PostgreSQL GRANT Command](https://www.postgresql.org/docs/current/sql-grant.html)
- [boto3 generate_db_auth_token](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.Client.generate_db_auth_token)
