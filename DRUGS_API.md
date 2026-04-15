# 💊 Drugs API - Complete Reference

## Overview

The **Drugs/Medicine Management API** enables efficient management of pharmaceutical inventory including drug details, pricing, stock management, and expiry tracking. Perfect for pharmacies, hospitals, and healthcare providers.

## Database Table Structure

```sql
CREATE TABLE drugs (
  id UUID PRIMARY KEY,
  name VARCHAR,
  generic_name VARCHAR,
  manufacturer VARCHAR,
  price DECIMAL,
  stock_quantity INT,
  expiry_date DATE
);
```

## API Endpoints Summary

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|------------|
| **POST** | `/api/drugs` | Create new drug | 201 |
| **GET** | `/api/drugs` | List all drugs (paginated, filterable) | 200 |
| **GET** | `/api/drugs/{drug_id}` | Get specific drug | 200 |
| **PUT** | `/api/drugs/{drug_id}` | Update drug | 200 |
| **DELETE** | `/api/drugs/{drug_id}` | Delete drug | 204 |

---

## Detailed Endpoints

### 1. Create Drug

**Endpoint:** `POST /api/drugs`

**Description:** Create a new drug/medicine record in the pharmacy inventory.

**Request Body:**
```json
{
  "name": "Aspirin 500mg",
  "generic_name": "Acetylsalicylic acid",
  "manufacturer": "Bayer",
  "price": 5.99,
  "stock_quantity": 100,
  "expiry_date": "2026-12-31"
}
```

**Fields:**
- `name` (string, required): Brand name of the drug
- `generic_name` (string, required): Generic/chemical name
- `manufacturer` (string, required): Drug manufacturer
- `price` (decimal, required): Price per unit (must be positive)
- `stock_quantity` (integer, required): Available quantity (non-negative)
- `expiry_date` (date, required): Expiry date in YYYY-MM-DD format

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Aspirin 500mg",
  "generic_name": "Acetylsalicylic acid",
  "manufacturer": "Bayer",
  "price": 5.99,
  "stock_quantity": 100,
  "expiry_date": "2026-12-31",
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T10:30:00"
}
```

**Error Responses:**
- `422 Unprocessable Entity` - Validation error (invalid price, negative stock, bad date format)

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/drugs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin 500mg",
    "generic_name": "Acetylsalicylic acid",
    "manufacturer": "Bayer",
    "price": 5.99,
    "stock_quantity": 100,
    "expiry_date": "2026-12-31"
  }'
```

**Python Example:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/drugs",
    json={
        "name": "Aspirin 500mg",
        "generic_name": "Acetylsalicylic acid",
        "manufacturer": "Bayer",
        "price": 5.99,
        "stock_quantity": 100,
        "expiry_date": "2026-12-31"
    }
)
drug = response.json()
print(f"Drug created: {drug['id']}")
```

---

### 2. Get All Drugs

**Endpoint:** `GET /api/drugs`

**Description:** Retrieve all drugs from inventory with optional pagination and filtering.

**Query Parameters:**
- `skip` (integer, default: 0): Number of drugs to skip
- `limit` (integer, default: 10): Maximum drugs to return
- `name` (string, optional): Filter by drug name (partial match, case-insensitive)
- `manufacturer` (string, optional): Filter by manufacturer (case-insensitive)

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Aspirin 500mg",
    "generic_name": "Acetylsalicylic acid",
    "manufacturer": "Bayer",
    "price": 5.99,
    "stock_quantity": 100,
    "expiry_date": "2026-12-31",
    "created_at": "2024-04-14T10:30:00",
    "updated_at": "2024-04-14T10:30:00"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "Paracetamol 650mg",
    "generic_name": "Paracetamol",
    "manufacturer": "GlaxoSmithKline",
    "price": 3.49,
    "stock_quantity": 200,
    "expiry_date": "2025-06-30",
    "created_at": "2024-04-14T10:35:00",
    "updated_at": "2024-04-14T10:35:00"
  }
]
```

**cURL Examples:**

Get first 10 drugs:
```bash
curl http://localhost:8000/api/drugs
```

Get drugs by manufacturer:
```bash
curl "http://localhost:8000/api/drugs?manufacturer=Bayer"
```

Search by name:
```bash
curl "http://localhost:8000/api/drugs?name=Aspirin"
```

Pagination (get next page):
```bash
curl "http://localhost:8000/api/drugs?skip=10&limit=10"
```

