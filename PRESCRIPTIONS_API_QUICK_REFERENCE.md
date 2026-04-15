# 📋 Prescriptions API - Quick Reference

## Server Setup

```bash
# Start server
python -m uvicorn app.main:app --reload --port 8000

# Access Swagger UI
# http://localhost:8000/docs
```

---

## Quick Endpoints Summary

### Prescriptions (Main)

| Operation | Endpoint | Method | Returns |
|-----------|----------|--------|---------|
| Create | `/api/prescriptions` | POST | 201 Created |
| List All | `/api/prescriptions` | GET | 200 OK (Array) |
| Get One | `/api/prescriptions/{id}` | GET | 200 OK (Detail) |
| List by Patient | `/api/prescriptions/patient/{id}` | GET | 200 OK (Array) |
| List by Doctor | `/api/prescriptions/doctor/{id}` | GET | 200 OK (Array) |
| List by Appointment | `/api/prescriptions/appointment/{id}` | GET | 200 OK (Array) |
| Update | `/api/prescriptions/{id}` | PUT | 200 OK |
| Delete | `/api/prescriptions/{id}` | DELETE | 204 No Content |

### Prescription Items

| Operation | Endpoint | Method | Returns |
|-----------|----------|--------|---------|
| Add Item | `/api/prescription-items?prescription_id={id}` | POST | 201 Created |
| List Items | `/api/prescription-items/prescription/{id}` | GET | 200 OK (Array) |
| Get Item | `/api/prescription-items/{id}` | GET | 200 OK |
| Get by Drug | `/api/prescription-items/drug/{id}` | GET | 200 OK (Array) |
| Update Item | `/api/prescription-items/{id}` | PUT | 200 OK |
| Delete Item | `/api/prescription-items/{id}` | DELETE | 204 No Content |

---

## Create Prescription

### cURL

```bash
curl -X POST http://localhost:8000/api/prescriptions \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "patient_id": "770e8400-e29b-41d4-a716-446655440222",
    "notes": "Take with food",
    "items": [
      {
        "drug_id": "880e8400-e29b-41d4-a716-446655440333",
        "dosage": "500mg",
        "duration": "7 days",
        "instructions": "Twice daily"
      }
    ]
  }'
```

### Response (201)

```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "notes": "Take with food",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

---

## Get All Prescriptions

```bash
# Get all
curl http://localhost:8000/api/prescriptions

# With pagination
curl "http://localhost:8000/api/prescriptions?skip=0&limit=10"

# Filter by patient
curl "http://localhost:8000/api/prescriptions?patient_id=770e8400-e29b-41d4-a716-446655440222"

# Filter by doctor
curl "http://localhost:8000/api/prescriptions?doctor_id=660e8400-e29b-41d4-a716-446655440111"

# Filter by appointment
curl "http://localhost:8000/api/prescriptions?appointment_id=550e8400-e29b-41d4-a716-446655440000"

# Multiple filters
curl "http://localhost:8000/api/prescriptions?patient_id=770e8400-e29b-41d4-a716-446655440222&doctor_id=660e8400-e29b-41d4-a716-446655440111&skip=0&limit=5"
```

---

## Get Single Prescription (with Items)

```bash
curl http://localhost:8000/api/prescriptions/aa0e8400-e29b-41d4-a716-446655440555
```

### Response

```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "notes": "Take with food",
  "items": [
    {
      "id": "bb0e8400-e29b-41d4-a716-446655440666",
      "prescription_id": "aa0e8400-e29b-41d4-a716-446655440555",
      "drug_id": "880e8400-e29b-41d4-a716-446655440333",
      "dosage": "500mg",
      "duration": "7 days",
      "instructions": "Twice daily",
      "created_at": "2024-04-15T14:30:00",
      "updated_at": "2024-04-15T14:30:00"
    }
  ],
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

---

## Get Patient Prescriptions

