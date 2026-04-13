# Pramith API - Authentication System Setup Complete! ✓

## What Has Been Created

### 1. **Database Models** (`app/models.py`)
- **User Model** - Supports both username/password and mobile-based authentication
  - `id` - User ID
  - `username` - Unique username
  - `email` - Optional (for mobile-only users)
  - `mobile_number` - Optional mobile for OTP login
  - `password_hash` - Bcrypt hashed passwords
  - `is_active` - Account status
  - `is_verified` - Verification status
  - `created_at`, `updated_at` - Timestamps

- **OTP Model** - Mobile OTP verification
  - `mobile_number` - Target mobile
  - `otp_code` - 6-digit code
  - `attempts` - Failed attempts counter
  - `max_attempts` - Max attempts limit (5)
  - `expires_at` - OTP expiration time

### 2. **Authentication Utilities** (`app/utils.py`)
- Password hashing and verification (bcrypt with fallback to pbkdf2)
- OTP generation (random 6-digit codes)
- JWT token creation and verification
- Mobile number validation

### 3. **API Endpoints** (`app/auth.py`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Register new user with username/password |
| POST | `/api/auth/login` | Login with username/password |
| POST | `/api/auth/otp/send` | Request OTP for mobile number |
| POST | `/api/auth/otp/verify` | Verify OTP and authenticate |
| GET | `/api/auth/health` | Health check endpoint |

### 4. **Request/Response Schemas** (`app/schemas.py`)
- Complete Pydantic models for validation
- Type hints for all request/response objects
- Email and mobile number validation

---

## Auto-Database Schema Creation

The API automatically creates and manages the database schema. When the API starts:

```python
@app.on_event("startup")
async def startup():
    create_all_tables()  # Automatically creates all tables!
```

**Tables Created:**
- ✓ `users` - User accounts
- ✓ `otps` - OTP records
- ✓ `items` - Example items table (existing)

No manual SQL or migrations needed!

---

## Quick Start

### 1. Install Dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the API
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will automatically create tables on startup.

### 3. Access Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "mobile_number": "+1234567890"
  }'
```

### Login with Username/Password
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'
```

### Request OTP
```bash
curl -X POST http://localhost:8000/api/auth/otp/send \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919876543210"
  }'
```

### Verify OTP (Check server logs for OTP code)
```bash
curl -X POST http://localhost:8000/api/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919876543210",
    "otp_code": "123456"
  }'
```

---

## Files Created/Modified

### New Files
- ✓ `app/auth.py` - Authentication routes (register, login, OTP endpoints)
- ✓ `app/utils.py` - Authentication utilities and helpers
- ✓ `AUTHENTICATION_API.md` - Complete API documentation
- ✓ `test_auth_flow.py` - Comprehensive test suite

### Modified Files
- ✓ `app/models.py` - Updated User model + added OTP model
- ✓ `app/schemas.py` - Added auth schemas (Login, OTP, etc.)
- ✓ `app/main.py` - Registered auth router
- ✓ `requirements.txt` - Added passlib, PyJWT dependencies

---

## Authentication Features

### ✓ Username/Password Authentication
- Register with username, email, password
- Login to get JWT token
- Password hashing with bcrypt
- Email uniqueness validation

### ✓ Mobile OTP Authentication
- Request OTP for any mobile number
- 6-digit numeric code (expires in 5 minutes)
- Verify OTP to get JWT token
- Auto-create user on first OTP verification
- Max 5 failed attempts per OTP

### ✓ Security
- Bcrypt password hashing
- JWT token-based authentication (HS256)
- Email and mobile validation
- Rate limiting on OTP attempts
- Automatic token expiration (30 minutes)

---

## Database Configuration

The `.env` file already has RDS configuration:
```env
USE_AWS_RDS=true
RDS_HOST=database-1.cj2sqc0u6bdr.eu-north-1.rds.amazonaws.com
RDS_PORT=5432
RDS_DATABASE=postgres
RDS_USERNAME=pramith2114
RDS_PASSWORD=karthikr2114
USE_IAM_AUTH=false
```

Tables are created automatically on API startup!

---

## Testing

Run the comprehensive test suite:
```bash
source .venv/bin/activate
python3 test_auth_flow.py
```

**Test Coverage:**
- ✓ User Registration
- ✓ User Login
- ✓ OTP Generation
- ✓ OTP Verification
- ✓ Auto User Creation
- ✓ JWT Token Generation
- ✓ Health Check

---

## Next Steps

### Optional: Integrate SMS Service
Replace the mock OTP logging with a real SMS provider:

```python
# In app/auth.py, replace the print statement with:
# For Twilio:
from twilio.rest import Client
client = Client(account_sid, auth_token)
client.messages.create(
    to=request.mobile_number,
    from_=twilio_number,
    body=f"Your OTP is {otp_code}"
)

# For AWS SNS:
import boto3
sns = boto3.client('sns', region_name=settings.AWS_REGION)
sns.publish(PhoneNumber=request.mobile_number, Message=f"OTP: {otp_code}")
```

### Optional: Add JWT Middleware
Create protected routes that require authentication:

```python
from fastapi import Depends, HTTPException
from app.utils import verify_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = verify_token(token).get("sub")
    # Load user from database
    return user
```

---

## Documentation

Complete API documentation available in [AUTHENTICATION_API.md](AUTHENTICATION_API.md):
- Detailed endpoint documentation
- Request/response examples
- Error handling
- Security features
- Configuration guide
- Troubleshooting

---

## Support

All tables are auto-created on API startup. No manual SQL queries needed!

For issues:
1. Check server logs for errors
2. Verify database connection in `.env`
3. Run `test_auth_flow.py` to diagnose issues

Happy coding! 🚀
