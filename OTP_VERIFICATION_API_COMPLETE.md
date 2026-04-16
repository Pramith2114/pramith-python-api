# OTP Verification API Documentation

## Overview

The OTP Verification API provides complete functionality for managing One-Time Password (OTP) verification records. It enables storing, verifying, and managing OTPs for mobile-based authentication and verification purposes.

## Database Table Schema

```sql
CREATE TABLE otp_verifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mobile VARCHAR(20) NOT NULL,
    otp VARCHAR(10) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_otp_verifications_mobile ON otp_verifications(mobile);
CREATE INDEX idx_otp_verifications_expires_at ON otp_verifications(expires_at);
CREATE INDEX idx_otp_verifications_is_verified ON otp_verifications(is_verified);
CREATE INDEX idx_otp_verifications_created_at ON otp_verifications(created_at);
```

## API Endpoints

### 1. Create OTP Verification Record

**Endpoint:** `POST /api/otp-verification`

**Description:** Create a new OTP verification record for a mobile number

**Request Body:**
```json
{
  "mobile": "+919876543210",
  "otp": "123456",
  "expires_at": "2026-04-16T12:30:00"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "mobile": "+919876543210",
  "otp": "123456",
  "expires_at": "2026-04-16T12:30:00",
  "is_verified": false,
  "created_at": "2026-04-16T11:30:00",
  "updated_at": "2026-04-16T11:30:00"
}
```

**Error Cases:**
- `400 Bad Request`: An active OTP already exists for this mobile number
- `422 Unprocessable Entity`: Invalid input format

---

### 2. Get All OTP Verification Records

**Endpoint:** `GET /api/otp-verification`

**Description:** Retrieve all OTP verification records with optional filtering

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 10)
- `mobile` (string, optional): Filter by mobile number
- `is_verified` (boolean, optional): Filter by verification status

**Examples:**
```bash
# Get all OTPs
curl -X GET "http://localhost:8000/api/otp-verification"

# Get unverified OTPs
curl -X GET "http://localhost:8000/api/otp-verification?is_verified=false"

# Get OTPs for specific mobile
curl -X GET "http://localhost:8000/api/otp-verification?mobile=%2B919876543210"

# Pagination
curl -X GET "http://localhost:8000/api/otp-verification?skip=0&limit=5"
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "mobile": "+919876543210",
    "otp": "123456",
    "expires_at": "2026-04-16T12:30:00",
    "is_verified": false,
    "created_at": "2026-04-16T11:30:00",
    "updated_at": "2026-04-16T11:30:00"
  }
]
```

---

### 3. Get OTP by ID

**Endpoint:** `GET /api/otp-verification/{id}`

**Description:** Retrieve a specific OTP verification record by UUID

**Path Parameters:**
- `id` (UUID): The OTP verification record ID

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "mobile": "+919876543210",
  "otp": "123456",
  "expires_at": "2026-04-16T12:30:00",
  "is_verified": false,
  "created_at": "2026-04-16T11:30:00",
  "updated_at": "2026-04-16T11:30:00"
}
```

**Error Cases:**
- `404 Not Found`: OTP verification record not found

---

### 4. Get OTP by Mobile Number

**Endpoint:** `GET /api/otp-verification/by-mobile/{mobile}`

**Description:** Retrieve all OTP records for a specific mobile number

**Path Parameters:**
- `mobile` (string): The mobile phone number

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "mobile": "+919876543210",
    "otp": "123456",
    "expires_at": "2026-04-16T12:30:00",
    "is_verified": false,
    "created_at": "2026-04-16T11:30:00",
    "updated_at": "2026-04-16T11:30:00"
  }
]
```

**Error Cases:**
- `404 Not Found`: No OTP records found for this mobile number

---

### 5. Verify OTP

**Endpoint:** `POST /api/otp-verification/verify`

**Description:** Verify an OTP for a given mobile number

**Request Body:**
```json
{
  "mobile": "+919876543210",
  "otp": "123456"
}
```

**Response (200 OK - Valid OTP):**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "is_verified": true
}
```

**Response (200 OK - Invalid/Expired OTP):**
```json
{
  "success": false,
  "message": "OTP has expired",  // or "Invalid OTP"
  "is_verified": false
}
```

**Error Cases:**
- `404 Not Found`: No OTP record found for this mobile number

---

### 6. Update OTP Record

**Endpoint:** `PUT /api/otp-verification/{id}`

**Description:** Update an OTP verification record

**Path Parameters:**
- `id` (UUID): The OTP verification record ID

**Request Body (all fields optional):**
```json
{
  "otp": "654321",
  "expires_at": "2026-04-16T13:00:00",
  "is_verified": true
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "mobile": "+919876543210",
  "otp": "654321",
  "expires_at": "2026-04-16T13:00:00",
  "is_verified": true,
  "created_at": "2026-04-16T11:30:00",
  "updated_at": "2026-04-16T11:35:00"
}
```

**Error Cases:**
- `404 Not Found`: OTP verification record not found

---

### 7. Delete OTP Record

**Endpoint:** `DELETE /api/otp-verification/{id}`

**Description:** Delete an OTP verification record

**Path Parameters:**
- `id` (UUID): The OTP verification record ID

**Response (204 No Content):**
```
[Empty response body]
```

**Error Cases:**
- `404 Not Found`: OTP verification record not found

---

## Usage Examples

### Python Example

```python
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
OTP_API = f"{BASE_URL}/api/otp-verification"

