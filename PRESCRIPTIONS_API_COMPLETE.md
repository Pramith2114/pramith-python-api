# 📋 Prescriptions API - Complete Specification

## Overview

The **Prescriptions API** is a complete REST API for managing pharmaceutical prescriptions issued during patient-doctor appointments. It supports prescription creation, item management, and comprehensive filtering for patient and doctor workflows.

**Features:**
- Create prescriptions linked to appointments
- Add multiple drugs to a single prescription
- Track dosage and duration per drug
- Filter prescriptions by patient, doctor, or appointment
- Full CRUD operations for both prescriptions and items
- Automatic timestamp tracking

---

## Database Tables

### Prescriptions Table

```sql
CREATE TABLE prescriptions (
  id UUID PRIMARY KEY,
  appointment_id UUID NOT NULL REFERENCES appointments(id),
  doctor_id UUID NOT NULL REFERENCES doctors(id),
  patient_id UUID NOT NULL REFERENCES users(id),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (appointment_id),
  INDEX (doctor_id),
  INDEX (patient_id),
  INDEX (created_at)
);
```

**Fields:**
- `id`: Unique prescription identifier (UUID)
- `appointment_id`: Reference to the appointment during which prescription was issued
- `doctor_id`: Reference to the doctor who issued the prescription
- `patient_id`: Reference to the patient receiving the prescription
- `notes`: Additional notes about the prescription
- `created_at`: Timestamp when prescription was created
- `updated_at`: Timestamp when prescription was last modified

### Prescription Items Table

```sql
CREATE TABLE prescription_items (
  id UUID PRIMARY KEY,
  prescription_id UUID NOT NULL REFERENCES prescriptions(id),
  drug_id UUID NOT NULL REFERENCES drugs(id),
  dosage VARCHAR(100) NOT NULL,
  duration VARCHAR(100) NOT NULL,
  instructions TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (prescription_id),
  INDEX (drug_id),
  INDEX (created_at)
);
```

**Fields:**
- `id`: Unique prescription item identifier (UUID)
- `prescription_id`: Reference to the parent prescription
- `drug_id`: Reference to the drug being prescribed
- `dosage`: Dosage amount (e.g., "500mg", "10ml")
- `duration`: Duration of treatment (e.g., "7 days", "2 weeks")
- `instructions`: Usage instructions (e.g., "Take twice daily after meals")
- `created_at`: Timestamp when item was created
- `updated_at`: Timestamp when item was last modified

---

## API Endpoints

### Prescriptions Endpoints

#### 1. Create Prescription
**Endpoint:** `POST /api/prescriptions`

**Status Code:** `201 Created`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "notes": "Patient to take antibiotics with food",
  "items": [
    {
      "drug_id": "880e8400-e29b-41d4-a716-446655440333",
      "dosage": "500mg",
      "duration": "7 days",
      "instructions": "Take twice daily after meals"
    },
    {
      "drug_id": "990e8400-e29b-41d4-a716-446655440444",
      "dosage": "10ml",
      "duration": "5 days",
      "instructions": "Take as needed"
    }
  ]
}
```

**Success Response:**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "notes": "Patient to take antibiotics with food",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

**Error Responses:**
- `404 Not Found` - Appointment, doctor, or patient not found
- `400 Bad Request` - Invalid data format
- `422 Unprocessable Entity` - Validation error

---

#### 2. Get All Prescriptions
**Endpoint:** `GET /api/prescriptions`

**Query Parameters:**
- `skip` (integer, default: 0) - Number of prescriptions to skip
- `limit` (integer, default: 10) - Maximum number to return
- `patient_id` (UUID, optional) - Filter by patient
- `doctor_id` (UUID, optional) - Filter by doctor
- `appointment_id` (UUID, optional) - Filter by appointment

**Example Request:**
```bash
GET /api/prescriptions?patient_id=770e8400-e29b-41d4-a716-446655440222&skip=0&limit=10
```

**Success Response (200 OK):**
```json
[
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440555",
    "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "patient_id": "770e8400-e29b-41d4-a716-446655440222",
    "notes": "Patient to take antibiotics with food",
    "created_at": "2024-04-15T14:30:00",
    "updated_at": "2024-04-15T14:30:00"
  }
]
```

---

#### 3. Get Single Prescription (with Items)
**Endpoint:** `GET /api/prescriptions/{prescription_id}`

**Path Parameters:**
- `prescription_id` (UUID) - Prescription identifier

**Success Response (200 OK):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
  "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "notes": "Patient to take antibiotics with food",
  "items": [
    {
      "id": "bb0e8400-e29b-41d4-a716-446655440666",
      "prescription_id": "aa0e8400-e29b-41d4-a716-446655440555",
      "drug_id": "880e8400-e29b-41d4-a716-446655440333",
      "dosage": "500mg",
      "duration": "7 days",
      "instructions": "Take twice daily after meals",
      "created_at": "2024-04-15T14:30:00",
      "updated_at": "2024-04-15T14:30:00"
    },
    {
      "id": "cc0e8400-e29b-41d4-a716-446655440777",
      "prescription_id": "aa0e8400-e29b-41d4-a716-446655440555",
      "drug_id": "990e8400-e29b-41d4-a716-446655440444",
      "dosage": "10ml",
      "duration": "5 days",
      "instructions": "Take as needed",
      "created_at": "2024-04-15T14:30:00",
      "updated_at": "2024-04-15T14:30:00"
    }
  ],
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Prescription not found"
}
```

