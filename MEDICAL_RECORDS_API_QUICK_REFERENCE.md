# 📚 Medical Records API - Quick Reference

## Quick Lookup Guide

### Endpoints at a Glance

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/medical-records` | Create medical record |
| GET | `/api/medical-records` | List all records (filterable) |
| GET | `/api/medical-records/{id}` | Get single record |
| GET | `/api/medical-records/patient/{id}` | Get patient's records |
| GET | `/api/medical-records/type/{type}` | Get records by type |
| PUT | `/api/medical-records/{id}` | Update record |
| DELETE | `/api/medical-records/{id}` | Delete record |

---

## Quick Examples

### Create Medical Record
```bash
curl -X POST http://localhost:8000/api/medical-records \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "770e8400-e29b-41d4-a716-446655440222",
    "file_url": "https://storage.example.com/lab.pdf",
    "record_type": "lab_report",
    "description": "Blood test results"
  }'
```

**Response (201 Created):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "patient_id": "770e8400-e29b-41d4-a716-446655440222",
  "file_url": "https://storage.example.com/lab.pdf",
  "record_type": "lab_report",
  "description": "Blood test results",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

---

### Get All Records
```bash
curl http://localhost:8000/api/medical-records
```

---

### Filter Records

#### By Patient
```bash
curl "http://localhost:8000/api/medical-records?patient_id=770e8400-e29b-41d4-a716-446655440222"
```

#### By Type
```bash
curl "http://localhost:8000/api/medical-records?record_type=lab_report"
```

#### By Patient AND Type
```bash
curl "http://localhost:8000/api/medical-records?patient_id=770e8400-e29b-41d4-a716-446655440222&record_type=x_ray"
```

#### With Pagination
```bash
curl "http://localhost:8000/api/medical-records?skip=10&limit=5"
```

---

### Get Patient's Records
```bash
curl "http://localhost:8000/api/medical-records/patient/770e8400-e29b-41d4-a716-446655440222"
```

**With Optional Type Filter:**
```bash
curl "http://localhost:8000/api/medical-records/patient/770e8400-e29b-41d4-a716-446655440222?record_type=lab_report"
```

---

### Get Single Record
```bash
curl http://localhost:8000/api/medical-records/aa0e8400-e29b-41d4-a716-446655440555
```

---

### Get Records by Type
```bash
curl "http://localhost:8000/api/medical-records/type/lab_report"
```

---

### Update Record
```bash
curl -X PUT http://localhost:8000/api/medical-records/aa0e8400-e29b-41d4-a716-446655440555 \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://storage.example.com/lab_updated.pdf",
    "record_type": "lab_report",
    "description": "Updated blood test results"
  }'
