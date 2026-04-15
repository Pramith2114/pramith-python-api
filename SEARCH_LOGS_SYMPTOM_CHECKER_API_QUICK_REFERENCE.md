# Search Logs & Symptom Checker APIs - Quick Reference

**Version:** 1.0 | **Status:** Production Ready | **Last Updated:** April 2026

---

## Endpoint Summary

### Search Logs API

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **POST** | `/api/search-logs` | Create search log |
| **GET** | `/api/search-logs` | List all logs (filterable by user_id) |
| **GET** | `/api/search-logs/{id}` | Get single log |
| **GET** | `/api/search-logs/user/{user_id}` | Get user's search logs |
| **PUT** | `/api/search-logs/{id}` | Update search log |
| **DELETE** | `/api/search-logs/{id}` | Delete search log |
| **DELETE** | `/api/search-logs/user/{user_id}/all` | Delete all user logs |

### Symptom Checker API

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **POST** | `/api/symptom-checkers` | Create symptom-disease mapping |
| **GET** | `/api/symptom-checkers` | List all (filterable by min_confidence) |
| **GET** | `/api/symptom-checkers/{id}` | Get single record |
| **GET** | `/api/symptom-checkers/search/by-symptoms` | Search by symptoms |
| **GET** | `/api/symptom-checkers/search/by-disease` | Search by disease |
| **PUT** | `/api/symptom-checkers/{id}` | Update record |
| **DELETE** | `/api/symptom-checkers/{id}` | Delete record |

---

## cURL Examples

### Search Logs

```bash
# Create search log
curl -X POST http://localhost:8000/api/search-logs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "query": "symptoms of diabetes",
    "results_count": 120
  }'

# List all logs
curl http://localhost:8000/api/search-logs?skip=0&limit=10

# Get user's search logs
curl http://localhost:8000/api/search-logs/user/550e8400-e29b-41d4-a716-446655440000

# Update search log
curl -X PUT http://localhost:8000/api/search-logs/{id} \
  -H "Content-Type: application/json" \
  -d '{"results_count": 125}'

# Delete search log
curl -X DELETE http://localhost:8000/api/search-logs/{id}

# Delete all user logs
curl -X DELETE http://localhost:8000/api/search-logs/user/{user_id}/all
```

### Symptom Checker

```bash
# Create symptom checker entry
curl -X POST http://localhost:8000/api/symptom-checkers \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": "cough, fever, body ache",
    "suggested_disease": "Common Cold or Flu",
    "confidence_score": 0.88
  }'

# List all records
curl http://localhost:8000/api/symptom-checkers?skip=0&limit=10

# Filter by confidence
curl "http://localhost:8000/api/symptom-checkers?min_confidence=0.80"

# Search by symptoms
curl "http://localhost:8000/api/symptom-checkers/search/by-symptoms?symptoms=cough&limit=10"

# Search by disease
curl "http://localhost:8000/api/symptom-checkers/search/by-disease?disease=influenza&limit=10"

# Update record
curl -X PUT http://localhost:8000/api/symptom-checkers/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "confidence_score": 0.92
  }'

# Delete record
curl -X DELETE http://localhost:8000/api/symptom-checkers/{id}
```

---

## Python Examples

### Search Logs

```python
import httpx

client = httpx.Client()

# Create search log
response = client.post(
    "http://localhost:8000/api/search-logs",
    json={
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "query": "hypertension treatment",
        "results_count": 85
    }
)
log = response.json()
print(f"Created log: {log['id']}")

# Get user's search history
response = client.get(
    "http://localhost:8000/api/search-logs/user/550e8400-e29b-41d4-a716-446655440000"
)
logs = response.json()
print(f"User has {len(logs)} search logs")
```

### Symptom Checker

```python
# Create mapping
response = client.post(
    "http://localhost:8000/api/symptom-checkers",
    json={
        "symptoms": "persistent cough, chest pain",
        "suggested_disease": "Bronchitis or Pneumonia",
        "confidence_score": 0.82
    }
)
record = response.json()

# Search by symptoms
response = client.get(
    "http://localhost:8000/api/symptom-checkers/search/by-symptoms",
    params={"symptoms": "cough", "limit": 10}
)
results = response.json()
print(f"Found {len(results)} records with 'cough'")

# Filter high confidence
response = client.get(
    "http://localhost:8000/api/symptom-checkers",
    params={"min_confidence": 0.85, "limit": 20}
)
high_confidence = response.json()
```