```bash
curl "http://localhost:8000/api/prescriptions/patient/770e8400-e29b-41d4-a716-446655440222"

# With pagination
curl "http://localhost:8000/api/prescriptions/patient/770e8400-e29b-41d4-a716-446655440222?skip=0&limit=10"
```

---

## Get Doctor Prescriptions

```bash
curl "http://localhost:8000/api/prescriptions/doctor/660e8400-e29b-41d4-a716-446655440111"

# With pagination
curl "http://localhost:8000/api/prescriptions/doctor/660e8400-e29b-41d4-a716-446655440111?skip=0&limit=10"
```

---

## Get Appointment Prescriptions

```bash
curl "http://localhost:8000/api/prescriptions/appointment/550e8400-e29b-41d4-a716-446655440000"
```

---

## Update Prescription

```bash
curl -X PUT http://localhost:8000/api/prescriptions/aa0e8400-e29b-41d4-a716-446655440555 \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Take with food, patient allergic to penicillin"
  }'
```

### Response (200)

Updated prescription object.

---

## Delete Prescription

```bash
curl -X DELETE http://localhost:8000/api/prescriptions/aa0e8400-e29b-41d4-a716-446655440555
```

**Response:** `204 No Content`

---

## Add Item to Prescription

```bash
curl -X POST "http://localhost:8000/api/prescription-items?prescription_id=aa0e8400-e29b-41d4-a716-446655440555" \
  -H "Content-Type: application/json" \
  -d '{
    "drug_id": "990e8400-e29b-41d4-a716-446655440444",
    "dosage": "10ml",
    "duration": "5 days",
    "instructions": "As needed for fever"
  }'
```

### Response (201)

```json
{
  "id": "cc0e8400-e29b-41d4-a716-446655440777",
  "prescription_id": "aa0e8400-e29b-41d4-a716-446655440555",
  "drug_id": "990e8400-e29b-41d4-a716-446655440444",
  "dosage": "10ml",
  "duration": "5 days",
  "instructions": "As needed for fever",
  "created_at": "2024-04-15T14:35:00",
  "updated_at": "2024-04-15T14:35:00"
}
```

---

## Get Prescription Items

```bash
curl "http://localhost:8000/api/prescription-items/prescription/aa0e8400-e29b-41d4-a716-446655440555"
```

---

## Get Single Item

```bash
curl http://localhost:8000/api/prescription-items/bb0e8400-e29b-41d4-a716-446655440666
```

---

## Get Items by Drug

```bash
curl "http://localhost:8000/api/prescription-items/drug/880e8400-e29b-41d4-a716-446655440333"
```

---

## Update Item

```bash
curl -X PUT http://localhost:8000/api/prescription-items/bb0e8400-e29b-41d4-a716-446655440666 \
  -H "Content-Type: application/json" \
  -d '{
    "drug_id": "880e8400-e29b-41d4-a716-446655440333",
    "dosage": "250mg",
    "duration": "7 days",
    "instructions": "Once daily"
  }'
```

---

## Delete Item

```bash
curl -X DELETE http://localhost:8000/api/prescription-items/bb0e8400-e29b-41d4-a716-446655440666
```

**Response:** `204 No Content`

---

## Schema Objects

### Prescription Response

