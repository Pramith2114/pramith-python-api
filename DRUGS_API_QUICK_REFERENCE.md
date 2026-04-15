# ⚡ Drugs API - Quick Reference

## Quick Endpoint Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/drugs` | Create drug |
| GET | `/api/drugs` | List drugs |
| GET | `/api/drugs/{id}` | Get specific drug |
| PUT | `/api/drugs/{id}` | Update drug |
| DELETE | `/api/drugs/{id}` | Delete drug |

---

## Quick Examples

### 1. Create Drug
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

### 2. Get All Drugs
```bash
curl http://localhost:8000/api/drugs
```

### 3. Search by Manufacturer
```bash
curl "http://localhost:8000/api/drugs?manufacturer=Bayer"
```

### 4. Search by Name
```bash
curl "http://localhost:8000/api/drugs?name=aspirin"
```

### 5. Get Specific Drug
```bash
curl http://localhost:8000/api/drugs/{drug_id}
```

### 6. Update Drug
```bash
curl -X PUT http://localhost:8000/api/drugs/{drug_id} \
  -H "Content-Type: application/json" \
  -d '{
    "stock_quantity": 150,
    "price": 6.49
  }'
```

### 7. Update Stock Only
```bash
curl -X PUT http://localhost:8000/api/drugs/{drug_id} \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 200}'
```

### 8. Delete Drug
```bash
curl -X DELETE http://localhost:8000/api/drugs/{drug_id}
```

---

## Python Examples

### Create Drug
```python
import requests

response = requests.post(
    "http://localhost:8000/api/drugs",
    json={
        "name": "Paracetamol 650mg",
        "generic_name": "Paracetamol",
        "manufacturer": "GlaxoSmithKline",
        "price": 3.49,
        "stock_quantity": 200,
        "expiry_date": "2025-06-30"
    }
)
drug = response.json()
print(f"Drug ID: {drug['id']}")
```

### Get All Drugs
```python
response = requests.get("http://localhost:8000/api/drugs")
drugs = response.json()
for drug in drugs:
    print(f"{drug['name']} - Stock: {drug['stock_quantity']}")
```

### Search Drugs
```python
response = requests.get(
    "http://localhost:8000/api/drugs",
    params={"manufacturer": "Bayer"}
)
drugs = response.json()
print(f"Found {len(drugs)} drugs from Bayer")
```

### Update Drug Stock
```python
drug_id = "550e8400-e29b-41d4-a716-446655440000"
response = requests.put(
    f"http://localhost:8000/api/drugs/{drug_id}",
    json={"stock_quantity": 300}
)
print(response.json())
```

---

## Request/Response Fields

### Create/Update Request
```json
{
  "name": "string",              // required
  "generic_name": "string",      // required
  "manufacturer": "string",      // required
  "price": 5.99,                 // required, > 0
  "stock_quantity": 100,         // required, >= 0
  "expiry_date": "2026-12-31"   // required, YYYY-MM-DD
}
```

### Response
```json
{
  "id": "UUID",
  "name": "string",
  "generic_name": "string",
  "manufacturer": "string",
  "price": 5.99,
  "stock_quantity": 100,
  "expiry_date": "2026-12-31",
  "created_at": "2024-04-14T10:30:00",
  "updated_at": "2024-04-14T10:30:00"
}
```

---

## Query Parameters

### Pagination
```
?skip=0          # Skip first N drugs
&limit=10        # Return max N drugs
```

### Filtering
```
?name=aspirin           # Search by name (case-insensitive)
?manufacturer=Bayer     # Filter by manufacturer
?name=pain&manufacturer=Bayer  # Multiple filters
```

---

## Common Filters

### By Manufacturer
```bash
curl "http://localhost:8000/api/drugs?manufacturer=Bayer"
```

### By Drug Name
```bash
curl "http://localhost:8000/api/drugs?name=aspirin"
```

### Pagination
```bash
curl "http://localhost:8000/api/drugs?skip=0&limit=20"
```

### Combination
```bash
curl "http://localhost:8000/api/drugs?name=pain&manufacturer=GSK&limit=5"
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 201 | Created |
| 200 | OK |
| 204 | Deleted |
| 404 | Not Found |
| 422 | Validation Error |

---

## Database Schema

```
drugs Table:
┌─────────┬──────────────────┬────────────────┬──────────┬───────────┐
│ id      │ name             │ generic_name   │ price    │ stock_qty │
│ (UUID)  │ (String)         │ (String)       │ (Decimal)│ (Integer) │
├─────────┼──────────────────┼────────────────┼──────────┼───────────┤
│ 550e... │ Aspirin 500mg    │ Acetylsalicyli │ 5.99     │ 100       │
│ 660e... │ Paracetamol 650m │ Paracetamol    │ 3.49     │ 200       │
│ 770e... │ Ibuprofen 400mg  │ Ibuprofen      │ 4.99     │ 150       │
└─────────┴──────────────────┴────────────────┴──────────┴───────────┘
```

---

## Tips

1. **Date Format**: Always use YYYY-MM-DD for expiry_date
2. **Price**: Must be positive decimal (e.g., 5.99, not -5.99)
3. **Stock**: Must be non-negative (0-9999+)
4. **Partial Search**: Name/manufacturer search is partial and case-insensitive
5. **Pagination**: Default limit is 10, max recommended is 100

---

## Error Examples

### Price Too Low
```bash
curl -X POST http://localhost:8000/api/drugs \
  -H "Content-Type: application/json" \
  -d '{"name": "Drug", "price": -5}'
# Returns 422 - price must be > 0
```

### Drug Not Found
```bash
curl http://localhost:8000/api/drugs/invalid-id
# Returns 404 - Drug not found
```

### Missing Required Field
```bash
curl -X POST http://localhost:8000/api/drugs \
  -H "Content-Type: application/json" \
  -d '{"name": "Drug"}'
# Returns 422 - Missing required fields
```

---

## Common Workflows

### Add New Drug + Check Stock
```bash
# Create
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

# Get details
curl http://localhost:8000/api/drugs/$DRUG_ID
```

### Search + Update
```bash
# Find Bayer drugs
curl "http://localhost:8000/api/drugs?manufacturer=Bayer" | jq '.[] | select(.id == "YOUR_ID")'

# Update price
curl -X PUT http://localhost:8000/api/drugs/YOUR_ID \
  -H "Content-Type: application/json" \
  -d '{"price": 6.49}'
```

### Inventory Management
```bash
# Get low stock (you filter on client)
curl "http://localhost:8000/api/drugs?limit=100" | \
  jq '.[] | select(.stock_quantity < 50)'

# Update stock after receiving shipment
curl -X PUT http://localhost:8000/api/drugs/DRUG_ID \
  -H "Content-Type: application/json" \
  -d '{"stock_quantity": 300}'
```

---

## Validation Rules

| Field | Rules |
|-------|-------|
| name | max 255 chars, required |
| generic_name | max 255 chars, required |
| manufacturer | max 255 chars, required |
| price | must be > 0 |
| stock_quantity | must be >= 0 |
| expiry_date | YYYY-MM-DD format |

---

## Interactive API Docs

Visit http://localhost:8000/docs to test endpoints interactively.

