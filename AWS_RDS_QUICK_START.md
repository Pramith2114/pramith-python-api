# Quick Start: AWS RDS Connection

This is a quick reference guide to connect your FastAPI app to AWS RDS PostgreSQL.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes `boto3` for AWS authentication.

## 2. Set Up AWS Credentials

### Option A: AWS CLI (Recommended)
```bash
aws configure
# Enter your AWS Access Key ID and Secret Access Key
```

### Option B: Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="eu-north-1"
```

### Option C: IAM Role (for EC2/Lambda)
Attach an IAM role with `rds-db:connect` permission to your compute resource.

## 3. Configure Your RDS Connection

Copy the configuration from `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your RDS details:
```env
USE_AWS_RDS=true
RDS_HOST=your-rds-endpoint.rds.amazonaws.com
RDS_PORT=5432
RDS_DATABASE=postgres
RDS_USERNAME=postgres
AWS_REGION=eu-north-1
USE_IAM_AUTH=true
```

## 4. Test the Connection

### Option A: Run Test Script
```bash
python scripts/test_aws_rds_connection.py
```

### Option B: Quick Python Test
```python
from app.database import engine

with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print("✓ Connected!", result.scalar())
```

### Option C: Generate Token Manually
```bash
python scripts/generate_rds_token.py --from-env
```

## 5. Start Your Application

```bash
uvicorn app.main:app --reload
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok", "database": "connected"}
```

## How It Works

### IAM Authentication Flow

1. **Generate Token**: boto3 requests a temporary token from AWS
   ```bash
   aws rds generate-db-auth-token \
     --hostname database-1.rds.amazonaws.com \
     --port 5432 \
     --username postgres \
     --region eu-north-1
   ```

2. **Token is Valid For**: 15 minutes (expires automatically)

3. **Use as Password**: The token replaces the regular password in your connection string
   ```
   postgresql://postgres:<TOKEN>@database-1.rds.amazonaws.com:5432/postgres
   ```

4. **Automatic Renewal**: The connection pool automatically regenerates expired tokens

### Security Benefits

- ✅ **No Static Passwords**: Uses temporary credentials that auto-expire
- ✅ **Audit Trail**: All database access is logged in AWS CloudTrail
- ✅ **Fine-Grained Access**: Control database access at the IAM policy level
- ✅ **Credential Rotation**: Tokens rotate every 15 minutes automatically

## File Structure

```
app/
├── config.py           # Database configuration
├── database.py         # Connection pool and session management
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── routes.py           # API routes with DB examples
└── main.py            # FastAPI app with DB initialization

scripts/
├── test_aws_rds_connection.py    # Test your connection
└── generate_rds_token.py         # Generate tokens manually

.env.example           # Configuration template
.env                   # Your actual configuration (create from example)
AWS_RDS_SETUP.md      # Detailed setup guide
```

## Common Commands

```bash
# Generate an auth token
python scripts/generate_rds_token.py --from-env

# Test your connection
python scripts/test_aws_rds_connection.py

# Connect directly with psql (using generated token)
export TOKEN=$(python scripts/generate_rds_token.py --from-env --output token-only)
psql -h $RDS_HOST -U $RDS_USERNAME -d postgres --sslmode=require password=$TOKEN

# Check database tables
curl http://localhost:8000/items

# Create an item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Item", "description": "A test"}'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Unknown user" | Verify database user has IAM auth enabled in RDS console |
| "Access Denied" | Check AWS credentials are configured correctly |
| "Connection timeout" | Verify RDS security group allows port 5432 from your IP |
| "Token expired" | This is normal; tokens auto-rotate in connection pool |
| "SSL certificate verify failed" | Update psycopg2: `pip install --upgrade psycopg2-binary` |

## Next Steps

- Read [AWS_RDS_SETUP.md](AWS_RDS_SETUP.md) for detailed configuration
- Check [app/routes.py](app/routes.py) for database usage examples
- See [app/database.py](app/database.py) for connection management details

## References

- [AWS RDS IAM Authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html)
- [boto3 RDS Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html)
- [SQLAlchemy PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