# 1. Create OTP
def create_otp(mobile: str, otp: str, expires_in_minutes: int = 10):
    expires_at = (datetime.utcnow() + timedelta(minutes=expires_in_minutes)).isoformat()
    payload = {
        "mobile": mobile,
        "otp": otp,
        "expires_at": expires_at
    }
    response = requests.post(OTP_API, json=payload)
    return response.json()

# 2. Verify OTP
def verify_otp(mobile: str, otp: str):
    payload = {
        "mobile": mobile,
        "otp": otp
    }
    response = requests.post(f"{OTP_API}/verify", json=payload)
    return response.json()

# 3. Get all OTPs for mobile
def get_otp_for_mobile(mobile: str):
    response = requests.get(f"{OTP_API}/by-mobile/{mobile}")
    return response.json()

# Usage
otp_record = create_otp("+919876543210", "123456")
print(f"OTP Created: {otp_record['id']}")

# Verify OTP
result = verify_otp("+919876543210", "123456")
print(f"Verification Result: {result}")
```

### cURL Examples

```bash
# Create OTP
curl -X POST "http://localhost:8000/api/otp-verification" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "+919876543210",
    "otp": "123456",
    "expires_at": "2026-04-16T12:30:00"
  }'

# Get all OTPs
curl -X GET "http://localhost:8000/api/otp-verification"

# Get OTP by ID
curl -X GET "http://localhost:8000/api/otp-verification/550e8400-e29b-41d4-a716-446655440000"

# Get OTP by mobile
curl -X GET "http://localhost:8000/api/otp-verification/by-mobile/%2B919876543210"

# Verify OTP
curl -X POST "http://localhost:8000/api/otp-verification/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "+919876543210",
    "otp": "123456"
  }'

# Update OTP
curl -X PUT "http://localhost:8000/api/otp-verification/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "is_verified": true
  }'

# Delete OTP
curl -X DELETE "http://localhost:8000/api/otp-verification/550e8400-e29b-41d4-a716-446655440000"
```

---

## Data Models

### OTPVerification Model

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | UUID | Unique identifier | Primary Key, Auto-generated |
| `mobile` | VARCHAR(20) | Mobile phone number | Required, Indexed |
| `otp` | VARCHAR(10) | One-time password | Required |
| `expires_at` | TIMESTAMP | OTP expiration time | Required, Indexed |
| `is_verified` | BOOLEAN | Verification status | Default: False, Indexed |
| `created_at` | TIMESTAMP | Record creation time | Auto-generated |
| `updated_at` | TIMESTAMP | Last update time | Auto-updated |

---

## Request/Response Schemas

### OTPVerificationCreate
```json
{
  "mobile": "string (required)",
  "otp": "string (required)",
  "expires_at": "datetime (required)"
}
```

### OTPVerificationResponse
```json
{
  "id": "UUID",
  "mobile": "string",
  "otp": "string",
  "expires_at": "datetime",
  "is_verified": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### OTPVerificationUpdate
```json
{
  "otp": "string (optional)",
  "expires_at": "datetime (optional)",
  "is_verified": "boolean (optional)"
}
```

### OTPVerificationCheckRequest
```json
{
  "mobile": "string (required, pattern: ^\\+?1?\\d{9,15}$)",
  "otp": "string (required)"
}
```

### OTPVerificationCheckResponse
```json
{
  "success": "boolean",
  "message": "string",
  "is_verified": "boolean"
}
```

---

## Best Practices

1. **OTP Expiration**: Always set appropriate expiration times (typically 10-15 minutes)
2. **OTP Length**: Use 6-digit OTPs for better security and user experience
3. **Mobile Format**: Accept international phone numbers in E.164 format (+country_codenumber)
4. **Verification**: Always check OTP expiration before verification
5. **Error Handling**: Implement proper error handling for expired and invalid OTPs
6. **Rate Limiting**: Consider implementing rate limiting for OTP creation and verification
7. **Audit Logging**: Log all OTP creation and verification attempts for security

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Successful GET, POST (verify), PUT request |
| 201 | Created | Successful POST (create) request |
| 204 | No Content | Successful DELETE request |
| 400 | Bad Request | Invalid input or business logic error |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error in request |
| 500 | Internal Server Error | Server error |

---

## Testing

Run the provided test suite:

```bash
python test_otp_verification_api.py
```

This will test all CRUD operations and the verification functionality.

---

## Integration with User Authentication

The OTP Verification API can be integrated with user registration/login flows:

```python
# During user signup
def signup_with_otp(mobile: str):
    # Step 1: Create OTP
    otp_record = create_otp_record(mobile)
    # Step 2: Send OTP to mobile (via SMS)
    send_otp_sms(mobile, otp_record['otp'])
    return {"message": "OTP sent to mobile"}

# During OTP verification
def verify_user_otp(mobile: str, otp: str, password: str):
    # Step 1: Verify OTP
    verification = verify_otp(mobile, otp)
    if not verification['success']:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Step 2: Create user account
    user = create_user(mobile=mobile, password=password)
    return user
```

---

## Performance Optimization

- All primary fields are indexed for fast queries
- Use pagination (skip/limit) for large datasets
- Clean up expired OTPs periodically using a scheduled task
- Consider database partitioning for high-volume applications

---

## Support & Questions

For issues or questions, please refer to the main API documentation or contact the development team.
