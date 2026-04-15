# Appointments API Documentation

## Overview

The Appointments API is designed for managing patient-doctor appointments in the Pramith Medical API system. It enables scheduling, tracking, and managing medical consultations.

---

## Database Schema

### Appointments Table

```sql
CREATE TABLE appointments (
  id UUID PRIMARY KEY,
  patient_id UUID REFERENCES users(id),
  doctor_id UUID REFERENCES doctors(id),
  appointment_date DATE NOT NULL,
  time_slot VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'scheduled',
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT valid_appointment_status CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no-show', 'rescheduled'))
);

CREATE INDEX idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor_id ON appointments(doctor_id);
CREATE INDEX idx_appointments_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_created_at ON appointments(created_at);
```

---

## API Endpoints

### 1. Create Appointment
**Endpoint:** `POST /api/appointments`

**Request Body:**
```json
{
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "scheduled",
  "notes": "First consultation"
}
```

**Response (201 Created):**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440222",
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "scheduled",
  "notes": "First consultation",
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

**Error Responses:**
- **404 Not Found:** Patient or doctor not found
- **400 Bad Request:** Invalid status
- **422 Unprocessable Entity:** Missing required fields

---

### 2. Get All Appointments
**Endpoint:** `GET /api/appointments`

**Query Parameters:**
- `skip` (int, optional): Number to skip (default: 0)
- `limit` (int, optional): Maximum to return (default: 10)
- `patient_id` (UUID, optional): Filter by patient
- `doctor_id` (UUID, optional): Filter by doctor
- `status` (string, optional): Filter by status
- `appointment_date` (string, optional): Filter by date (YYYY-MM-DD)

**Example Request:**
```
GET /api/appointments?status=scheduled&limit=10
```

**Response (200 OK):**
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440222",
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "appointment_date": "2024-04-20",
    "time_slot": "09:00-09:30",
    "status": "scheduled",
    "notes": "First consultation",
    "created_at": "2024-04-15T10:30:00",
    "updated_at": "2024-04-15T10:30:00"
  }
]
```

---

### 3. Get Specific Appointment
**Endpoint:** `GET /api/appointments/{appointment_id}`

**Path Parameters:**
- `appointment_id` (UUID): The appointment's ID

**Response (200 OK):**
Returns appointment with patient and doctor details
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440222",
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "scheduled",
  "notes": "First consultation",
  "patient": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "mobile": "+91-9876543210",
    "email": "john@example.com",
    "role": "patient"
  },
  "doctor": {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "specialization": "Cardiology",
    "experience": 5,
    "consultation_fee": 500.00,
    "verification_status": "approved"
  },
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

**Error Responses:**
- **404 Not Found:** Appointment not found

---

### 4. Get Appointments by Patient
**Endpoint:** `GET /api/appointments/patient/{patient_id}`

**Path Parameters:**
- `patient_id` (UUID): The patient's ID

**Query Parameters:**
- `skip` (int, optional): Number to skip (default: 0)
- `limit` (int, optional): Maximum to return (default: 10)
- `status` (string, optional): Filter by status

**Response (200 OK):**
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440222",
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "appointment_date": "2024-04-20",
    "time_slot": "09:00-09:30",
    "status": "scheduled",
    "notes": "First consultation",
    "created_at": "2024-04-15T10:30:00",
    "updated_at": "2024-04-15T10:30:00"
  }
]
```

**Error Responses:**
- **404 Not Found:** Patient not found

---

### 5. Get Appointments by Doctor
**Endpoint:** `GET /api/appointments/doctor/{doctor_id}`

**Path Parameters:**
- `doctor_id` (UUID): The doctor's ID

**Query Parameters:**
- `skip` (int, optional): Number to skip (default: 0)
- `limit` (int, optional): Maximum to return (default: 10)
- `status` (string, optional): Filter by status
- `appointment_date` (string, optional): Filter by date (YYYY-MM-DD)

**Response (200 OK):**
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440222",
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "appointment_date": "2024-04-20",
    "time_slot": "09:00-09:30",
    "status": "scheduled",
    "notes": "First consultation",
    "created_at": "2024-04-15T10:30:00",
    "updated_at": "2024-04-15T10:30:00"
  }
]
```

**Error Responses:**
- **404 Not Found:** Doctor not found

---

### 6. Update Appointment
**Endpoint:** `PUT /api/appointments/{appointment_id}`

**Path Parameters:**
- `appointment_id` (UUID): The appointment's ID

**Request Body (all fields optional):**
```json
{
  "appointment_date": "2024-04-22",
  "time_slot": "10:00-10:30",
  "status": "scheduled",
  "notes": "Rescheduled appointment"
}
```

**Response (200 OK):**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440222",
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "appointment_date": "2024-04-22",
  "time_slot": "10:00-10:30",
  "status": "scheduled",
  "notes": "Rescheduled appointment",
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T14:00:00"
}
```

**Error Responses:**
- **404 Not Found:** Appointment not found
- **400 Bad Request:** Invalid status

---

### 7. Cancel Appointment
**Endpoint:** `POST /api/appointments/{appointment_id}/cancel`

**Path Parameters:**
- `appointment_id` (UUID): The appointment's ID

**Response (200 OK):**
Sets status to 'cancelled'
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440222",
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "cancelled",
  "notes": "First consultation",
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

**Error Responses:**
- **404 Not Found:** Appointment not found

---

