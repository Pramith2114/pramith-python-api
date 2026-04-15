# 📄 Doctor Documents API - Complete Reference

## Overview

The **Doctor Documents API** allows doctors to upload, manage, and verify professional credentials and documents (licenses, degrees, certifications, etc.). This API includes role-based access control and document verification workflow.

## Database Table Structure

```sql
CREATE TABLE doctor_documents (
  id UUID PRIMARY KEY,
  doctor_id UUID REFERENCES doctors(id),
  document_type VARCHAR,
  file_url TEXT,
  verified BOOLEAN DEFAULT FALSE,
  uploaded_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## API Endpoints Summary

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|------------|
| **POST** | `/api/doctor-documents` | Upload new document | 201 |
| **GET** | `/api/doctor-documents` | Get all documents (paginated, filterable) | 200 |
| **GET** | `/api/doctor-documents/{id}` | Get specific document | 200 |
| **GET** | `/api/doctor-documents/doctor/{doctor_id}` | Get all documents for a doctor | 200 |
| **PUT** | `/api/doctor-documents/{id}` | Update document info | 200 |
| **POST** | `/api/doctor-documents/{id}/verify` | Verify/reject document | 200 |
| **DELETE** | `/api/doctor-documents/{id}` | Delete document | 204 |

---

## Detailed Endpoints

### 1. Upload Doctor Document

**Endpoint:** `POST /api/doctor-documents`

**Description:** Upload a new professional document for a doctor.

**Request Body:**
```json
{
  "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "Medical License",
  "file_url": "https://storage.example.com/licenses/doc123.pdf"
}
```

**Fields:**
- `doctor_id` (UUID, required): UUID of the doctor uploading the document
- `document_type` (string, required): Type of document (e.g., "Medical License", "Degree", "Certification")
- `file_url` (string, required): URL to the uploaded document file

**Response (201 Created):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "Medical License",
  "file_url": "https://storage.example.com/licenses/doc123.pdf",
  "verified": false,
  "uploaded_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T10:30:00"
}
```

**Error Responses:**
- `404 Not Found` - If doctor doesn't exist
- `400 Bad Request` - If associated user doesn't have doctor role

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/doctor-documents \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical License",
    "file_url": "https://storage.example.com/licenses/doc123.pdf"
  }'
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/doctor-documents",
    json={
        "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
        "document_type": "Medical License",
        "file_url": "https://storage.example.com/licenses/doc123.pdf"
    }
)
print(response.json())
```

---

### 2. Get All Documents

**Endpoint:** `GET /api/doctor-documents`

**Description:** Retrieve all doctor documents with optional pagination and filtering.

**Query Parameters:**
- `skip` (integer, default: 0): Number of documents to skip
- `limit` (integer, default: 10): Maximum documents to return
- `doctor_id` (UUID, optional): Filter by specific doctor
- `verified` (boolean, optional): Filter by verification status (true/false)

**Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical License",
    "file_url": "https://storage.example.com/licenses/doc123.pdf",
    "verified": false,
    "uploaded_at": "2024-04-14T10:30:00",
    "updated_at": "2024-04-14T10:30:00"
  }
]
```

**cURL Examples:**

Get first 10 documents:
```bash
curl http://localhost:8000/api/doctor-documents
```

Get verified documents only:
```bash
curl "http://localhost:8000/api/doctor-documents?verified=true"
```

Get unverified documents for specific doctor:
```bash
curl "http://localhost:8000/api/doctor-documents?doctor_id=550e8400-e29b-41d4-a716-446655440000&verified=false"
```

Pagination (get next page):
```bash
curl "http://localhost:8000/api/doctor-documents?skip=10&limit=10"
```

---

### 3. Get Specific Document

**Endpoint:** `GET /api/doctor-documents/{document_id}`

**Description:** Retrieve a specific document by UUID.

