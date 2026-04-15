# User API Quick Reference

## Quick Start

```bash
# Start the server
uvicorn app.main:app --reload

# Run tests
python test_user_api.py

# Access documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

## Endpoints Summary

### User Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/users` | Create new user | ❌ |
| GET | `/api/users` | Get all users | ❌ |
| GET | `/api/users/{id}` | Get user by ID | ❌ |
| GET | `/api/users/mobile/{mobile}` | Get user by mobile | ❌ |
| PUT | `/api/users/{id}` | Update user | ❌ |
| DELETE | `/api/users/{id}` | Delete user | ❌ |
| POST | `/api/users/{id}/verify` | Verify user | ❌ |

## Request/Response Examples

### 1. Create User

```http
POST /api/users HTTP/1.1
Content-Type: application/json

{
  "name": "John Doe",
  "mobile": "9876543210",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "patient"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "mobile": "9876543210",
  "email": "john@example.com",
  "role": "patient",
  "is_verified": false,
  "created_at": "2024-04-14T10:30:00"
}
```

### 2. Get All Users

```http
GET /api/users?skip=0&limit=10&role=patient HTTP/1.1
```

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "mobile": "9876543210",
    "email": "john@example.com",
    "role": "patient",
    "is_verified": false,
    "created_at": "2024-04-14T10:30:00"
  }
]
```

### 3. Get User by ID

```http
GET /api/users/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "mobile": "9876543210",
  "email": "john@example.com",
  "role": "patient",
  "is_verified": false,
  "created_at": "2024-04-14T10:30:00"
}
```

### 4. Get User by Mobile

```http
GET /api/users/mobile/9876543210 HTTP/1.1
```

**Response (200):** Same as Get User by ID

### 5. Update User

```http
PUT /api/users/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Content-Type: application/json

{
  "name": "John Updated",
  "email": "newemail@example.com",
  "role": "doctor"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Updated",
  "mobile": "9876543210",
  "email": "newemail@example.com",
  "role": "doctor",
  "is_verified": false,
  "created_at": "2024-04-14T10:30:00"
}
```

### 6. Verify User

```http
POST /api/users/550e8400-e29b-41d4-a716-446655440000/verify HTTP/1.1
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "mobile": "9876543210",
  "email": "john@example.com",
  "role": "patient",
  "is_verified": true,
  "created_at": "2024-04-14T10:30:00"
}
```

### 7. Delete User

```http
DELETE /api/users/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
```

**Response (204 No Content)**

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - New user created |
| 204 | No Content - Delete successful |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - User doesn't exist |
| 500 | Server Error |

## Query Parameters

### GET /api/users

- `skip` (int): How many users to skip (default: 0)
- `limit` (int): How many users to return (default: 10)
- `role` (string): Filter by role (patient, doctor, admin, vendor)

Example:
```
GET /api/users?skip=10&limit=20&role=doctor
```

## Field Validation

### UserCreate (POST /api/users)

```json
{
  "name": "string (optional, max 255 chars)",
  "mobile": "string (optional, unique, max 20 chars)",
  "email": "string (optional, valid email)",
  "password": "string (required, min 6 chars)",
  "role": "string (patient, doctor, admin, vendor) - default: patient"
}
```

### UserUpdate (PUT /api/users/{id})

```json
{
  "name": "string (optional, max 255 chars)",
  "email": "string (optional, valid email)",
  "role": "string (patient, doctor, admin, vendor)"
}
```

## cURL Examples

### Create User
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "mobile": "9876543210",
    "email": "john@example.com",
    "password": "password123",
    "role": "patient"
  }' | jq
```

### Get All Users
```bash
curl http://localhost:8000/api/users | jq
```

### Get Users by Role
```bash
curl "http://localhost:8000/api/users?role=doctor" | jq
```

### Get User by ID
```bash
curl http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000 | jq
```

### Get User by Mobile
```bash
curl http://localhost:8000/api/users/mobile/9876543210 | jq
```

### Update User
```bash
curl -X PUT http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"role": "doctor"}' | jq
```

### Verify User
```bash
curl -X POST http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/verify | jq
```

### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000 -v
```

## Python Examples

### Create User
```python
import requests

response = requests.post(
    "http://localhost:8000/api/users",
    json={
        "name": "John Doe",
        "mobile": "9876543210",
        "email": "john@example.com",
        "password": "password123",
        "role": "patient"
    }
)
user = response.json()
print(user['id'])
```

### Get User
```python
import requests

response = requests.get("http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000")
user = response.json()
print(user['name'])
```

### Update User
```python
import requests

response = requests.put(
    "http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000",
    json={"role": "doctor"}
)
user = response.json()
print(user['role'])
```

## Database Schema

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR,
  mobile VARCHAR UNIQUE,
  email VARCHAR,
  password_hash TEXT,
  role VARCHAR CHECK (role IN ('patient','doctor','admin','vendor')),
  is_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP
);
```

## Key Features

✅ UUID Primary Key for scalability
✅ Password hashing with bcrypt
✅ Role-based access control
✅ Duplicate mobile/email detection
✅ Email verification support
✅ Full CRUD operations
✅ Filtering and pagination
✅ Comprehensive validation
✅ Automatic timestamp management
✅ Transaction support

## Error Handling

### Invalid Mobile (Duplicate)
```json
{
  "detail": "Mobile number already registered"
}
```

### Invalid Email (Duplicate)
```json
{
  "detail": "Email already registered"
}
```

### User Not Found
```json
{
  "detail": "User not found"
}
```

### Invalid Role
```json
{
  "detail": "role must be one of: patient, doctor, admin, vendor"
}
```

## Links

- 📚 Full Documentation: [USER_API_DOCS.md](USER_API_DOCS.md)
- 🚀 Setup Guide: [SETUP_USER_API.md](SETUP_USER_API.md)
- 🧪 Test Suite: [test_user_api.py](test_user_api.py)
- 🔗 API Docs (Live): http://localhost:8000/docs