### 8. Complete Appointment
**Endpoint:** `POST /api/appointments/{appointment_id}/complete`

**Path Parameters:**
- `appointment_id` (UUID): The appointment's ID

**Response (200 OK):**
Sets status to 'completed'
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440222",
  "patient_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "completed",
  "notes": "First consultation",
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T15:00:00"
}
```

**Error Responses:**
- **404 Not Found:** Appointment not found

---

### 9. Delete Appointment
**Endpoint:** `DELETE /api/appointments/{appointment_id}`

**Path Parameters:**
- `appointment_id` (UUID): The appointment's ID

**Response (204 No Content)**

**Error Responses:**
- **404 Not Found:** Appointment not found

---

## Appointment Status Workflow

```
         Initial State: NEW APPOINTMENT
                   ↓
    ┌────────────────────────────────┐
    │   Status: SCHEDULED (Default)  │
    │   (Appointment is booked)      │
    └────────────┬───────────────────┘
                 │
     ┌───────────┼───────────┐
     │           │           │
  Mark as    Reschedule   Cancel
  Complete   (change date/time)
     │           │           │
     ▼           ▼           ▼
  COMPLETED  RESCHEDULED  CANCELLED

Alternative:
   After scheduled → NO-SHOW (Patient didn't arrive)
```

---

## Status Options

| Status | Description |
|--------|-------------|
| `scheduled` | Appointment is confirmed and scheduled (default) |
| `completed` | Appointment has been completed |
| `cancelled` | Appointment has been cancelled |
| `no-show` | Patient didn't show up for appointment |
| `rescheduled` | Appointment has been rescheduled |

---

## Example Usage

### Create an Appointment
```bash
curl -X POST http://localhost:8000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "appointment_date": "2024-04-20",
    "time_slot": "09:00-09:30",
    "status": "scheduled",
    "notes": "First consultation"
  }'
```

### Get Patient Appointments
```bash
curl "http://localhost:8000/api/appointments/patient/550e8400-e29b-41d4-a716-446655440000?status=scheduled"
```

### Get Doctor Appointments for a Date
```bash
curl "http://localhost:8000/api/appointments/doctor/660e8400-e29b-41d4-a716-446655440111?appointment_date=2024-04-20"
```

### Cancel Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/770e8400-e29b-41d4-a716-446655440222/cancel
```

### Mark as Completed
```bash
curl -X POST http://localhost:8000/api/appointments/770e8400-e29b-41d4-a716-446655440222/complete
```

### Reschedule Appointment
```bash
curl -X PUT http://localhost:8000/api/appointments/770e8400-e29b-41d4-a716-446655440222 \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_date": "2024-04-25",
    "time_slot": "14:00-14:30",
    "status": "rescheduled"
  }'
```

---

## Filtering Examples

### Get all scheduled appointments
```
GET /api/appointments?status=scheduled
```

### Get appointments for a specific patient
```
GET /api/appointments?patient_id=550e8400-e29b-41d4-a716-446655440000
```

### Get appointments for a specific doctor
```
GET /api/appointments?doctor_id=660e8400-e29b-41d4-a716-446655440111
```

### Get appointments for a specific date
```
GET /api/appointments?appointment_date=2024-04-20
```

### Combine filters
```
GET /api/appointments?doctor_id=660e8400-e29b-41d4-a716-446655440111&appointment_date=2024-04-20&status=scheduled
```

---

## Pagination

All list endpoints support pagination:

```
GET /api/appointments?skip=0&limit=20
```

- `skip`: Offset for pagination (default: 0)
- `limit`: Number of items per page (default: 10)

---

## Field Validation

### Request Fields
- **patient_id** (UUID, required): Must be an existing patient
- **doctor_id** (UUID, required): Must be an existing doctor
- **appointment_date** (string, required): Date format YYYY-MM-DD
- **time_slot** (string, required): Time slot format (e.g., 09:00-09:30)
- **status** (string, optional): Must be one of the valid statuses
- **notes** (string, optional): Additional notes about the appointment

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Appointment created |
| 204 | No Content - Delete successful |
| 400 | Bad Request - Validation error |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Invalid data |

---

## Error Responses

### Patient Not Found
```json
{
  "detail": "Patient not found"
}
```

### Doctor Not Found
```json
{
  "detail": "Doctor not found"
}
```

### Invalid Status
```json
{
  "detail": "Status must be one of: scheduled, completed, cancelled, no-show, rescheduled"
}
```

### Appointment Not Found
```json
{
  "detail": "Appointment not found"
}
```

---

## Integration with Other APIs

### With Doctor API
- Link appointments to verified doctors
- Validate doctor exists before creating appointment

### With User API
- Link appointments to registered patients
- Track patient history

### With Prescriptions (Future)
- Create prescriptions after appointment completion
- Track follow-up appointments

---

## API Response Time

Expected response times:
- Create: 150-200ms
- Get Single: 50-100ms
- List (10 items): 100-150ms
- Update: 100-150ms
- Delete: 80-120ms

---

## Best Practices

1. **Validate patient and doctor exist** before creating appointments
2. **Use pagination** for large date ranges
3. **Filter by doctor** to get available appointments
4. **Track status changes** for audit trails
5. **Use notes** to store additional context
6. **Soft delete** by cancelling rather than hard delete

---

## Version & Support

API Version: 1.0  
Last Updated: April 15, 2024

For issues or questions, check the Swagger UI at http://localhost:8000/docs