```

---

### Delete Record
```bash
curl -X DELETE http://localhost:8000/api/medical-records/aa0e8400-e29b-41d4-a716-446655440555
```

**Response:** `204 No Content`

---

## Response Schemas

### Medical Record Object
```json
{
  "id": "uuid",
  "patient_id": "uuid",
  "file_url": "string",
  "record_type": "string",
  "description": "string (optional)",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Successful GET/PUT |
| 201 | Created - Successful POST |
| 204 | No Content - Successful DELETE |
| 400 | Bad Request - Invalid format |
| 404 | Not Found - Resource not found |
| 422 | Validation Error - Invalid data |

---

## Common Record Types

```
• lab_report         Lab test results
• x_ray              X-ray imaging
• ultrasound         Ultrasound scan
• mri                MRI scan
• ct_scan            CT scan
• ekg                Electrocardiogram
• prescription       Prescription document
• discharge_summary  Discharge summary
• diagnosis          Diagnosis notes
• surgery_report     Surgery report
• vaccination_record Vaccination record
• consultation_note  Doctor notes
• insurance_form     Insurance document
• referral           Referral letter
• other              Other documents
```

---

## Query Parameters

### List & Filter Query Parameters
- `skip` (int) - Records to skip (default: 0)
- `limit` (int) - Max records to return (default: 10)
- `patient_id` (UUID) - Filter by patient
- `record_type` (string) - Filter by type

### Example Combinations
```bash
# Skip 20, return 5
?skip=20&limit=5

# Patient's recent records
?patient_id=xxx&skip=0&limit=10

# Specific type, paginated
?record_type=lab_report&skip=10&limit=5
```

---

## Request Body Schema

### Create Medical Record (POST)
```json
{
  "patient_id": "uuid (required)",
  "file_url": "string (required)",
  "record_type": "string (required, max 100)",
  "description": "string (optional, max 5000)"
}
```

### Update Medical Record (PUT)
```json
{
  "file_url": "string (optional)",
  "record_type": "string (optional)",
  "description": "string (optional)"
}
```

---

## Field Validation

| Field | Type | Required | Max Length | Notes |
|-------|------|----------|-----------|-------|
| patient_id | UUID | ✓ | - | Must exist in users table |
| file_url | String | ✓ | 2000 | Valid URL format |
| record_type | String | ✓ | 100 | Categorize document type |
| description | String | ✗ | 5000 | Optional context |

---

## Filtering & Pagination Guide

### Get All Records with Pagination
```bash
# Page 1 (first 10)
curl "http://localhost:8000/api/medical-records?skip=0&limit=10"

# Page 2 (next 10)
curl "http://localhost:8000/api/medical-records?skip=10&limit=10"

# Page 3 (next 10)
curl "http://localhost:8000/api/medical-records?skip=20&limit=10"
```

### Filter by Single Criteria
```bash
# All records for patient
curl "http://localhost:8000/api/medical-records?patient_id=xxx"

# All lab reports
curl "http://localhost:8000/api/medical-records?record_type=lab_report"
```

### Filter and Paginate
```bash
# Patient's lab reports, first 5
curl "http://localhost:8000/api/medical-records?patient_id=xxx&record_type=lab_report&limit=5"

# Patient's lab reports, page 2
curl "http://localhost:8000/api/medical-records?patient_id=xxx&record_type=lab_report&skip=5&limit=5"
```

---

## Error Codes & Solutions

| Error | Possible Cause | Solution |
|-------|---|-----------|
| 404 Not Found | Record doesn't exist | Verify ID is correct |
| 404 Not Found | Patient doesn't exist | Verify patient_id exists |
| 400 Bad Request | Wrong data type | Check UUIDs are valid format |
| 422 Unprocessable | String too long | Trim record_type or description |
| 422 Unprocessable | Bad URL format | Verify file_url is valid HTTPS |

---

## Testing in Swagger UI

1. Navigate to: `http://localhost:8000/docs`
2. Scroll to "Medical Records" section
3. Click endpoint to expand
4. Click "Try it out"
5. Enter required parameters
6. Click "Execute"
7. View response

---

## Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Create
response = requests.post(f"{BASE_URL}/medical-records", json={
    "patient_id": "770e8400-e29b-41d4-a716-446655440222",
    "file_url": "https://storage.example.com/lab.pdf",
    "record_type": "lab_report",
    "description": "Blood test"
})
record = response.json()

# Get
response = requests.get(f"{BASE_URL}/medical-records/{record['id']}")
print(response.json())

# List
response = requests.get(f"{BASE_URL}/medical-records?limit=10")
print(response.json())

# Update
requests.put(f"{BASE_URL}/medical-records/{record['id']}", json={
    "description": "Updated: Blood test from lab A"
})

# Delete
requests.delete(f"{BASE_URL}/medical-records/{record['id']}")
```

---

## JavaScript Example

```javascript
const BASE_URL = "http://localhost:8000/api";

// Create
const response = await fetch(`${BASE_URL}/medical-records`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    patient_id: "770e8400-e29b-41d4-a716-446655440222",
    file_url: "https://storage.example.com/lab.pdf",
    record_type: "lab_report",
    description: "Blood test"
  })
});
const record = await response.json();

// Get
const getResponse = await fetch(`${BASE_URL}/medical-records/${record.id}`);
console.log(await getResponse.json());

// List
const listResponse = await fetch(`${BASE_URL}/medical-records?limit=10`);
console.log(await listResponse.json());

// Update
await fetch(`${BASE_URL}/medical-records/${record.id}`, {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    description: "Updated: Blood test from lab A"
  })
});

// Delete
await fetch(`${BASE_URL}/medical-records/${record.id}`, {
  method: "DELETE"
});
```

---

## Common Workflows

### Upload New Medical Record Workflow
```
1. Get patient ID (from users API)
   GET /api/users?role=patient
   
2. Upload file to storage service
   (External operation - get file_url)
   
3. Create medical record
   POST /api/medical-records
   {patient_id, file_url, record_type, description}
   
4. Confirm creation
   GET /api/medical-records/{id}
```

### Review Patient Medical History Workflow
```
1. Get patient's records
   GET /api/medical-records/patient/{patient_id}
   
2. Filter by type if needed
   GET /api/medical-records/patient/{patient_id}?record_type=lab_report
   
3. View individual record details
   GET /api/medical-records/{id}
```

### Search Records by Type Workflow
```
1. Get all records of type
   GET /api/medical-records/type/{record_type}
   
2. View pagination if large result set
   GET /api/medical-records/type/{record_type}?skip=10&limit=5
   
3. View individual record
   GET /api/medical-records/{id}
```

---

## Quick Notes

- All IDs are UUIDs
- Timestamps are ISO 8601 format
- File URLs should be HTTPS for security
- Patient must exist before creating record
- Records are immutable after creation (only description/file_url updatable)
- Deletions are permanent - archive before deleting
- Use pagination for large result sets

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
✅ **Status:** Ready to Use
