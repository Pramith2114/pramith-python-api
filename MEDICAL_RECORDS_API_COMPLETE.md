# 📋 Medical Records API - Complete Specification

## Overview

The **Medical Records API** is a complete REST API for managing patient medical records and documents. It supports uploading, storing, and retrieving various types of medical documents including lab reports, X-rays, prescriptions, discharge summaries, and other patient records.

**Features:**
- Create and store medical records
- Link records to patient profiles
- Categorize records by type
- Filter records by patient or type
- Full CRUD operations
- Automatic timestamp tracking
- Complete audit trail

---

## Database Table

### Medical Records Table

```sql
CREATE TABLE medical_records (
  id UUID PRIMARY KEY,
  patient_id UUID NOT NULL REFERENCES users(id),
  file_url TEXT NOT NULL,
  record_type VARCHAR(100) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (patient_id),
  INDEX (record_type),
  INDEX (created_at)
);
```

**Fields:**
- `id`: Unique medical record identifier (UUID)
- `patient_id`: Reference to the patient
- `file_url`: URL to the uploaded medical record file
- `record_type`: Type of record (e.g., lab_report, x_ray, prescription, discharge_summary)
- `description`: Additional description or notes about the record
- `created_at`: Timestamp when record was created
- `updated_at`: Timestamp when record was last modified

---

## API Endpoints

### Medical Records Endpoints

#### 1. Create Medical Record
**Endpoint:** `POST /api/medical-records`

**Status Code:** `201 Created`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "file_url": "https://storage.example.com/records/lab_report_2024_01.pdf",
  "record_type": "lab_report",
  "description": "Complete blood count (CBC) test results"
}
```

**Success Response:**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "file_url": "https://storage.example.com/records/lab_report_2024_01.pdf",
  "record_type": "lab_report",
  "description": "Complete blood count (CBC) test results",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

**Error Responses:**
- `404 Not Found` - Patient not found
- `400 Bad Request` - Invalid data format
- `422 Unprocessable Entity` - Validation error

---

#### 2. Get All Medical Records
**Endpoint:** `GET /api/medical-records`

**Query Parameters:**
- `skip` (integer, default: 0) - Number of records to skip
- `limit` (integer, default: 10) - Maximum number to return
- `patient_id` (UUID, optional) - Filter by patient
- `record_type` (string, optional) - Filter by record type

**Example Requests:**
```bash
# Get all records
GET /api/medical-records

# Filter by patient
GET /api/medical-records?patient_id=770e8400-e29b-41d4-a716-446655440222

# Filter by type
GET /api/medical-records?record_type=lab_report

# Combine filters
GET /api/medical-records?patient_id=770e8400-e29b-41d4-a716-446655440222&record_type=x_ray&skip=0&limit=10
```

**Success Response (200 OK):**
```json
[
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440555",
    "patient_id": "770e8400-e29b-41d4-a716-446655440222",
    "file_url": "https://storage.example.com/records/lab_report_2024_01.pdf",
    "record_type": "lab_report",
    "description": "Complete blood count (CBC) test results",
    "created_at": "2024-04-15T14:30:00",
    "updated_at": "2024-04-15T14:30:00"
  }
]
```

---

#### 3. Get Single Medical Record
**Endpoint:** `GET /api/medical-records/{record_id}`

**Path Parameters:**
- `record_id` (UUID) - Medical record identifier

**Success Response (200 OK):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "file_url": "https://storage.example.com/records/lab_report_2024_01.pdf",
  "record_type": "lab_report",
  "description": "Complete blood count (CBC) test results",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Medical record not found"
}
```

---

#### 4. Get Patient Medical Records
**Endpoint:** `GET /api/medical-records/patient/{patient_id}`

**Path Parameters:**
- `patient_id` (UUID) - Patient identifier

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)
- `record_type` (string, optional) - Filter by record type

**Success Response (200 OK):**
Returns list of medical records for the patient, ordered by most recent first.

---

#### 5. Get Records by Type
**Endpoint:** `GET /api/medical-records/type/{record_type}`

**Path Parameters:**
- `record_type` (string) - Type of record (lab_report, x_ray, prescription, etc.)

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)

**Success Response (200 OK):**
Returns list of all records of the specified type.

---

#### 6. Update Medical Record
**Endpoint:** `PUT /api/medical-records/{record_id}`

**Path Parameters:**
- `record_id` (UUID) - Medical record identifier

**Request Body:**
```json
{
  "file_url": "https://storage.example.com/records/lab_report_2024_01_v2.pdf",
  "record_type": "lab_report",
  "description": "Updated: Complete blood count (CBC) test results - corrected values"
}
```

**Success Response (200 OK):**
Returns updated medical record object.

---

#### 7. Delete Medical Record
**Endpoint:** `DELETE /api/medical-records/{record_id}`

**Path Parameters:**
- `record_id` (UUID) - Medical record identifier

**Success Response:** `204 No Content`

---

## Record Types

Common medical record types:

| Type | Description |
|------|-------------|
| `lab_report` | Laboratory test results |
| `x_ray` | X-ray imaging results |
| `ultrasound` | Ultrasound imaging |
| `mri` | MRI scan results |
| `ct_scan` | CT scan results |
| `ekg` | Electrocardiogram |
| `prescription` | Prescription documents |
| `discharge_summary` | Hospital discharge summary |
| `diagnosis` | Diagnosis documents |
| `surgery_report` | Surgical procedure report |
| `vaccination_record` | Vaccination records |
| `consultation_note` | Doctor consultation notes |
| `insurance_form` | Insurance related documents |
| `referral` | Doctor referral letters |
| `other` | Other medical documents |

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
| 400 | Bad Request | Invalid patient ID format |
| 404 | Not Found | Medical record or patient not found |
| 422 | Unprocessable Entity | Invalid field format or value |
| 500 | Internal Server Error | Database or server error |