---

## JavaScript Examples

### Search Logs

```javascript
// Create search log
const createSearchLog = async (userId, query) => {
  const response = await fetch('http://localhost:8000/api/search-logs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      query: query,
      results_count: 0
    })
  });
  return await response.json();
};

// Get user's logs
const getUserLogs = async (userId) => {
  const response = await fetch(
    `http://localhost:8000/api/search-logs/user/${userId}`
  );
  return await response.json();
};

// Update log results
const updateLogResults = async (logId, count) => {
  const response = await fetch(
    `http://localhost:8000/api/search-logs/${logId}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ results_count: count })
    }
  );
  return await response.json();
};
```

### Symptom Checker

```javascript
// Create mapping
const createSymptomMapping = async (symptoms, disease, confidence) => {
  const response = await fetch('http://localhost:8000/api/symptom-checkers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      symptoms: symptoms,
      suggested_disease: disease,
      confidence_score: confidence
    })
  });
  return await response.json();
};

// Search symptoms
const searchBySymptoms = async (symptom) => {
  const response = await fetch(
    `http://localhost:8000/api/symptom-checkers/search/by-symptoms?symptoms=${encodeURIComponent(symptom)}`
  );
  return await response.json();
};

// Get high confidence records
const getHighConfidence = async (threshold = 0.80) => {
  const response = await fetch(
    `http://localhost:8000/api/symptom-checkers?min_confidence=${threshold}&limit=100`
  );
  return await response.json();
};
```

---

## Response Schemas

### Search Log Object

```json
{
  "id": "UUID",
  "user_id": "UUID",
  "query": "String (any length)",
  "results_count": 0,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

### Symptom Checker Object

```json
{
  "id": "UUID",
  "symptoms": "String (comma-separated or description)",
  "suggested_disease": "String",
  "confidence_score": 0.85,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| **200** | OK - GET or PUT successful |
| **201** | Created - POST successful |
| **204** | No Content - DELETE successful |
| **404** | Not Found - Resource doesn't exist |
| **422** | Invalid Data - Validation error |

---

## Query Parameters

### Search Logs
- `skip` (default: 0) - Pagination offset
- `limit` (default: 10) - Results per page
- `user_id` - Filter by user

### Symptom Checker
- `skip` (default: 0) - Pagination offset
- `limit` (default: 10) - Results per page
- `min_confidence` - Minimum confidence (0.00-1.00)
- `symptoms` (search endpoint) - Symptom keyword
- `disease` (search endpoint) - Disease keyword

---

## Common Use Cases

### Analytics: User Search Patterns
```
POST /api/search-logs → stores every search
GET /api/search-logs/user/{id} → analyze user searches
```

### Medical: Symptom Diagnosis
```
GET /api/symptom-checkers/search/by-symptoms?symptoms=headache
GET /api/symptom-checkers?min_confidence=0.85
```

### Decision Support: High-Confidence Suggestions
```
GET /api/symptom-checkers?min_confidence=0.90
→ Returns only high-confidence disease mappings for clinical use
```

### Training Data: Symptom Database
```
GET /api/symptom-checkers?limit=1000
→ Extract all symptom-disease relationships for training
```

---

## Validation Rules

### Search Log Creation
- user_id: Must reference valid user
- query: Text required, no max length
- results_count: Integer, 0+

### Symptom Checker Creation
- symptoms: Text required (comma-separated or prose)
- suggested_disease: Text required
- confidence_score: Decimal 0.00 to 1.00 required

---

## Integration Checklist

**Search Logs:**
- [ ] Log all user searches for analytics
- [ ] Track popular search queries
- [ ] Monitor search performance (results count)
- [ ] Implement search history view in UI
- [ ] Feed data into recommendation engine

**Symptom Checker:**
- [ ] Build clinical decision support tool
- [ ] Create patient self-assessment questionnaire
- [ ] Provide symptom-to-disease mapping
- [ ] Filter results by confidence threshold
- [ ] Support medical education platform

---

## Performance Tips

1. Use pagination with `limit` parameter
2. Filter by `min_confidence` to reduce large result sets
3. Search endpoints use LIKE queries - consider indexing strategies
4. Archive old search logs periodically
5. Cache high-confidence symptom records

---

**Quick Reference Complete**
