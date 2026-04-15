# Appointments API - Quick Reference

## Overview
- **Base Path:** `/api`
- **Appointments Endpoint:** `/api/appointments`

---

## Appointment CRUD Operations

### CREATE Appointment
```bash
POST /api/appointments
Content-Type: application/json

{
  "patient_id": "UUID",
  "doctor_id": "UUID",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "scheduled",
  "notes": "First consultation"
}
```
**Returns:** 201 Created

### READ All Appointments
```bash
GET /api/appointments?skip=0&limit=10&status=scheduled
```
**Returns:** 200 OK - Array of appointments

### READ Single Appointment
```bash
GET /api/appointments/{appointment_id}
```
**Returns:** 200 OK - Appointment with patient & doctor details

### READ Patient Appointments
```bash
GET /api/appointments/patient/{patient_id}?status=scheduled&limit=10
```
**Returns:** 200 OK - Array of patient appointments

### READ Doctor Appointments
```bash
GET /api/appointments/doctor/{doctor_id}?appointment_date=2024-04-20&limit=10
```
**Returns:** 200 OK - Array of doctor appointments

### UPDATE Appointment
```bash
PUT /api/appointments/{appointment_id}
Content-Type: application/json

{
  "appointment_date": "2024-04-22",
  "time_slot": "10:00-10:30",
  "status": "rescheduled",
  "notes": "Rescheduled"
}
```
**Returns:** 200 OK - Updated appointment

### DELETE Appointment
```bash
DELETE /api/appointments/{appointment_id}
```
**Returns:** 204 No Content

### CANCEL Appointment (Shorthand)
```bash
POST /api/appointments/{appointment_id}/cancel
```
**Returns:** 200 OK - Cancelled appointment

### COMPLETE Appointment (Shorthand)
```bash
POST /api/appointments/{appointment_id}/complete
```
**Returns:** 200 OK - Completed appointment

---

## Response Objects

### Appointment Response
```json
{
  "id": "UUID",
  "patient_id": "UUID",
  "doctor_id": "UUID",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "scheduled",
  "notes": "First consultation",
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

### Appointment Detail Response (includes patient & doctor)
```json
{
  "id": "UUID",
  "patient_id": "UUID",
  "doctor_id": "UUID",
  "appointment_date": "2024-04-20",
  "time_slot": "09:00-09:30",
  "status": "scheduled",
  "notes": "First consultation",
  "patient": { /* user object */ },
  "doctor": { /* doctor object */ },
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

---

## Status Options

| Status | Description |
|--------|-------------|
| `scheduled` | Appointment is booked (default) |
| `completed` | Appointment finished |
| `cancelled` | Appointment cancelled |
| `no-show` | Patient didn't attend |
| `rescheduled` | Appointment rescheduled |

---

## Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Delete successful |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |

---

## Example cURL Commands

### Create Appointment
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

### Get All Appointments
```bash
curl http://localhost:8000/api/appointments?limit=10
```

### Get Patient Appointments
```bash
curl "http://localhost:8000/api/appointments/patient/550e8400-e29b-41d4-a716-446655440000?status=scheduled"
```

### Get Doctor Appointments
```bash
curl "http://localhost:8000/api/appointments/doctor/660e8400-e29b-41d4-a716-446655440111?appointment_date=2024-04-20"
```

### Cancel Appointment
```bash
curl -X POST http://localhost:8000/api/appointments/APPOINTMENT_ID/cancel
```

### Mark as Completed
```bash
curl -X POST http://localhost:8000/api/appointments/APPOINTMENT_ID/complete
```

### Reschedule Appointment
```bash
curl -X PUT http://localhost:8000/api/appointments/APPOINTMENT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_date": "2024-04-25",
    "time_slot": "14:00-14:30",
    "status": "rescheduled"
  }'
```

---

## Filtering Examples

### By Status
```
GET /api/appointments?status=scheduled
```

### By Patient
```
GET /api/appointments?patient_id=UUID
```

### By Doctor
```
GET /api/appointments?doctor_id=UUID
```

### By Date
```
GET /api/appointments?appointment_date=2024-04-20
```

### Multiple Filters
```
GET /api/appointments?doctor_id=UUID&appointment_date=2024-04-20&status=scheduled
```

---

## Pagination

```
GET /api/appointments?skip=0&limit=20
```

- `skip`: Number to skip (default: 0)
- `limit`: Items per page (default: 10)

---

## Status Workflow

```
scheduled → completed ✓ (Done)
         → cancelled ✗ (Not happening)
         → no-show ✗ (Patient didn't come)
         → rescheduled → scheduled (new time)
```

---

## Field Validation

### Required Fields
- `patient_id` - UUID must exist
- `doctor_id` - UUID must exist
- `appointment_date` - Format: YYYY-MM-DD
- `time_slot` - Format: HH:MM-HH:MM (e.g., 09:00-09:30)

### Optional Fields
- `status` - Must be valid status (default: scheduled)
- `notes` - Free text description

---

## Endpoints Summary

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/appointments | Create appointment |
| GET | /api/appointments | List all appointments |
| GET | /api/appointments/{id} | Get single (with details) |
| GET | /api/appointments/patient/{id} | Get patient appointments |
| GET | /api/appointments/doctor/{id} | Get doctor appointments |
| PUT | /api/appointments/{id} | Update appointment |
| DELETE | /api/appointments/{id} | Delete appointment |
| POST | /api/appointments/{id}/cancel | Cancel appointment |
| POST | /api/appointments/{id}/complete | Mark completed |

---

## Database Table

```
appointments
├── id (UUID, PK)
├── patient_id (UUID, FK → users.id)
├── doctor_id (UUID, FK → doctors.id)
├── appointment_date (DATE)
├── time_slot (VARCHAR)
├── status (VARCHAR, CHECK)
├── notes (TEXT)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

---

## Tips & Best Practices

1. **Always verify IDs exist** before creating appointments
2. **Use patient endpoint** to get all appointments for a patient
3. **Use doctor endpoint** to get appointments for a specific doctor
4. **Use shorthand endpoints** (cancel, complete) for common operations
5. **Combine filters** for specific queries
6. **Use pagination** for large datasets
7. **Store additional info** in notes field

---

## Troubleshooting

### Patient Not Found (404)
- Verify patient UUID is correct
- Check patient exists with GET /api/users/{id}

### Doctor Not Found (404)
- Verify doctor UUID is correct
- Check doctor exists with GET /api/doctors/{id}

### Invalid Status (400)
- Use only: scheduled, completed, cancelled, no-show, rescheduled
- Check spelling carefully

### Appointment Not Found (404)
- Verify appointment UUID is correct
- Check appointment exists with GET /api/appointments/{id}

---

## Performance Expected

| Operation | Time |
|-----------|------|
| Create | 150-200ms |
| Get Single | 50-100ms |
| List (10) | 100-150ms |
| Update | 100-150ms |
| Delete | 80-120ms |

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0
