# Doctor API Documentation

## Database Table Structure

The `doctors` table has been created with the following structure:

```sql
CREATE TABLE doctors (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  specialization VARCHAR,
  experience INT,
  consultation_fee DECIMAL,
  verification_status VARCHAR CHECK (verification_status IN ('pending','approved','rejected')),
  verified_at TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## Doctor Model

The Doctor model is defined in `app/models.py`:

```python
class Doctor(Base):
    """Doctor model with verification status"""
    __tablename__ = "doctors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    specialization = Column(String(255), nullable=False)
    experience = Column(Integer, nullable=False, default=0)
    consultation_fee = Column(Numeric(10, 2), nullable=False)
    verification_status = Column(String(50), nullable=False, default='pending')
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## Doctor API Endpoints

### 1. Create Doctor Profile
**POST** `/api/doctors`

Create a new doctor profile for an existing user.

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "specialization": "Cardiology",
  "experience": 5,
  "consultation_fee": 500.00
}
```

**Response (201 Created):**
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

**Status Codes:**
- `201 Created` - Doctor profile created successfully
- `400 Bad Request` - User not found or doctor profile already exists
- `404 Not Found` - User not found

---

### 2. Get All Doctors
**GET** `/api/doctors?skip=0&limit=10&verification_status=approved`

Retrieve all doctors with optional filtering.

**Query Parameters:**
- `skip` (int): Number of doctors to skip (default: 0)
- `limit` (int): Maximum number of doctors to return (default: 10)
- `verification_status` (string, optional): Filter by status (pending, approved, rejected)

**Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "specialization": "Cardiology",
    "experience": 5,
    "consultation_fee": 500.00,
    "verification_status": "approved",
    "verified_at": "2024-04-14T11:00:00",
    "created_at": "2024-04-14T10:30:00",
    "updated_at": "2024-04-14T11:00:00"
  }
]
```

---

### 3. Get Doctor by ID
**GET** `/api/doctors/{doctor_id}`

Retrieve a specific doctor by UUID.

**Path Parameters:**
- `doctor_id` (UUID): The doctor's unique identifier

**Response (200 OK):**
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

**Status Codes:**
- `200 OK` - Doctor found
- `404 Not Found` - Doctor not found

---

### 4. Get Doctor by User ID
**GET** `/api/doctors/user/{user_id}`

Retrieve doctor profile by associated user ID.

**Path Parameters:**
- `user_id` (UUID): The user's unique identifier

**Response (200 OK):** Same as Get Doctor by ID

**Status Codes:**
- `200 OK` - Doctor profile found
- `404 Not Found` - Doctor profile not found for this user

---

### 5. Update Doctor Profile
**PUT** `/api/doctors/{doctor_id}`

Update doctor information.

**Path Parameters:**
- `doctor_id` (UUID): The doctor's unique identifier

**Request Body (all fields optional):**
```json
{
  "specialization": "Cardiology & Oncology",
  "experience": 10,
  "consultation_fee": 750.00
}
```

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "specialization": "Cardiology & Oncology",
  "experience": 10,
  "consultation_fee": 750.00,
  "verification_status": "pending",
  "verified_at": null,
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T11:15:00"
}
```

**Status Codes:**
- `200 OK` - Doctor updated successfully
- `404 Not Found` - Doctor not found

---

### 6. Delete Doctor Profile
**DELETE** `/api/doctors/{doctor_id}`

Delete a doctor profile by ID.

**Path Parameters:**
- `doctor_id` (UUID): The doctor's unique identifier

**Response:**
- `204 No Content` - Doctor deleted successfully
- `404 Not Found` - Doctor not found

---

### 7. Update Doctor Verification Status
**POST** `/api/doctors/{doctor_id}/verify`

Update doctor verification status with complete control.

**Path Parameters:**
- `doctor_id` (UUID): The doctor's unique identifier

**Request Body:**
```json
{
  "verification_status": "approved"
}
```

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "specialization": "Cardiology",
  "experience": 5,
  "consultation_fee": 500.00,
  "verification_status": "approved",
  "verified_at": "2024-04-14T11:00:00",
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T11:00:00"
}
```

