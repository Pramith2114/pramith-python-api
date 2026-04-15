# ⚡ Doctor Documents API - Quick Reference

## Quick Endpoint Summary

| Action | Endpoint | Method |
|--------|----------|--------|
| Upload Document | `/api/doctor-documents` | POST |
| List All Documents | `/api/doctor-documents` | GET |
| Get One Document | `/api/doctor-documents/{id}` | GET |
| Get Doctor's Documents | `/api/doctor-documents/doctor/{doctor_id}` | GET |
| Update Document | `/api/doctor-documents/{id}` | PUT |
| Verify Document | `/api/doctor-documents/{id}/verify` | POST |
| Delete Document | `/api/doctor-documents/{id}` | DELETE |

---

## Quick Examples

### 1. Upload a Document
```bash
curl -X POST http://localhost:8000/api/doctor-documents \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical License",
    "file_url": "https://storage.example.com/license.pdf"
  }'
```

### 2. List All Documents
```bash
curl http://localhost:8000/api/doctor-documents
```

### 3. Filter Verified Documents
```bash
curl "http://localhost:8000/api/doctor-documents?verified=true"
```

### 4. Get Doctor's Documents
```bash
curl "http://localhost:8000/api/doctor-documents/doctor/550e8400-e29b-41d4-a716-446655440000"
```

### 5. Get Specific Document
```bash
curl http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001
```

### 6. Update Document
```bash
curl -X PUT http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001 \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://storage.example.com/license_updated.pdf"
  }'
```

### 7. Verify Document
```bash
curl -X POST http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001/verify \
  -H "Content-Type: application/json" \
  -d '{"verified": true}'
```

### 8. Delete Document
```bash
curl -X DELETE http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001
```

---

## Python Examples

### Upload Document
```python
import requests

requests.post(
    "http://localhost:8000/api/doctor-documents",
    json={
        "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
        "document_type": "Medical License",
        "file_url": "https://storage.example.com/license.pdf"
    }
)
```

### Get Doctor's Documents
```python
import requests

response = requests.get(
    "http://localhost:8000/api/doctor-documents/doctor/550e8400-e29b-41d4-a716-446655440000"
)
documents = response.json()
for doc in documents:
    print(f"{doc['document_type']}: {doc['verified']}")
```

### Verify Document
```python
import requests

requests.post(
    "http://localhost:8000/api/doctor-documents/660e8400-e29b-41d4-a716-446655440001/verify",
    json={"verified": True}
)
```

---

## Request/Response Fields

### Upload Request
```json
{
  "doctor_id": "UUID",
  "document_type": "string",
  "file_url": "string"
}
```

### Response
```json
{
  "id": "UUID",
  "doctor_id": "UUID",
  "document_type": "string",
  "file_url": "string",
  "verified": boolean,
  "uploaded_at": "datetime",
  "updated_at": "datetime"
}
```

---

## Query Parameters

### Get All Documents
```
?skip=0           # Skip first N documents
&limit=10         # Return max N documents
&doctor_id=UUID   # Filter by doctor
&verified=true    # Filter by verification status
```

### Get Doctor Documents
```
/doctor/{doctor_id}?skip=0&limit=10
```

---

## Document Types (Examples)

- Medical License
- Medical Degree
- Board Certification
- Specialization Certification
- Malpractice Insurance
- ID Proof
- Address Proof
- Other Credentials

---

## Common Workflows

### Workflow: Complete Document Upload & Verification
```bash
# 1. Doctor uploads license
DOC_ID=$(curl -s -X POST http://localhost:8000/api/doctor-documents \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": "550e8400-e29b-41d4-a716-446655440000",
    "document_type": "Medical License",
    "file_url": "https://storage.example.com/license.pdf"
  }' | jq -r '.id')
echo "Document ID: $DOC_ID"

# 2. Get document details
curl http://localhost:8000/api/doctor-documents/$DOC_ID

# 3. Admin verifies
curl -X POST http://localhost:8000/api/doctor-documents/$DOC_ID/verify \
  -H "Content-Type: application/json" \
  -d '{"verified": true}'
```

### Workflow: Get Doctor Profile with All Documents
```bash
DOCTOR_ID="550e8400-e29b-41d4-a716-446655440000"

# Get doctor details
curl http://localhost:8000/api/doctors/$DOCTOR_ID

# Get all documents for doctor
curl http://localhost:8000/api/doctor-documents/doctor/$DOCTOR_ID
```

---

## Error Messages

| Status | Error | Meaning |
|--------|-------|---------|
| 404 | "Doctor not found" | doctor_id doesn't exist |
| 404 | "Document not found" | document_id doesn't exist |
| 400 | "Associated user must have 'doctor' role" | User not a doctor |

---

## Pagination

### Get Page 1 (10 items)
```bash
curl "http://localhost:8000/api/doctor-documents?skip=0&limit=10"
```

### Get Page 2 (items 11-20)
```bash
curl "http://localhost:8000/api/doctor-documents?skip=10&limit=10"
```

### Get Page 3 (items 21-30)
```bash
curl "http://localhost:8000/api/doctor-documents?skip=20&limit=30"
```

---

## Filtering

### Get All Unverified Documents
```bash
curl "http://localhost:8000/api/doctor-documents?verified=false"
```

### Get All Verified Documents
```bash
curl "http://localhost:8000/api/doctor-documents?verified=true"
```

### Get Specific Doctor's Verified Documents
```bash
curl "http://localhost:8000/api/doctor-documents/doctor/550e8400-e29b-41d4-a716-446655440000?verified=true"
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 201 | Created |
| 200 | OK |
| 204 | No Content (deleted) |
| 400 | Bad Request |
| 404 | Not Found |

---

## Database Schema

```
doctor_documents Table:
┌─────────┬──────────┬────────────────────┬──────────────┬──────────┐
│  id     │ doctor_id│ document_type      │ file_url     │ verified │
│  (UUID) │ (UUID)   │ (String)           │ (Text)       │ (Bool)   │
├─────────┼──────────┼────────────────────┼──────────────┼──────────┤
│ 660e... │ 550e...  │ Medical License    │ https://...  │ true     │
│ 770e... │ 550e...  │ Medical Degree     │ https://...  │ true     │
│ 880e... │ 550e...  │ Board Certification│ https://...  │ false    │
└─────────┴──────────┴────────────────────┴──────────────┴──────────┘
```

---

## Tips

1. **Always use UUID for doctor_id** (not integer ID)
2. **Store documents externally** (S3, CDN, etc.) - this API manages metadata
3. **Verify before display** - set verified=true before showing to patients
4. **Track upload_at** - use for sorting/filtering recent uploads
5. **Use consistent naming** for document_type (e.g., "Medical License" not "license")
6. **Delete carefully** - deletion is permanent and affects all references

---

## Integration

**Works with:**
- Doctor API: Link documents to doctor profiles
- User API: Doctor must have user role='doctor'
- Admin APIs: For verification workflow