Multiple filters:
```bash
curl "http://localhost:8000/api/drugs?name=pain&manufacturer=Bayer&limit=5"
```

---

### 3. Get Specific Drug

**Endpoint:** `GET /api/drugs/{drug_id}`

**Description:** Retrieve a specific drug by UUID.

**Path Parameters:**
- `drug_id` (UUID, required): UUID of the drug

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Aspirin 500mg",
  "generic_name": "Acetylsalicylic acid",
  "manufacturer": "Bayer",
  "price": 5.99,
  "stock_quantity": 100,
  "expiry_date": "2026-12-31",
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T10:30:00"
}
```

**Error Responses:**
- `404 Not Found` - If drug doesn't exist

**cURL Example:**
```bash
curl http://localhost:8000/api/drugs/550e8400-e29b-41d4-a716-446655440000
```

---

### 4. Update Drug

**Endpoint:** `PUT /api/drugs/{drug_id}`

**Description:** Update drug information.

**Path Parameters:**
- `drug_id` (UUID, required): UUID of the drug

**Request Body** (all fields optional):
```json
{
  "name": "Aspirin 500mg (Updated)",
  "generic_name": "Acetylsalicylic acid",
  "manufacturer": "Bayer",
  "price": 6.49,
  "stock_quantity": 150,
  "expiry_date": "2027-12-31"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Aspirin 500mg (Updated)",
  "generic_name": "Acetylsalicylic acid",
  "manufacturer": "Bayer",
  "price": 6.49,
  "stock_quantity": 150,
  "expiry_date": "2027-12-31",
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T12:00:00"
}
```

**Error Responses:**
- `404 Not Found` - If drug doesn't exist
- `422 Unprocessable Entity` - Validation error

**cURL Example:**
```bash
curl -X PUT http://localhost:8000/api/drugs/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 6.49,
    "stock_quantity": 150
  }'
```

**Python Example:**
```python
import requests

response = requests.put(
    "http://localhost:8000/api/drugs/550e8400-e29b-41d4-a716-446655440000",
    json={
        "stock_quantity": 150,
        "price": 6.49
    }
)
print(response.json())
```

---

### 5. Delete Drug

**Endpoint:** `DELETE /api/drugs/{drug_id}`

**Description:** Delete a drug record by ID.

**Path Parameters:**
- `drug_id` (UUID, required): UUID of the drug

**Response (204 No Content)**

**Error Responses:**
- `404 Not Found` - If drug doesn't exist

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/drugs/550e8400-e29b-41d4-a716-446655440000
```

---

## Data Models

### DrugBase (Request/Response Base)
```python
{
    "name": str,                 # required
    "generic_name": str,         # required
    "manufacturer": str,         # required
    "price": float,              # required, > 0
    "stock_quantity": int,       # required, >= 0
    "expiry_date": str          # required, YYYY-MM-DD
}
```

### DrugCreate (Request)
Inherits from `DrugBase` - all fields required

### DrugUpdate (Request)
```python
{
    "name": str (optional),
    "generic_name": str (optional),
    "manufacturer": str (optional),
    "price": float (optional, > 0),
    "stock_quantity": int (optional, >= 0),
    "expiry_date": str (optional)
}
```

### DrugResponse (Response)
```python
{
    "id": str (UUID),
    "name": str,
    "generic_name": str,
    "manufacturer": str,
    "price": float,
    "stock_quantity": int,
    "expiry_date": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

---

## Common Workflows

### Workflow 1: Add New Drug to Inventory
```bash
# 1. Create drug record
DRUG_ID=$(curl -s -X POST http://localhost:8000/api/drugs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin 500mg",
    "generic_name": "Acetylsalicylic acid",
    "manufacturer": "Bayer",
    "price": 5.99,
    "stock_quantity": 100,
    "expiry_date": "2026-12-31"
  }' | jq -r '.id')

echo "Drug created: $DRUG_ID"

# 2. Verify creation
curl http://localhost:8000/api/drugs/$DRUG_ID
```

### Workflow 2: Update Stock Quantity
```bash
# Pharmacy received new shipment
curl -X PUT http://localhost:8000/api/drugs/{drug_id} \
  -H "Content-Type: application/json" \
  -d '{
    "stock_quantity": 250
  }'
```

### Workflow 3: Search Drug by Manufacturer
```bash
curl "http://localhost:8000/api/drugs?manufacturer=Bayer"
```

### Workflow 4: Update Price
```bash
curl -X PUT http://localhost:8000/api/drugs/{drug_id} \
  -H "Content-Type: application/json" \
  -d '{
    "price": 6.49
  }'
