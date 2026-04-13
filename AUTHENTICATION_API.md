# Authentication API Documentation

## Overview

This API provides two authentication methods:
1. **Username/Password Authentication** - Traditional login mechanism
2. **OTP-Based Authentication** - Mobile number verification using One-Time Passwords

The API automatically creates the database schema on startup with the following tables:
- `users` - User accounts with support for multiple auth methods
- `otps` - One-Time Password records for mobile verification

## Database Schema Auto-Creation

When the API starts, it automatically:
✓ Checks if tables exist
✓ Creates missing tables from SQLAlchemy models
✓ Initializes all indexes
✓ Sets up proper constraints

No manual database setup is required!

---

## API Endpoints

### Authentication Routes

#### 1. Register User (Username/Password)

**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "mobile_number": "+1234567890"  // Optional
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "mobile_number": "+1234567890",
  "is_active": true,
  "is_verified": true,
  "created_at": "2026-04-13T18:32:59.426679",
  "updated_at": "2026-04-13T18:32:59.426684"
}
```

**Error Cases:**
- `409 Conflict` - Username or email already registered
- `422 Unprocessable Entity` - Password too short (<6 characters)

---

#### 2. Login with Username/Password

**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "mobile_number": "+1234567890",
    "is_active": true,
    "is_verified": true,
    "created_at": "2026-04-13T18:32:59.426679",
    "updated_at": "2026-04-13T18:32:59.426684"
  }
}
```

**Error Cases:**
- `401 Unauthorized` - Invalid username or password
- `403 Forbidden` - User account is deactivated

---

#### 3. Request OTP for Mobile

**Endpoint:** `POST /api/auth/otp/send`

**Request Body:**
```json
{
  "mobile_number": "+919876543210"
}
```

**Response:** `200 OK`
```json
{
  "message": "OTP sent to +919876543210",
  "mobile_number": "+919876543210",
  "expires_in_seconds": 300
}
```

**Notes:**
- OTP is valid for 5 minutes (300 seconds)
- OTP format: 6-digit numeric code
- For development, OTP is printed in server logs
- In production, integrate with SMS service (Twilio, AWS SNS, etc.)

**Error Cases:**
- `400 Bad Request` - Invalid mobile number format

---

#### 4. Verify OTP and Authenticate

**Endpoint:** `POST /api/auth/otp/verify`

**Request Body:**
```json
{
  "mobile_number": "+919876543210",
  "otp_code": "123456"
}
```

**Response:** `200 OK`
```json
{
  "message": "OTP verified successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "username": "mobile_user_919876543210",
    "email": null,
    "mobile_number": "+919876543210",
    "is_active": true,
    "is_verified": true,
    "created_at": "2026-04-13T18:32:59.426679",
    "updated_at": "2026-04-13T18:32:59.426684"
  }
}
```

**Auto-User Creation:**
- If the mobile number is new, a user account is automatically created
- Username format: `mobile_user_{cleaned_number}`
- Email is not required for mobile-only users

**Error Cases:**
- `404 Not Found` - OTP not found or expired
- `401 Unauthorized` - Invalid OTP code
- `429 Too Many Requests` - Maximum OTP attempts exceeded (5)

---

#### 5. Health Check

**Endpoint:** `GET /api/auth/health`

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "authentication",
  "timestamp": "2026-04-13T18:32:59.426679"
}
```

---

## Database Schema

### Users Table
```
users (
  id INTEGER PRIMARY KEY,
  email VARCHAR(255) UNIQUE NULLABLE,
  username VARCHAR(255) UNIQUE NOT NULL,
  mobile_number VARCHAR(20) UNIQUE NULLABLE,
  password_hash VARCHAR(255) NULLABLE,
  is_active BOOLEAN DEFAULT True,
  is_verified BOOLEAN DEFAULT False,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
)
```

### OTPs Table
```
otps (
  id INTEGER PRIMARY KEY,
  mobile_number VARCHAR(20) NOT NULL,
  otp_code VARCHAR(6) NOT NULL,
  is_verified BOOLEAN DEFAULT False,
  attempts INTEGER DEFAULT 0,
  max_attempts INTEGER DEFAULT 5,
  created_at TIMESTAMP DEFAULT now(),
  expires_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT now()
)
```

---

## Security Features

1. **Password Hashing**
   - Uses bcrypt algorithm
   - Passwords never stored in plaintext
   - Automatic salt generation

2. **JWT Tokens**
   - Algorithm: HS256
   - Default expiration: 30 minutes
   - Configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` env var

3. **OTP Security**
   - 6-digit numeric codes
   - Expiration: 5 minutes (configurable)
   - Max 5 verification attempts per OTP
   - Prevents brute force attacks

4. **Input Validation**
   - Mobile number format validation
   - Email validation (RFC compliant)
   - Password strength requirements (minimum 6 chars)

---

## Configuration

### Environment Variables

```env
# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
OTP_EXPIRE_MINUTES=5

# Database
USE_AWS_RDS=true
RDS_HOST=your-rds-endpoint
RDS_PORT=5432
RDS_DATABASE=postgres
RDS_USERNAME=username
RDS_PASSWORD=password
RDS_REGION=eu-north-1
```

---

## Usage Examples

### Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api/auth"

# Register
response = requests.post(f"{BASE_URL}/register", json={
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "mobile_number": "+1234567890"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/login", json={
    "username": "john_doe",
    "password": "SecurePass123!"
})
token = response.json()["access_token"]

# Use token for protected routes
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/items", headers=headers)
```

### cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "mobile_number": "+1234567890"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePass123!"
  }'

# Request OTP
curl -X POST http://localhost:8000/api/auth/otp/send \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919876543210"
  }'

# Verify OTP
curl -X POST http://localhost:8000/api/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number": "+919876543210",
    "otp_code": "123456"
  }'
```

---

## Running the API

### Start the Server

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Run Tests

```bash
# Run authentication flow tests
python3 test_auth_flow.py
```

---

## Future Enhancements

1. **SMS Integration**
   - Twilio
   - AWS SNS
   - Firebase Cloud Messaging

2. **Email Verification**
   - Email confirmation tokens
   - Password reset functionality
   - Email-based OTP

3. **Rate Limiting**
   - Prevent brute force attacks
   - API rate limiting

4. **Audit Logging**
   - Track login attempts
   - Log password changes
   - Record OTP usage

5. **Two-Factor Authentication (2FA)**
   - TOTP implementation
   - Backup codes

6. **Token Refresh**
   - Refresh token mechanism
   - Token rotation

---

## Troubleshooting

### OTP Not Appearing in Logs
Make sure the server is running in development mode. In production, configure an SMS service.

### Database Connection Errors
Check your RDS endpoint and credentials in the `.env` file.

### Invalid Email Address
For mobile-only users registered via OTP, the email field is set to `null`. This is expected behavior.

### Token Expired
Tokens are valid for 30 minutes by default. Request a new token by logging in again.

---

## Support

For issues or questions, please open an issue on the GitHub repository.