**Path Parameters:**
- `document_id` (UUID, required): UUID of the document

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "Medical License",
  "file_url": "https://storage.example.com/licenses/doc123.pdf",
  "verified": true,
  "uploaded_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T11:00:00"
}
```

**Error Responses:**
- `404 Not Found` - If document doesn't exist

**cURL Example:**
```bash
curl http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001
```

---

### 4. Get Doctor's Documents

**Endpoint:** `GET /api/doctor-documents/doctor/{doctor_id}`

**Description:** Retrieve all documents for a specific doctor.

**Path Parameters:**
- `doctor_id` (UUID, required): UUID of the doctor

**Query Parameters:**
- `skip` (integer, default: 0): Number of documents to skip
- `limit` (integer, default: 10): Maximum documents to return

**Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical License",
    "file_url": "https://storage.example.com/licenses/doc123.pdf",
    "verified": true,
    "uploaded_at": "2024-04-14T10:30:00",
    "updated_at": "2024-04-14T11:00:00"
  },
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical Degree",
    "file_url": "https://storage.example.com/degrees/deg456.pdf",
    "verified": true,
    "uploaded_at": "2024-04-14T10:35:00",
    "updated_at": "2024-04-14T11:05:00"
  }
]
```

**Error Responses:**
- `404 Not Found` - If doctor doesn't exist

**cURL Example:**
```bash
curl http://localhost:8000/api/doctor-documents/doctor/550e8400-e29b-41d4-a716-446655440000
```

---

### 5. Update Document

**Endpoint:** `PUT /api/doctor-documents/{document_id}`

**Description:** Update document information (document type or file URL).

**Path Parameters:**
- `document_id` (UUID, required): UUID of the document

**Request Body:**
```json
{
  "document_type": "Updated Medical License",
  "file_url": "https://storage.example.com/licenses/doc123_updated.pdf"
}
```

**Fields (all optional):**
- `document_type` (string, optional): New document type
- `file_url` (string, optional): New file URL

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "Updated Medical License",
  "file_url": "https://storage.example.com/licenses/doc123_updated.pdf",
  "verified": true,
  "uploaded_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T12:00:00"
}
```

**Error Responses:**
- `404 Not Found` - If document doesn't exist

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001 \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "Updated Medical License",
    "file_url": "https://storage.example.com/licenses/doc123_updated.pdf"
  }'
```

---

### 6. Verify Document

**Endpoint:** `POST /api/doctor-documents/{document_id}/verify`

**Description:** Verify or reject a document.

**Path Parameters:**
- `document_id` (UUID, required): UUID of the document

**Request Body:**
```json
{
  "verified": true
}
```

**Fields:**
- `verified` (boolean, required): Verification status (true = verified, false = rejected)

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type": "Medical License",
  "file_url": "https://storage.example.com/licenses/doc123.pdf",
  "verified": true,
  "uploaded_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T13:30:00"
}
```

**Error Responses:**
- `404 Not Found` - If document doesn't exist

**cURL Examples:**

Approve document:
```bash
curl -X POST http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001/verify \
  -H "Content-Type: application/json" \
  -d '{
    "verified": true
  }'
```

Reject document:
```bash
curl -X POST http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001/verify \
  -H "Content-Type: application/json" \
  -d '{
    "verified": false
  }'
```

---

### 7. Delete Document

**Endpoint:** `DELETE /api/doctor-documents/{document_id}`

**Description:** Delete a document by ID.

**Path Parameters:**
- `document_id` (UUID, required): UUID of the document

**Response (204 No Content)**

**Error Responses:**
- `404 Not Found` - If document doesn't exist

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001
```

---

## Data Models

### DoctorDocumentCreate (Request)
```python
{
    "doctor_id": str (UUID),          # required
    "document_type": str,              # required
    "file_url": str                    # required
}
```

### DoctorDocumentResponse (Response)
```python
{
    "id": str (UUID),
    "doctor_id": str (UUID),
    "document_type": str,
    "file_url": str,
    "verified": bool,
    "uploaded_at": str (datetime),
    "updated_at": str (datetime)
}
```

### DoctorDocumentUpdate (Request)
```python
{
    "document_type": str (optional),
    "file_url": str (optional)
}
```

### DoctorDocumentVerify (Request)
```python
{
    "verified": bool                   # required
}
```

---

## Common Workflows

### Workflow 1: Upload Doctor License
```bash
# 1. Doctor uploads license
curl -X POST http://localhost:8000/api/doctor-documents \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical License",
    "file_url": "https://storage.example.com/licenses/license.pdf"
  }'

# Response includes: document_id, verified: false
```

### Workflow 2: Admin Verifies Document
```bash
# 1. Get unverified documents
curl "http://localhost:8000/api/doctor-documents?verified=false"

# 2. Review document at file_url

# 3. Verify the document
curl -X POST http://localhost:8000/api/doctor-documents/{document_id}/verify \
  -H "Content-Type: application/json" \
  -d '{"verified": true}'
```