---

#### 4. Get Patient Prescriptions
**Endpoint:** `GET /api/prescriptions/patient/{patient_id}`

**Path Parameters:**
- `patient_id` (UUID) - Patient identifier

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)

**Success Response (200 OK):**
```json
[
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440555",
    "appointment_id": "550e8400-e29b-41d4-a716-446655440000",
    "doctor_id": "660e8400-e29b-41d4-a716-446655440111",
    "patient_id": "770e8400-e29b-41d4-a716-446655440222",
    "notes": "Patient to take antibiotics with food",
    "created_at": "2024-04-15T14:30:00",
    "updated_at": "2024-04-15T14:30:00"
  }
]
```

---

#### 5. Get Doctor Prescriptions
**Endpoint:** `GET /api/prescriptions/doctor/{doctor_id}`

**Path Parameters:**
- `doctor_id` (UUID) - Doctor identifier

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)

**Success Response (200 OK):**
Returns list of prescriptions issued by the doctor.

---

#### 6. Get Appointment Prescriptions
**Endpoint:** `GET /api/prescriptions/appointment/{appointment_id}`

**Path Parameters:**
- `appointment_id` (UUID) - Appointment identifier

**Success Response (200 OK):**
Returns list of prescriptions created for the appointment.

---

#### 7. Update Prescription
**Endpoint:** `PUT /api/prescriptions/{prescription_id}`

**Path Parameters:**
- `prescription_id` (UUID) - Prescription identifier

**Request Body:**
```json
{
  "notes": "Updated notes - patient had allergic reaction"
}
```

**Success Response (200 OK):**
Returns updated prescription object.

**Note:** Only notes can be updated. To change items, use the Prescription Items endpoints.

---

#### 8. Delete Prescription
**Endpoint:** `DELETE /api/prescriptions/{prescription_id}`

**Path Parameters:**
- `prescription_id` (UUID) - Prescription identifier

**Success Response:** `204 No Content`

**Behavior:** Deletes the prescription and all associated prescription items.

---

### Prescription Items Endpoints

#### 1. Create Prescription Item
**Endpoint:** `POST /api/prescription-items?prescription_id={prescription_id}`

**Query Parameters:**
- `prescription_id` (UUID, required) - Prescription to add item to

**Request Body:**
```json
{
  "drug_id": "880e8400-e29b-41d4-a716-446655440333",
  "dosage": "250mg",
  "duration": "10 days",
  "instructions": "Take once daily before bedtime"
}
```

**Success Response (201 Created):**
```json
{
  "id": "dd0e8400-e29b-41d4-a716-446655440888",
  "prescription_id": "aa0e8400-e29b-41d4-a716-446655440555",
  "drug_id": "880e8400-e29b-41d4-a716-446655440333",
  "dosage": "250mg",
  "duration": "10 days",
  "instructions": "Take once daily before bedtime",
  "created_at": "2024-04-15T14:35:00",
  "updated_at": "2024-04-15T14:35:00"
}
```

---

#### 2. Get Prescription Items
**Endpoint:** `GET /api/prescription-items/prescription/{prescription_id}`

**Path Parameters:**
- `prescription_id` (UUID) - Prescription identifier

**Success Response (200 OK):**
```json
[
  {
    "id": "bb0e8400-e29b-41d4-a716-446655440666",
    "prescription_id": "aa0e8400-e29b-41d4-a716-446655440555",
    "drug_id": "880e8400-e29b-41d4-a716-446655440333",
    "dosage": "500mg",
    "duration": "7 days",
    "instructions": "Take twice daily after meals",
    "created_at": "2024-04-15T14:30:00",
    "updated_at": "2024-04-15T14:30:00"
  }
]
```

---

#### 3. Get Single Item
**Endpoint:** `GET /api/prescription-items/{item_id}`

**Path Parameters:**
- `item_id` (UUID) - Prescription item identifier

**Success Response (200 OK):**
Returns single prescription item object.

---

#### 4. Get Items by Drug
**Endpoint:** `GET /api/prescription-items/drug/{drug_id}`

**Path Parameters:**
- `drug_id` (UUID) - Drug identifier