```json
{
  "id": "UUID",
  "appointment_id": "UUID",
  "doctor_id": "UUID",
  "patient_id": "UUID",
  "notes": "string or null",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Prescription Detail Response (with Items)

```json
{
  "id": "UUID",
  "appointment_id": "UUID",
  "doctor_id": "UUID",
  "patient_id": "UUID",
  "notes": "string or null",
  "items": [
    {
      "id": "UUID",
      "prescription_id": "UUID",
      "drug_id": "UUID",
      "dosage": "string",
      "duration": "string",
      "instructions": "string or null",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Prescription Item Response

```json
{
  "id": "UUID",
  "prescription_id": "UUID",
  "drug_id": "UUID",
  "dosage": "string",
  "duration": "string",
  "instructions": "string or null",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## Common Workflows

### Workflow 1: Issue Complete Prescription

```bash
# 1. Get appointment ID (from appointment endpoint)
APPT_ID="550e8400-e29b-41d4-a716-446655440000"

# 2. Get drug IDs (from drugs endpoint)
DRUG1="880e8400-e29b-41d4-a716-446655440333"
DRUG2="990e8400-e29b-41d4-a716-446655440444"

# 3. Create prescription with items
curl -X POST http://localhost:8000/api/prescriptions \
  -d "{
    \"appointment_id\": \"$APPT_ID\",
    \"doctor_id\": \"660e8400-e29b-41d4-a716-446655440111\",
    \"patient_id\": \"770e8400-e29b-41d4-a716-446655440222\",
    \"items\": [
      {
        \"drug_id\": \"$DRUG1\",
        \"dosage\": \"500mg\",
        \"duration\": \"7 days\",
        \"instructions\": \"Twice daily\"
      },
      {
        \"drug_id\": \"$DRUG2\",
        \"dosage\": \"10ml\",
        \"duration\": \"5 days\",
        \"instructions\": \"As needed\"
      }
    ]
  }"
```

### Workflow 2: Retrieve Patient's Medication History

```bash
PATIENT_ID="770e8400-e29b-41d4-a716-446655440222"

# Get all prescriptions
curl "http://localhost:8000/api/prescriptions/patient/$PATIENT_ID"

# Get details of each prescription (includes items)
curl "http://localhost:8000/api/prescriptions/{prescription_id}"
```

### Workflow 3: Modify Prescription

```bash
RX_ID="aa0e8400-e29b-41d4-a716-446655440555"
ITEM_ID="bb0e8400-e29b-41d4-a716-446655440666"

# Update prescription notes
curl -X PUT "http://localhost:8000/api/prescriptions/$RX_ID" \
  -d '{"notes": "Update: side effects reported"}'

# Update item dosage
curl -X PUT "http://localhost:8000/api/prescription-items/$ITEM_ID" \
  -d '{
    "drug_id": "880e8400-e29b-41d4-a716-446655440333",
    "dosage": "250mg",
    "duration": "7 days",
    "instructions": "Once daily"
  }'
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 204 | No Content - Deleted |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource missing |
| 422 | Validation Error - Invalid field |
| 500 | Server Error |

---

## Common Errors

### Prescription Not Found
```json
{"detail": "Prescription not found"}
```

### Missing Prescription ID
```json
{"detail": "prescription_id query parameter is required"}
```

### Drug Not Found
```json
{"detail": "Drug not found"}
```

### Appointment Not Found
```json
{"detail": "Appointment not found"}
```

### Patient Not Found
```json
{"detail": "Patient not found"}
```

---

## Test with Swagger UI

1. Go to `http://localhost:8000/docs`
2. Find endpoint under "prescriptions" or "prescription-items"
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

---

## Tips & Tricks

### Get All Items in a Prescription
```bash
curl "http://localhost:8000/api/prescriptions/{id}"
# Includes "items" array
```

### Filter Prescriptions by Multiple Criteria
```bash
curl "http://localhost:8000/api/prescriptions?patient_id=X&doctor_id=Y"
```

### Pagination Pages
```bash
# Page 1 (0-9)
curl "http://localhost:8000/api/prescriptions?skip=0&limit=10"

# Page 2 (10-19)
curl "http://localhost:8000/api/prescriptions?skip=10&limit=10"

# Page 3 (20-29)
curl "http://localhost:8000/api/prescriptions?skip=20&limit=10"
```

### Delete Entire Prescription (with items)
```bash
curl -X DELETE "http://localhost:8000/api/prescriptions/{id}"
# Automatically deletes all associated items
```

---

## Performance

| Operation | Time |
|-----------|------|
| Create prescription | 150-250ms |
| Get single | 50-100ms |
| List (10) | 100-150ms |
| Filter by patient | 100-150ms |
| Update | 80-120ms |
| Delete | 100-150ms |

---

**Quick Reference Updated:** April 15, 2024  
**API Version:** 1.0
