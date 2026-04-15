# Doctor API - Quick Reference

## Quick Start

```bash
# Start the server
source .venv/bin/activate
uvicorn app.main:app --reload

# Access API docs at: http://localhost:8000/docs
```

## Endpoints Summary

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/doctors` | Create doctor profile | ✅ |
| GET | `/api/doctors` | Get all doctors (paginated) | ✅ |
| GET | `/api/doctors/{id}` | Get doctor by ID | ✅ |
| GET | `/api/doctors/user/{user_id}` | Get doctor by user ID | ✅ |
| PUT | `/api/doctors/{id}` | Update doctor | ✅ |
| DELETE | `/api/doctors/{id}` | Delete doctor | ✅ |
| POST | `/api/doctors/{id}/verify` | Update verification status | ✅ |
| POST | `/api/doctors/{id}/approve` | Approve doctor | ✅ |
| POST | `/api/doctors/{id}/reject` | Reject doctor | ✅ |

## Request/Response Examples

### Create Doctor

```bash
curl -X POST http://localhost:8000/api/doctors \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "specialization": "Cardiology",
    "experience": 5,
    "consultation_fee": 500.00
  }'
```

**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "specialization": "Cardiology",
  "experience": 5,
  "consultation_fee": 500.00,
  "verification_status": "pending",
  "verified_at": null,
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T10:30:00"
}
```

### Get All Doctors

```bash
curl http://localhost:8000/api/doctors?limit=10&skip=0
```

### Get Doctor by ID

```bash
curl http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000
```

### Get Doctor by User ID

```bash
curl http://localhost:8000/api/doctors/user/550e8400-e29b-41d4-a716-446655440000
```

### Filter by Verification Status

```bash
# Get all approved doctors
curl "http://localhost:8000/api/doctors?verification_status=approved"

# Get pending doctors
curl "http://localhost:8000/api/doctors?verification_status=pending"

# Get rejected doctors
curl "http://localhost:8000/api/doctors?verification_status=rejected"
```

### Update Doctor

```bash
curl -X PUT http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "specialization": "Cardiology & Internal Medicine",
    "experience": 10,
    "consultation_fee": 750.00
  }'
```

### Approve Doctor

```bash
# Quick approve
curl -X POST http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000/approve

# Or with custom status
curl -X POST http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000/verify \
  -H "Content-Type: application/json" \
  -d '{"verification_status": "approved"}'
```

### Reject Doctor

```bash
curl -X POST http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000/reject
```

### Delete Doctor

```bash
curl -X DELETE http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - New doctor profile created |
| 204 | No Content - Delete successful |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error |

## Field Validation

### DoctorCreate (POST)

```json
{
  "user_id": "UUID (required)",
  "specialization": "string (required, max 255 chars)",
  "experience": "integer (required, >= 0)",
  "consultation_fee": "float (required, > 0)"
}
```

### DoctorUpdate (PUT)

```json
{
  "specialization": "string (optional)",
  "experience": "integer (optional, >= 0)",
  "consultation_fee": "float (optional, > 0)"
}
```

### DoctorVerificationUpdate

```json
{
  "verification_status": "string (required: pending|approved|rejected)"
}
```

## Verification Statuses

| Status | Description |
|--------|-------------|
| pending | Initial status, awaiting verification |
| approved | Verified and approved, verified_at is set |
| rejected | Rejected, verified_at is null |

## Database Schema

```sql
CREATE TABLE doctors (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id) UNIQUE,
  specialization VARCHAR(255) NOT NULL,
  experience INT NOT NULL DEFAULT 0,
  consultation_fee DECIMAL(10, 2) NOT NULL,
  verification_status VARCHAR(50) NOT NULL DEFAULT 'pending',
  verified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (verification_status IN ('pending', 'approved', 'rejected')),
  CHECK (experience >= 0),
  CHECK (consultation_fee > 0)
);
```

## Python Examples

### Create Doctor

```python
import requests

response = requests.post(
    "http://localhost:8000/api/doctors",
    json={
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "specialization": "Cardiology",
        "experience": 5,
        "consultation_fee": 500.00
    }
)
doctor = response.json()
print(f"Doctor ID: {doctor['id']}")
```

### Get Doctor

```python
response = requests.get(
    "http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000"
)
doctor = response.json()
print(f"Status: {doctor['verification_status']}")
```

### Update Doctor

```python
response = requests.put(
    "http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000",
    json={
        "experience": 10,
        "consultation_fee": 750.00
    }
)
print(response.json())
```

### Approve Doctor

```python
response = requests.post(
    "http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000/approve"
)
print(f"Verified at: {response.json()['verified_at']}")
```

### Get Approved Doctors

```python
response = requests.get(
    "http://localhost:8000/api/doctors?verification_status=approved&limit=10"
)
approved_doctors = response.json()
print(f"Found {len(approved_doctors)} approved doctors")
```

## Common Workflows

### 1. Creating a Doctor Profile

```bash
# Step 1: Create user with doctor role
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. John Smith",
    "mobile": "9876543210",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "doctor"
  }'
# Returns: user_id

# Step 2: Create doctor profile
curl -X POST http://localhost:8000/api/doctors \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "{user_id}",
    "specialization": "Cardiology",
    "experience": 5,
    "consultation_fee": 500.00
  }'
```

### 2. Verifying a Doctor

```bash
# Admin approves doctor
curl -X POST http://localhost:8000/api/doctors/{doctor_id}/approve

# Get approved doctors for listing
curl http://localhost:8000/api/doctors?verification_status=approved
```

### 3. Managing Doctor Info

```bash
# Update experience when doctor adds more years
curl -X PUT http://localhost:8000/api/doctors/{doctor_id} \
  -H "Content-Type: application/json" \
  -d '{"experience": 10}'

# Adjust consultation fee
curl -X PUT http://localhost:8000/api/doctors/{doctor_id} \
  -H "Content-Type: application/json" \
  -d '{"consultation_fee": 750.00}'
```

## Error Handling

### Doctor Not Found
```json
{
  "detail": "Doctor not found"
}
```

### User Not Found
```json
{
  "detail": "User not found"
}
```

### Doctor Profile Already Exists
```json
{
  "detail": "Doctor profile already exists for this user"
}
```

### Invalid Status
```json
{
  "detail": "Status must be one of: pending, approved, rejected"
}
```

## Links

- 📚 Full Documentation: [DOCTOR_API_DOCS.md](DOCTOR_API_DOCS.md)
- 🔗 User API: [USER_API_DOCS.md](USER_API_DOCS.md)
- 🎯 User API Quick Ref: [USER_API_QUICK_REFERENCE.md](USER_API_QUICK_REFERENCE.md)
- 📋 Interactive Docs: http://localhost:8000/docs (when server is running)