```

### Workflow 5: List Low Stock Drugs
```bash
# Get all drugs (you'll need to filter on client side for stock < threshold)
curl "http://localhost:8000/api/drugs?limit=100"
```

---

## Validation Rules

| Field | Rules |
|-------|-------|
| `name` | Required, string, max 255 chars |
| `generic_name` | Required, string, max 255 chars |
| `manufacturer` | Required, string, max 255 chars |
| `price` | Required, decimal, must be > 0 |
| `stock_quantity` | Required, integer, must be >= 0 |
| `expiry_date` | Required, date format YYYY-MM-DD |

---

## Filter Operators

### Name Filter
- Case-insensitive partial string match
- Example: `?name=aspirin` matches "ASPIRIN", "Aspirin 500mg", "aspirin plus"

### Manufacturer Filter
- Case-insensitive partial string match
- Example: `?manufacturer=Bayer` matches "Bayer", "BAYER Inc", "Bayer Healthcare"

---

## Pagination

### Get Page 1 (10 items)
```bash
curl "http://localhost:8000/api/drugs?skip=0&limit=10"
```

### Get Page 2 (items 11-20)
```bash
curl "http://localhost:8000/api/drugs?skip=10&limit=10"
```

### Get Page 3 (items 21-30)
```bash
curl "http://localhost:8000/api/drugs?skip=20&limit=30"
```

---

## Database Schema Details

```sql
CREATE TABLE drugs (
  id UUID NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  generic_name VARCHAR(255) NOT NULL,
  manufacturer VARCHAR(255) NOT NULL,
  price NUMERIC(10, 2) NOT NULL,
  stock_quantity INTEGER NOT NULL DEFAULT 0,
  expiry_date DATE NOT NULL,
  created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_generic_name (generic_name),
  INDEX idx_manufacturer (manufacturer)
);
```

### Fields Explanation

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | UUID | Primary Key | Auto-generated |
| `name` | VARCHAR(255) | NOT NULL | Brand name |
| `generic_name` | VARCHAR(255) | NOT NULL | Chemical name |
| `manufacturer` | VARCHAR(255) | NOT NULL | Manufacturer name |
| `price` | NUMERIC(10,2) | NOT NULL, > 0 | Price per unit |
| `stock_quantity` | INTEGER | NOT NULL, >= 0 | Available units |
| `expiry_date` | DATE | NOT NULL | Expiry date |
| `created_at` | TIMESTAMP | Auto | Creation time |
| `updated_at` | TIMESTAMP | Auto | Last update time |

---

## Status Codes

| Code | Meaning |
|------|---------|
| **201** | Created successfully |
| **200** | Request successful |
| **204** | Deleted (no content) |
| **404** | Drug not found |
| **422** | Validation error |
| **500** | Server error |

---

## Error Handling

### 404 Not Found
```json
{
  "detail": "Drug not found"
}
```

### 422 Validation Error (Negative Price)
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

### 422 Validation Error (Invalid Date)
```json
{
  "detail": [
    {
      "loc": ["body", "expiry_date"],
      "msg": "invalid date format",
      "type": "value_error.date"
    }
  ]
}
```

---

## Interactive Testing

Visit http://localhost:8000/docs for interactive Swagger UI where you can:
- Test all endpoints
- View request/response schemas
- See live examples
- Auto-generate API client code

---

## Best Practices

1. **Price Format**: Always use decimal format with 2 decimal places (e.g., 5.99, not 5.9)
2. **Stock Tracking**: Keep stock_quantity updated to avoid overselling
3. **Expiry Dates**: Monitor expiry dates and remove expired drugs
4. **Naming Convention**: Use consistent naming (e.g., "Drug Name 500mg" format)
5. **Manufacturer Info**: Keep manufacturer consistent for inventory tracking

---

## Integration Notes

- **No Authentication Required**: Add authentication as needed
- **No Role-Based Access**: Add role checking if needed
- **Auto Timestamps**: `created_at` and `updated_at` are automatic
- **UUID Format**: All IDs are UUID v4

---

## Rate Limiting

Currently no rate limiting. Consider implementing if needed for production.

---

## Future Enhancements

- Add batch/lot number tracking
- Add drug category/classification
- Add supplier information
- Add drug interactions/contraindications
- Add prescription requirements
- Add sales tracking