### Common Errors

**Medical Record Not Found:**
```json
{
  "detail": "Medical record not found"
}
```

**Patient Not Found:**
```json
{
  "detail": "Patient not found"
}
```

---

## Workflow Examples

### Workflow 1: Upload Patient Lab Report

```bash
# Step 1: Get patient ID (from users API)
curl http://localhost:8000/api/users?role=patient&limit=1

# Step 2: Upload file (to your storage service)
# Returns: file_url = "https://storage.example.com/records/lab_2024_04_15.pdf"

# Step 3: Create medical record
curl -X POST http://localhost:8000/api/medical-records \
  -d '{
    "patient_id":"770e8400-e29b-41d4-a716-446655440222",
    "file_url":"https://storage.example.com/records/lab_2024_04_15.pdf",
    "record_type":"lab_report",
    "description":"CBC test - April 15, 2024"
  }'
```

### Workflow 2: Get Patient Medical History

```bash
# Get all records for patient
curl "http://localhost:8000/api/medical-records/patient/770e8400-e29b-41d4-a716-446655440222"

# Get only lab reports
curl "http://localhost:8000/api/medical-records/patient/770e8400-e29b-41d4-a716-446655440222?record_type=lab_report"

# Get X-ray records
curl "http://localhost:8000/api/medical-records/patient/770e8400-e29b-41d4-a716-446655440222?record_type=x_ray"
```

### Workflow 3: Find All Records of a Type

```bash
# Get all lab reports in system
curl "http://localhost:8000/api/medical-records/type/lab_report"

# Get all X-rays
curl "http://localhost:8000/api/medical-records/type/x_ray"

# Get all discharge summaries
curl "http://localhost:8000/api/medical-records/type/discharge_summary"
```

### Workflow 4: Update Record Information

```bash
# Update description and file URL
curl -X PUT http://localhost:8000/api/medical-records/aa0e8400-e29b-41d4-a716-446655440555 \
  -d '{
    "file_url":"https://storage.example.com/records/lab_2024_04_15_updated.pdf",
    "record_type":"lab_report",
    "description":"CBC test - April 15, 2024 (Updated with corrected values)"
  }'
```

---

## Field Validation

### Medical Record Fields

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| patient_id | UUID | ✓ | Must exist in users table |
| file_url | String | ✓ | Valid URL format, max 2000 chars |
| record_type | String | ✓ | Max 100 characters |
| description | Text | ✗ | Max 5000 characters |

---

## Performance Characteristics

### Query Performance

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Create record | 100-200ms | File URL validation |
| Get single record | 20-50ms | Direct lookup by ID |
| List records (10) | 80-120ms | With pagination |
| Filter by patient | 100-150ms | Indexed on patient_id |
| Filter by type | 100-150ms | Indexed on record_type |
| Update record | 80-120ms | |
| Delete record | 80-120ms | |

### Indexing Strategy

Indexes on:
- `id` (PK)
- `patient_id` (FK)
- `record_type` (for filtering)
- `created_at` (for sorting)

---

## Integration with Other APIs

### Dependencies

- **Users API** - Patient IDs
- **File Storage Service** - File URLs

### Related Operations

**Before creating a record:**
1. Ensure patient exists: `GET /api/users/{id}`
2. Upload file to storage service and get file URL

**After creating a record:**
1. Can link to prescriptions
2. Can include in patient profile
3. Can use in doctor consultations
4. Can track in medical history

---

## Best Practices

### Do's ✓

- Always verify patient exists before creating record
- Use descriptive record types for easy filtering
- Include detailed descriptions for context
- Maintain file URLs with version control
- Regularly audit medical record access
- Archive old records appropriately
- Use secure storage for file URLs (HTTPS)

### Don'ts ✗

- Don't create records for non-existent patients
- Don't use generic descriptions
- Don't expose sensitive information in descriptions
- Don't use insecure file URLs (HTTP)
- Don't delete records without backup
- Don't modify patient_id after creation
- Don't store actual files in database (use URLs only)

---

## Testing

### Using cURL

```bash
# Create
curl -X POST http://localhost:8000/api/medical-records \
  -H "Content-Type: application/json" \
  -d '{...}'

# List
curl http://localhost:8000/api/medical-records

# Get
curl http://localhost:8000/api/medical-records/{id}

# Filter by patient
curl "http://localhost:8000/api/medical-records/patient/{id}"

# Update
curl -X PUT http://localhost:8000/api/medical-records/{id} \
  -H "Content-Type: application/json" \
  -d '{...}'

# Delete
curl -X DELETE http://localhost:8000/api/medical-records/{id}
```

### Using Swagger UI

Navigate to: `http://localhost:8000/docs`

---

## Troubleshooting

### 404 Not Found

**Cause:** Medical record or patient doesn't exist

**Solution:**
1. Verify patient ID is correct UUID
2. Check if record was deleted
3. Confirm patient exists: `GET /api/users/{id}`

### 400 Bad Request

**Cause:** Invalid data format

**Solution:**
1. Verify patient_id is valid UUID
2. Check file_url is valid URL
3. Ensure all required fields provided

### 422 Unprocessable Entity

**Cause:** Invalid field values

**Solution:**
1. Check record_type length (max 100 chars)
2. Verify file_url format
3. Check description length (max 5000 chars)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-04-15 | Initial release |

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
**Status:** Production Ready ✅
