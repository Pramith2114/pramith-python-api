# OTP Verification API - Quick Reference

## Quick Start

### Base URL
```
http://localhost:8000/api/otp-verification
```

## Endpoints Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/` | Create new OTP |
| GET | `/` | List all OTPs (with filters) |
| GET | `/{id}` | Get OTP by ID |
| GET | `/by-mobile/{mobile}` | Get OTPs by mobile number |
| POST | `/verify` | Verify OTP |
| PUT | `/{id}` | Update OTP |
| DELETE | `/{id}` | Delete OTP |

## Common Operations

### 1. Send OTP to User

```bash
curl -X POST "http://localhost:8000/api/otp-verification" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "+919876543210",
    "otp": "123456",
    "expires_at": "2026-04-16T12:30:00"
  }'
```

### 2. Verify User OTP

```bash
curl -X POST "http://localhost:8000/api/otp-verification/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile": "+919876543210",
    "otp": "123456"
  }'
```

### 3. Check OTP Status

```bash
curl -X GET "http://localhost:8000/api/otp-verification/by-mobile/%2B919876543210"
```

### 4. List Unverified OTPs

```bash
curl -X GET "http://localhost:8000/api/otp-verification?is_verified=false"
```

## Request/Response Templates

### Create OTP
**Request:**
```json
{
  "mobile": "+919876543210",
  "otp": "123456",
  "expires_at": "2026-04-16T12:30:00"
}
```

**Success Response (201):**
```json
{
  "id": "UUID",
  "mobile": "+919876543210",
  "otp": "123456",
  "expires_at": "2026-04-16T12:30:00",
  "is_verified": false,
  "created_at": "2026-04-16T11:30:00",
  "updated_at": "2026-04-16T11:30:00"
}
```

### Verify OTP
**Request:**
```json
{
  "mobile": "+919876543210",
  "otp": "123456"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "OTP verified successfully",
  "is_verified": true
}
```

**Response (Invalid OTP):**
```json
{
  "success": false,
  "message": "Invalid OTP",
  "is_verified": false
}
```

## Database Table

```sql
CREATE TABLE otp_verifications (
  id UUID PRIMARY KEY,
  mobile VARCHAR(20) NOT NULL,
  otp VARCHAR(10) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  is_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Python Integration

```python
import requests
from datetime import datetime, timedelta

OTP_API = "http://localhost:8000/api/otp-verification"

# Create OTP
def send_otp(mobile):
    expires_at = (datetime.utcnow() + timedelta(minutes=10)).isoformat()
    response = requests.post(OTP_API, json={
        "mobile": mobile,
        "otp": "123456",
        "expires_at": expires_at
    })
    return response.json()

# Verify OTP
def check_otp(mobile, otp):
    response = requests.post(f"{OTP_API}/verify", json={
        "mobile": mobile,
        "otp": otp
    })
    return response.json()

# Get OTP records
def get_otps(mobile):
    response = requests.get(f"{OTP_API}/by-mobile/{mobile}")
    return response.json()
```

## Query Parameters

### List OTPs - Filters
```
?skip=0              # Skip first N records
&limit=10            # Return max N records
&mobile=+919876...   # Filter by mobile
&is_verified=false   # Filter by status
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, POST verify, PUT) |
| 201 | Created (POST create) |
| 204 | Deleted (DELETE) |
| 400 | Bad Request |
| 404 | Not Found |
| 422 | Validation Error |

## Field Validation

| Field | Validation |
|-------|-----------|
| mobile | Valid international format |
| otp | Required string |
| expires_at | ISO 8601 datetime |
| is_verified | Boolean |

## Tips

1. **OTP Format**: Use variable-length OTPs (6-10 digits)
2. **Expiration**: Set to 10-15 minutes for security
3. **Mobile Format**: Use E.164 (+country_codenumber)
4. **Error Handling**: Always check response success field
5. **Cleanup**: Implement scheduled task to delete expired OTPs

## Common Errors

| Error | Solution |
|-------|----------|
| 404 Not Found | OTP doesn't exist or has expired |
| 400 Bad Request | Active OTP already exists |
| 422 Validation Error | Invalid input format |
| Invalid OTP | Check expiration and OTP value |

## Testing

```bash
python test_otp_verification_api.py
```

## Next Steps

1. Integrate with SMS service to send actual OTPs
2. Add rate limiting to prevent abuse
3. Implement cleanup of expired OTPs
4. Add audit logging for security compliance