**Success Response (200 OK):**
Returns list of all prescription items for the specified drug.

---

#### 5. Update Prescription Item
**Endpoint:** `PUT /api/prescription-items/{item_id}`

**Path Parameters:**
- `item_id` (UUID) - Prescription item identifier

**Request Body:**
```json
{
  "drug_id": "880e8400-e29b-41d4-a716-446655440333",
  "dosage": "250mg",
  "duration": "10 days",
  "instructions": "Take once daily after meals"
}
```

**Success Response (200 OK):**
Returns updated prescription item object.

---

#### 6. Delete Prescription Item
**Endpoint:** `DELETE /api/prescription-items/{item_id}`

**Path Parameters:**
- `item_id` (UUID) - Prescription item identifier

**Success Response:** `204 No Content`

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET, PUT operations |
| 201 | Created | Successful POST operation |
| 204 | No Content | Successful DELETE operation |
| 400 | Bad Request | Invalid appointment/doctor/patient ID |
| 404 | Not Found | Prescription or drug not found |
| 422 | Unprocessable Entity | Invalid field format or value |
| 500 | Internal Server Error | Database or server error |

### Common Errors

**Prescription Not Found:**
```json
{
  "detail": "Prescription not found"
}
```

**Appointment Not Found:**
```json
{
  "detail": "Appointment not found"
}
```

**Drug Not Found:**
```json
{
  "detail": "Drug not found"
}
```

**Missing Prescription ID:**
```json
{
  "detail": "prescription_id query parameter is required"
}
```

---

## Workflow Examples

### Workflow 1: Issue a Complete Prescription

```bash
# Step 1: Create appointment
curl -X POST http://localhost:8000/api/appointments \
  -d '{
    "patient_id":"770e8400-e29b-41d4-a716-446655440222",
    "doctor_id":"660e8400-e29b-41d4-a716-446655440111",
    "appointment_date":"2024-04-20",
    "time_slot":"10:00-10:30"
  }'
# Response includes: "id": "550e8400-e29b-41d4-a716-446655440000"

# Step 2: Get drug IDs
curl http://localhost:8000/api/drugs?name=aspirin

# Step 3: Create prescription with items
curl -X POST http://localhost:8000/api/prescriptions \
  -d '{
    "appointment_id":"550e8400-e29b-41d4-a716-446655440000",
    "doctor_id":"660e8400-e29b-41d4-a716-446655440111",
    "patient_id":"770e8400-e29b-41d4-a716-446655440222",
    "notes":"For pain relief",
    "items": [
      {
        "drug_id":"880e8400-e29b-41d4-a716-446655440333",
        "dosage":"500mg",
        "duration":"7 days",
        "instructions":"Take twice daily with food"
      }
    ]
  }'
```

### Workflow 2: Add More Drugs to Existing Prescription

```bash
# Get prescription ID first
curl http://localhost:8000/api/prescriptions/patient/770e8400-e29b-41d4-a716-446655440222

# Add new drug to prescription
curl -X POST "http://localhost:8000/api/prescription-items?prescription_id=aa0e8400-e29b-41d4-a716-446655440555" \
  -d '{
    "drug_id":"990e8400-e29b-41d4-a716-446655440444",
    "dosage":"10ml",
    "duration":"5 days",
    "instructions":"As needed for fever"
  }'
```

### Workflow 3: Get Patient's Medication History

```bash
# Get all prescriptions for a patient
curl "http://localhost:8000/api/prescriptions/patient/770e8400-e29b-41d4-a716-446655440222"

# Get detailed view of each prescription
curl http://localhost:8000/api/prescriptions/aa0e8400-e29b-41d4-a716-446655440555
```

### Workflow 4: Modify a Prescription

```bash
# Update prescription notes
curl -X PUT http://localhost:8000/api/prescriptions/aa0e8400-e29b-41d4-a716-446655440555 \
  -d '{
    "notes":"Patient reported side effects - consider alternatives"
  }'

# Update specific medication dosage
curl -X PUT http://localhost:8000/api/prescription-items/bb0e8400-e29b-41d4-a716-446655440666 \
  -d '{
    "drug_id":"880e8400-e29b-41d4-a716-446655440333",
    "dosage":"250mg",
    "duration":"7 days",
    "instructions":"Take once daily instead"
  }'
```

---

## Field Validation

### Prescription Fields

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| appointment_id | UUID | ✓ | Must exist in appointments table |
| doctor_id | UUID | ✓ | Must exist in doctors table |
| patient_id | UUID | ✓ | Must exist in users table |
| notes | Text | ✗ | Max 5000 characters |
| items | Array | ✗ | Array of PrescriptionItem objects |

### Prescription Item Fields

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| drug_id | UUID | ✓ | Must exist in drugs table |
| dosage | String | ✓ | 1-100 characters (e.g., "500mg", "10ml") |
| duration | String | ✓ | 1-100 characters (e.g., "7 days", "2 weeks") |
| instructions | Text | ✗ | Max 500 characters |

