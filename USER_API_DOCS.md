# User API Documentation

## Database Table Structure

The `users` table has been created with the following structure:

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

## User Model

The User model is defined in `app/models.py`:

```python
class User(Base):
    """User model with UUID primary key and role-based access"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=True)
    mobile = Column(String(20), unique=True, index=True, nullable=True)
    email = Column(String(255), nullable=True)
    password_hash = Column(Text, nullable=True)
    role = Column(String(50), nullable=False, default='patient')
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## User API Endpoints

### 1. Create User
**POST** `/api/users`

Create a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "mobile": "9876543210",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "patient"
}
```

**Response (201 Created):**
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

**Status Codes:**
- `201 Created` - User created successfully
- `400 Bad Request` - Mobile or email already registered, or invalid role

---

### 2. Get All Users
**GET** `/api/users?skip=0&limit=10&role=patient`

Retrieve all users with optional filtering.

**Query Parameters:**
- `skip` (int): Number of users to skip (default: 0)
- `limit` (int): Maximum number of users to return (default: 10)
- `role` (string, optional): Filter by role (patient, doctor, admin, vendor)

**Response (200 OK):**
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
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Dr. Jane Smith",
    "mobile": "9876543211",
    "email": "jane@example.com",
    "role": "doctor",
    "is_verified": true,
    "created_at": "2024-04-14T11:00:00"
  }
]
```

---

### 3. Get User by ID
**GET** `/api/users/{user_id}`

Retrieve a specific user by UUID.

**Path Parameters:**
- `user_id` (UUID): The user's unique identifier

**Response (200 OK):**
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

**Status Codes:**
- `200 OK` - User found
- `404 Not Found` - User not found

---

### 4. Get User by Mobile
**GET** `/api/users/mobile/{mobile}`

Retrieve a user by their mobile number.

**Path Parameters:**
- `mobile` (string): The user's mobile number

**Response (200 OK):**
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

**Status Codes:**
- `200 OK` - User found
- `404 Not Found` - User not found

---

### 5. Update User
**PUT** `/api/users/{user_id}`

Update user information.

**Path Parameters:**
- `user_id` (UUID): The user's unique identifier

**Request Body (all fields optional):**
```json
{
  "name": "John Doe Updated",
  "email": "newemail@example.com",
  "role": "doctor"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe Updated",
  "mobile": "9876543210",
  "email": "newemail@example.com",
  "role": "doctor",
  "is_verified": false,
  "created_at": "2024-04-14T10:30:00"
}
```

**Status Codes:**
- `200 OK` - User updated successfully
- `404 Not Found` - User not found
- `400 Bad Request` - Email already in use

---

### 6. Delete User
**DELETE** `/api/users/{user_id}`

Delete a user account.

**Path Parameters:**
- `user_id` (UUID): The user's unique identifier

**Response:**
- `204 No Content` - User deleted successfully
- `404 Not Found` - User not found

---

### 7. Verify User
**POST** `/api/users/{user_id}/verify`

Mark a user as verified.

**Path Parameters:**
- `user_id` (UUID): The user's unique identifier

**Response (200 OK):**
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

**Status Codes:**
- `200 OK` - User verified successfully
- `404 Not Found` - User not found

---

## User Roles

The system supports four user roles:
- **patient**: Regular patient user
- **doctor**: Medical doctor with healthcare credentials
- **admin**: Administrator with full system access
- **vendor**: Vendor or service provider

## Password Security

All passwords are hashed using bcrypt before storage in the database. Passwords must be:
- Minimum 6 characters long
- Stored as SHA-256 hashes with bcrypt salt

## Database Initialization

The database tables are automatically created on application startup via the `create_all_tables()` function in `app/database.py`.

## Example Usage

### Using cURL

```bash
# Create a new user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "mobile": "9876543210",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "patient"
  }'

# Get all users
curl http://localhost:8000/api/users

# Get user by ID
curl http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000

# Get user by mobile
curl http://localhost:8000/api/users/mobile/9876543210

# Update user
curl -X PUT http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "role": "doctor"
  }'

# Verify user
curl -X POST http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/verify

# Delete user
curl -X DELETE http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a user
response = requests.post(
    f"{BASE_URL}/api/users",
    json={
        "name": "John Doe",
        "mobile": "9876543210",
        "email": "john@example.com",
        "password": "securepassword123",
        "role": "patient"
    }
)
user = response.json()
print(f"Created user: {user['id']}")

# Get user by ID
response = requests.get(f"{BASE_URL}/api/users/{user['id']}")
print(response.json())

# Update user
response = requests.put(
    f"{BASE_URL}/api/users/{user['id']}",
    json={"role": "doctor"}
)
print(f"Updated user: {response.json()}")

# Delete user
response = requests.delete(f"{BASE_URL}/api/users/{user['id']}")
print(f"Delete response: {response.status_code}")
```

## Files Modified/Created

1. **app/models.py** - Updated User model with UUID and role-based fields
2. **app/schemas.py** - Added/updated User schemas for API validation
3. **app/routes.py** - Added comprehensive user API endpoints
4. **app/database.py** - Existing database setup (no changes needed)
5. **USER_API_DOCS.md** - This documentation file

## Notes

- The database tables are automatically created on application startup
- UUID is used as the primary key for better scalability
- Mobile numbers are unique per user
- Email is optional but should be unique if provided
- The role field has a CHECK constraint to ensure valid values
- All timestamps are in UTC