### Workflow 3: Doctor Updates Document
```bash
# 1. Doctor gets their documents
curl "http://localhost:8000/api/doctor-documents/doctor/550e8400-e29b-41d4-a716-446655440000"

# 2. Doctor updates document with new file URL
curl -X PUT http://localhost:8000/api/doctor-documents/{document_id} \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://storage.example.com/licenses/license_updated.pdf"
  }'

# 3. Admin re-verifies if needed
curl -X POST http://localhost:8000/api/doctor-documents/{document_id}/verify \
  -H "Content-Type: application/json" \
  -d '{"verified": true}'
```

### Workflow 4: Get Complete Doctor Profile with Documents
```bash
# 1. Get doctor
curl http://localhost:8000/api/doctors/{doctor_id}

# 2. Get all documents for that doctor
curl "http://localhost:8000/api/doctor-documents/doctor/{doctor_id}"

# Result: Full picture of doctor's profile and credentials
```

---

## Error Handling

### Common Error Scenarios

**404 Not Found:**
```json
{
  "detail": "Doctor not found"
}
```

**400 Bad Request:**
```json
{
  "detail": "Associated user must have 'doctor' role"
}
```

**404 Document Not Found:**
```json
{
  "detail": "Document not found"
}
```

---

## Database Schema Details

```sql
CREATE TABLE doctor_documents (
  id UUID NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  doctor_id UUID NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
  document_type VARCHAR(255) NOT NULL,
  file_url TEXT NOT NULL,
  verified BOOLEAN NOT NULL DEFAULT FALSE,
  uploaded_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_doctor_id (doctor_id),
  CONSTRAINT fk_doctor_id FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
```

### Fields Explanation

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | Primary key, auto-generated |
| `doctor_id` | UUID | Foreign key to doctors.id |
| `document_type` | VARCHAR | Type of document (string, required) |
| `file_url` | TEXT | URL to document file |
| `verified` | BOOLEAN | Verification status (default: false) |
| `uploaded_at` | TIMESTAMP | Auto-set to current time |
| `updated_at` | TIMESTAMP | Auto-updated on changes |

---

## Access Control

- **Doctor Role Required**: Users must have `role='doctor'` to upload documents
- **Doctor Association**: Document must be associated with a doctor
- **No Authentication Required**: For simplicity, endpoints are open (add authentication as needed)

---

## Testing

### Quick Test Script

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Create a doctor (if not exists)
doctor_id = "550e8400-e29b-41d4-a716-446655440000"

# 2. Upload document
doc_response = requests.post(
    f"{BASE_URL}/api/doctor-documents",
    json={
        "doctor_id": doctor_id,
        "document_type": "Medical License",
        "file_url": "https://storage.example.com/license.pdf"
    }
)
document_id = doc_response.json()["id"]
print(f"✓ Document uploaded: {document_id}")

# 3. Get all documents
docs = requests.get(f"{BASE_URL}/api/doctor-documents")
print(f"✓ Found {len(docs.json())} documents")

# 4. Verify document
verify_response = requests.post(
    f"{BASE_URL}/api/doctor-documents/{document_id}/verify",
    json={"verified": True}
)
print(f"✓ Document verified: {verify_response.json()['verified']}")

# 5. Get verified documents only
verified = requests.get(
    f"{BASE_URL}/api/doctor-documents?verified=true"
)
print(f"✓ Verified documents: {len(verified.json())}")
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| **201** | Document created successfully |
| **200** | Request successful |
| **204** | Document deleted (no content) |
| **400** | Bad request (validation error) |
| **404** | Resource not found |
| **500** | Server error |

---

## Best Practices

1. **Always validate doctor_id exists** before uploading documents
2. **Use consistent document_type naming** (e.g., "Medical License", not "license")
3. **Store file_url securely** (use CDN or secure cloud storage)
4. **Verify documents before showing to patients** (set verified=true)
5. **Track document_type for auditing** and compliance purposes
6. **Handle file uploads separately** (this API manages metadata only)

---

## Integration with Other APIs

### Relationship with Doctor API
```
Users (id)
  ↓
Doctors (user_id → users.id)
  ↓
Doctor Documents (doctor_id → doctors.id)
```

---

## Interactive Testing

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