**Status Codes:**
- `200 OK` - Verification status updated
- `400 Bad Request` - Invalid status value
- `404 Not Found` - Doctor not found

---

### 8. Approve Doctor (Shorthand)
**POST** `/api/doctors/{doctor_id}/approve`

Quickly approve a doctor (sets status to 'approved' and sets verified_at timestamp).

**Path Parameters:**
- `doctor_id` (UUID): The doctor's unique identifier

**Response (200 OK):** Doctor with verification_status='approved' and verified_at set

**Status Codes:**
- `200 OK` - Doctor approved
- `404 Not Found` - Doctor not found

---

### 9. Reject Doctor (Shorthand)
**POST** `/api/doctors/{doctor_id}/reject`

Quickly reject a doctor (sets status to 'rejected' and clears verified_at timestamp).

**Path Parameters:**
- `doctor_id` (UUID): The doctor's unique identifier

**Response (200 OK):** Doctor with verification_status='rejected' and verified_at=null

**Status Codes:**
- `200 OK` - Doctor rejected
- `404 Not Found` - Doctor not found

---

## Verification Statuses

The system supports three verification statuses:

| Status | Description |
|--------|-------------|
| **pending** | Default status when profile is created. Awaiting admin verification |
| **approved** | Doctor profile is verified and approved. verified_at timestamp is set |
| **rejected** | Doctor profile was rejected. verified_at is cleared |

## Consultation Fee

- Currency: Stored as DECIMAL(10, 2)
- Must be positive (> 0)
- Typically represents cost per consultation in the platform's currency

## Experience

- Non-negative integer representing years of experience
- Default: 0
- Can be updated at any time

## Database Relationships

```
Users Table ─────────┐
                     │ (one-to-one)
                     ▼
               Doctors Table
```

Each user can have at most one doctor profile (user_id is unique in doctors table).

## Example Usage

### Using cURL

```bash
# Create a doctor profile
curl -X POST http://localhost:8000/api/doctors \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "specialization": "Cardiology",
    "experience": 5,
    "consultation_fee": 500.00
  }'

# Get all approved doctors
curl "http://localhost:8000/api/doctors?verification_status=approved"

# Get doctor by ID
curl http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000

# Get doctor by user ID
curl http://localhost:8000/api/doctors/user/550e8400-e29b-41d4-a716-446655440000

# Update doctor profile
curl -X PUT http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "specialization": "Cardiology & Internal Medicine",
    "experience": 10
  }'

# Approve doctor
curl -X POST http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000/approve

# Reject doctor
curl -X POST http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000/reject

# Delete doctor
curl -X DELETE http://localhost:8000/api/doctors/660e8400-e29b-41d4-a716-446655440000
```

### Using Python

```python
import requests
from uuid import UUID

BASE_URL = "http://localhost:8000"

# Create a doctor profile
response = requests.post(
    f"{BASE_URL}/api/doctors",
    json={
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "specialization": "Cardiology",
        "experience": 5,
        "consultation_fee": 500.00
    }
)
doctor = response.json()
print(f"Created doctor: {doctor['id']}")

# Get doctor by ID
response = requests.get(f"{BASE_URL}/api/doctors/{doctor['id']}")
print(response.json())

# Update doctor
response = requests.put(
    f"{BASE_URL}/api/doctors/{doctor['id']}",
    json={"experience": 10}
)
print(f"Updated doctor: {response.json()}")

# Approve doctor
response = requests.post(f"{BASE_URL}/api/doctors/{doctor['id']}/approve")
print(f"Approved doctor: {response.json()['verification_status']}")
```

## Files Modified/Created

1. **app/models.py** - Added Doctor model with UUID and foreign key to users
2. **app/schemas.py** - Added Doctor schemas (Create, Response, Update, Verification, Detail)
3. **app/routes.py** - Added 9 comprehensive doctor API endpoints

## Notes

- Doctor profiles are linked to users via user_id (one-to-one relationship)
- user_id must reference an existing user in the users table
- Consultation fee is stored as DECIMAL(10, 2) for precise currency handling
- verified_at timestamp is automatically set when status is 'approved'
- verified_at is cleared when status is changed to 'pending' or 'rejected'
- Tables are automatically created on application startup