---

## Performance Characteristics

### Query Performance

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Create prescription | 150-250ms | Includes items creation |
| Get single prescription | 50-100ms | With items |
| List prescriptions (10) | 100-150ms | With pagination |
| Filter by patient | 100-150ms | Indexed on patient_id |
| Filter by doctor | 100-150ms | Indexed on doctor_id |
| Update prescription | 80-120ms | |
| Delete prescription | 100-150ms | Includes items |

### Indexing Strategy

Indexes on:
- `prescription_id` (PK)
- `appointment_id` (FK)
- `doctor_id` (FK)
- `patient_id` (FK)
- `created_at` (for sorting)
- `prescription_items.prescription_id` (FK)
- `prescription_items.drug_id` (FK)

---

## Integration with Other APIs

### Dependencies

- **Users API** - Patient IDs
- **Doctors API** - Doctor IDs
- **Appointments API** - Appointment IDs
- **Drugs API** - Drug IDs and drug information

### Related Operations

**Before creating a prescription:**
1. Ensure appointment exists: `GET /api/appointments/{id}`
2. Ensure doctor exists: `GET /api/doctors/{id}`
3. Ensure patient exists: `GET /api/users/{id}`
4. Ensure drugs exist: `GET /api/drugs/{id}`

**After creating a prescription:**
1. Can create medical notes
2. Can update appointment status
3. Can track stock transactions for drugs

---

## Best Practices

### Do's ✓

- Always validate appointment is completed before creating related prescriptions
- Include clear usage instructions for each drug
- Update prescription notes if patient reports side effects
- Use dosage formats consistently (e.g., "mg" not "milligram")
- Regularly archive old prescriptions

### Don'ts ✗

- Don't create prescriptions for non-existent appointments
- Don't prescribe expired drugs
- Don't forget to add notes for patient-specific instructions
- Don't modify appointment back-references
- Don't delete prescriptions without audit trail

---

## Rate Limiting & Throttling

**Current Implementation:** No rate limiting

**Recommended:** 
- 100 requests per minute per user
- 1000 requests per hour per API key

---

## Pagination Guide

All list endpoints support pagination:

```bash
# Get first 10 prescriptions
curl http://localhost:8000/api/prescriptions?skip=0&limit=10

# Get next 10
curl http://localhost:8000/api/prescriptions?skip=10&limit=10

# Get last 5
curl http://localhost:8000/api/prescriptions?skip=995&limit=5
```

---

## Filtering Guide

### Filter by Patient

```bash
curl "http://localhost:8000/api/prescriptions?patient_id=770e8400-e29b-41d4-a716-446655440222"
```

### Filter by Doctor

```bash
curl "http://localhost:8000/api/prescriptions?doctor_id=660e8400-e29b-41d4-a716-446655440111"
```

### Filter by Appointment

```bash
curl "http://localhost:8000/api/prescriptions?appointment_id=550e8400-e29b-41d4-a716-446655440000"
```

### Combine Filters

```bash
curl "http://localhost:8000/api/prescriptions?patient_id=770e8400-e29b-41d4-a716-446655440222&doctor_id=660e8400-e29b-41d4-a716-446655440111&skip=0&limit=20"
```

---

## Testing

### Using cURL

```bash
# Create prescription
curl -X POST http://localhost:8000/api/prescriptions \
  -H "Content-Type: application/json" \
  -d @prescription.json

# List all
curl http://localhost:8000/api/prescriptions

# Get single
curl http://localhost:8000/api/prescriptions/{id}

# Update
curl -X PUT http://localhost:8000/api/prescriptions/{id} \
  -H "Content-Type: application/json" \
  -d '{"notes":"Updated"}'

# Delete
curl -X DELETE http://localhost:8000/api/prescriptions/{id}
```

### Using Swagger UI

Navigate to: `http://localhost:8000/docs`

---

## Troubleshooting

### 404 Not Found

**Cause:** Prescription, appointment, or drug doesn't exist

**Solution:** 
1. Verify IDs are correct UUIDs
2. Check if resource was deleted
3. Confirm appointment/doctor/patient exist before creating prescription

### 400 Bad Request

**Cause:** Invalid appointment ID or missing appointment

**Solution:**
1. Ensure appointment_id is a valid UUID
2. Verify appointment exists: `GET /api/appointments/{id}`
3. Check appointment is linked to correct patient/doctor

### 422 Unprocessable Entity

**Cause:** Invalid field values or format

**Solution:**
1. Check dosage format (e.g., "500mg" not "500")
2. Verify duration format (e.g., "7 days" not "7")
3. Ensure all required fields are provided

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-04-15 | Initial release |

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
**Status:** Production Ready ✅
