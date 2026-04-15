# Search Logs & Symptom Checker APIs - Complete Specification

**API Version:** 1.0  
**Status:** Production Ready  
**Last Updated:** April 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Database Schema](#database-schema)
3. [Search Logs API Endpoints](#search-logs-api-endpoints)
4. [Symptom Checker API Endpoints](#symptom-checker-api-endpoints)
5. [Request/Response Examples](#requestresponse-examples)
6. [Error Handling](#error-handling)
7. [Field Validation](#field-validation)
8. [Integration Points](#integration-points)

---

## Overview

These two related APIs provide complete systems for:

**Search Logs API:** Tracks and manages user search queries and their results
- Log search queries for analytics
- Retrieve search history by user
- Analyze search patterns

**Symptom Checker API:** Manages symptom-to-disease mapping with confidence scores
- Create and retrieve symptom-disease associations
- Search by symptoms or disease names
- Filter by confidence thresholds
- Support clinical decision support

---

## Database Schema

### Search Logs Table

```sql
CREATE TABLE search_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    query TEXT NOT NULL,
    results_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

**Columns:**
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique search log identifier |
| user_id | UUID | NOT NULL, FK | Reference to user |
| query | TEXT | NOT NULL | Search query text |
| results_count | INT | DEFAULT 0 | Number of results returned |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

### Symptom Checker Table

```sql
CREATE TABLE symptom_checkers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symptoms TEXT NOT NULL,
    suggested_disease TEXT NOT NULL,
    confidence_score DECIMAL(3, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_created_at (created_at)
);
```

**Columns:**
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique symptom checker ID |
| symptoms | TEXT | NOT NULL | Symptom description or comma-separated list |
| suggested_disease | TEXT | NOT NULL | Disease suggestion |
| confidence_score | DECIMAL(3,2) | NOT NULL | Score 0.00-1.00 |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

## Search Logs API Endpoints

### 1. Create Search Log

**Endpoint:** `POST /api/search-logs`

**Description:** Log a new search query

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "query": "symptoms of headache and fever",
  "results_count": 42
}
```

**Success Response:** `201 Created`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "query": "symptoms of headache and fever",
  "results_count": 42,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

**Error Responses:**
- `404 Not Found` - User does not exist
- `422 Unprocessable Entity` - Invalid input format

---

### 2. List All Search Logs

**Endpoint:** `GET /api/search-logs`

**Description:** Retrieve all search logs with pagination and filtering

**Query Parameters:**
- `skip` (integer, default: 0) - Offset for pagination
- `limit` (integer, default: 10) - Maximum results per page
- `user_id` (UUID, optional) - Filter by user

**Example Request:**
```
GET /api/search-logs?user_id=550e8400-e29b-41d4-a716-446655440000&skip=0&limit=5
```

**Success Response:** `200 OK`
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "query": "symptoms of headache and fever",
    "results_count": 42,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

---

### 3. Get Single Search Log

**Endpoint:** `GET /api/search-logs/{id}`

**Description:** Retrieve a specific search log by ID

**Path Parameters:**
- `id` (UUID, required) - Search log ID

**Success Response:** `200 OK`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "query": "symptoms of headache and fever",
  "results_count": 42,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

**Error Response:** `404 Not Found`

---

### 4. Get User Search Logs

**Endpoint:** `GET /api/search-logs/user/{user_id}`

**Description:** Retrieve all search logs for a specific user

**Path Parameters:**
- `user_id` (UUID, required) - User ID

**Query Parameters:**
- `skip` (integer, default: 0) - Offset
- `limit` (integer, default: 10) - Max results

**Success Response:** `200 OK`
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "query": "symptoms of headache and fever",
    "results_count": 42,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

**Error Response:** `404 Not Found` - User not found

---

### 5. Update Search Log

**Endpoint:** `PUT /api/search-logs/{id}`

**Description:** Update a search log (typically results_count)

**Path Parameters:**
- `id` (UUID, required) - Search log ID

**Request Body (all fields optional):**
```json
{
  "results_count": 50
}
```

**Success Response:** `200 OK`

**Error Response:** `404 Not Found`

---

### 6. Delete Search Log

**Endpoint:** `DELETE /api/search-logs/{id}`

**Description:** Delete a specific search log

**Path Parameters:**
- `id` (UUID, required) - Search log ID

**Success Response:** `204 No Content`

**Error Response:** `404 Not Found`

---

### 7. Delete User Search Logs

**Endpoint:** `DELETE /api/search-logs/user/{user_id}/all`

**Description:** Delete all search logs for a user

**Path Parameters:**
- `user_id` (UUID, required) - User ID

**Success Response:** `204 No Content`

**Error Response:** `404 Not Found` - User not found

---

## Symptom Checker API Endpoints

### 1. Create Symptom Checker Record

**Endpoint:** `POST /api/symptom-checkers`

**Description:** Create a new symptom-disease mapping

**Request Body:**
```json
{
  "symptoms": "headache, fever, cough, body ache",
  "suggested_disease": "Common Cold or Influenza",
  "confidence_score": 0.85
}
```

**Success Response:** `201 Created`
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440002",
  "symptoms": "headache, fever, cough, body ache",
  "suggested_disease": "Common Cold or Influenza",
  "confidence_score": 0.85,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

**Error Responses:**
- `422 Unprocessable Entity` - Confidence score not between 0.00-1.00

---

### 2. List All Symptom Checkers

**Endpoint:** `GET /api/symptom-checkers`

**Description:** Retrieve all symptom checker records with optional filtering

**Query Parameters:**
- `skip` (integer, default: 0) - Offset
- `limit` (integer, default: 10) - Max results
- `min_confidence` (float, optional) - Minimum confidence threshold

**Example Request:**
```
GET /api/symptom-checkers?min_confidence=0.75&skip=0&limit=10
```

**Success Response:** `200 OK`
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "symptoms": "headache, fever, cough, body ache",
    "suggested_disease": "Common Cold or Influenza",
    "confidence_score": 0.85,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

---

### 3. Get Single Symptom Checker

**Endpoint:** `GET /api/symptom-checkers/{id}`

**Description:** Retrieve a specific symptom checker record

**Path Parameters:**
- `id` (UUID, required) - Record ID

**Success Response:** `200 OK`

**Error Response:** `404 Not Found`

---

### 4. Search by Symptoms

**Endpoint:** `GET /api/symptom-checkers/search/by-symptoms`

**Description:** Search symptom checker records by symptoms (case-insensitive partial match)

**Query Parameters:**
- `symptoms` (string, required) - Symptom to search for
- `skip` (integer, default: 0) - Offset
- `limit` (integer, default: 10) - Max results

**Example Request:**
```
GET /api/symptom-checkers/search/by-symptoms?symptoms=headache&skip=0&limit=10
```

**Success Response:** `200 OK`
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "symptoms": "headache, fever, cough, body ache",
    "suggested_disease": "Common Cold or Influenza",
    "confidence_score": 0.85,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

---

### 5. Search by Disease

**Endpoint:** `GET /api/symptom-checkers/search/by-disease`

**Description:** Search symptom checker records by disease name (case-insensitive partial match)

**Query Parameters:**
- `disease` (string, required) - Disease to search for
- `skip` (integer, default: 0) - Offset
- `limit` (integer, default: 10) - Max results

**Example Request:**
```
GET /api/symptom-checkers/search/by-disease?disease=influenza&skip=0&limit=10
```

**Success Response:** `200 OK`

---

### 6. Update Symptom Checker

**Endpoint:** `PUT /api/symptom-checkers/{id}`

**Description:** Update a symptom checker record

**Path Parameters:**
- `id` (UUID, required) - Record ID

**Request Body (all fields optional):**
```json
{
  "symptoms": "updated symptoms",
  "suggested_disease": "updated disease",
  "confidence_score": 0.90
}
```

**Success Response:** `200 OK`

**Error Responses:**
- `404 Not Found` - Record not found
- `422 Unprocessable Entity` - Invalid confidence score

---

### 7. Delete Symptom Checker

**Endpoint:** `DELETE /api/symptom-checkers/{id}`

**Description:** Delete a symptom checker record

**Path Parameters:**
- `id` (UUID, required) - Record ID

**Success Response:** `204 No Content`

**Error Response:** `404 Not Found`

---

## Request/Response Examples

### Search Logs Workflow

```bash
# 1. Create search log
curl -X POST http://localhost:8000/api/search-logs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "query": "diabetes symptoms",
    "results_count": 150
  }'

# 2. Get user's search history
curl http://localhost:8000/api/search-logs/user/550e8400-e29b-41d4-a716-446655440000

# 3. Update results count
curl -X PUT http://localhost:8000/api/search-logs/{id} \
  -H "Content-Type: application/json" \
  -d '{"results_count": 155}'
```

### Symptom Checker Workflow

```bash
# 1. Create symptom-disease mapping
curl -X POST http://localhost:8000/api/symptom-checkers \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "chest pain, shortness of breath",
    "suggested_disease": "Heart attack or Angina",
    "confidence_score": 0.92
  }'

# 2. Search by symptoms
curl "http://localhost:8000/api/symptom-checkers/search/by-symptoms?symptoms=chest+pain"

# 3. Filter by confidence
curl "http://localhost:8000/api/symptom-checkers?min_confidence=0.80"
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| 200 | OK | GET, PUT successful |
| 201 | Created | POST successful |
| 204 | No Content | DELETE successful |
| 404 | Not Found | Resource doesn't exist |
| 422 | Invalid Data | Validation failed (confidence score range) |

---

## Field Validation

### Search Logs

**query:**
- Type: Text
- Required: Yes
- No length limit

**results_count:**
- Type: Integer
- Default: 0
- Min/Max: 0 to any positive integer

**user_id:**
- Type: UUID
- Required: Yes (at creation)
- Must reference existing user

### Symptom Checker

**symptoms:**
- Type: Text
- Required: Yes
- Format: Comma-separated or description
- Examples: "headache, fever", "chest pain and shortness of breath"

**suggested_disease:**
- Type: Text
- Required: Yes
- Examples: "Common Cold", "Influenza", "Pneumonia"

**confidence_score:**
- Type: Decimal (0.00 to 1.00)
- Required: Yes
- Constraint: Must be between 0.00 and 1.00
- Precision: 2 decimal places

---

## Integration Points

### Search Logs Integration
- Track search patterns across your platform
- Analyze user search behavior for UX improvements
- Support analytics and reporting features
- Feed search data into recommendation engines

### Symptom Checker Integration
- Support clinical decision-making workflows
- Educational resources about symptom-disease relationships
- Integration with medical reference systems
- Pre-consultation patient self-assessment
- Training data for medical AI/ML models

---

## Performance Considerations

1. **Pagination:** Always use limit parameter for large datasets
2. **Filtering:** Search endpoints use LIKE queries - add indexes as needed
3. **Confidence Filtering:** min_confidence parameter efficiently filters results
4. **Bulk Operations:** Delete user search logs clears all records efficiently

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | April 2026 | Initial implementation (7 search log endpoints, 7 symptom checker endpoints) |

---

**End of Search Logs & Symptom Checker APIs Specification**
