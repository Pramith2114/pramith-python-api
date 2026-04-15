# 📚 Invoices API - Quick Reference

## Quick Lookup Guide

### Endpoints at a Glance

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/invoices` | Create invoice |
| GET | `/api/invoices` | List all invoices (filterable) |
| GET | `/api/invoices/{id}` | Get invoice with items |
| GET | `/api/invoices/user/{id}` | Get user's invoices |
| PUT | `/api/invoices/{id}` | Update invoice |
| DELETE | `/api/invoices/{id}` | Delete invoice |
| POST | `/api/invoice-items` | Create item |
| GET | `/api/invoice-items` | List all items (filterable) |
| GET | `/api/invoice-items/{id}` | Get single item |
| GET | `/api/invoice-items/invoice/{id}` | Get invoice items |
| PUT | `/api/invoice-items/{id}` | Update item |
| DELETE | `/api/invoice-items/{id}` | Delete item |

---

## Quick Examples

### Create Invoice
```bash
curl -X POST http://localhost:8000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "770e8400-e29b-41d4-a716-446655440222",
    "total_amount": 1250.75
  }'
```

**Response (201 Created):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "user_id": "770e8400-e29b-41d4-a716-446655440222",
  "total_amount": 1250.75,
  "status": "draft",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

---

### Add Item to Invoice
```bash
curl -X POST http://localhost:8000/api/invoice-items \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": "aa0e8400-e29b-41d4-a716-446655440555",
    "item_type": "drug",
    "item_id": "cc0e8400-e29b-41d4-a716-446655440777",
    "quantity": 2,
    "price": 250.00
  }'
```

---

### Get Invoice with All Items
```bash
curl http://localhost:8000/api/invoices/aa0e8400-e29b-41d4-a716-446655440555
```

---

### Get All Invoices
```bash
curl http://localhost:8000/api/invoices
```

---

### Filter Invoices

#### By User
```bash
curl "http://localhost:8000/api/invoices?user_id=770e8400-e29b-41d4-a716-446655440222"
```

#### By Status
```bash
curl "http://localhost:8000/api/invoices?status_filter=paid"
```

#### By User AND Status
```bash
curl "http://localhost:8000/api/invoices?user_id=xxx&status_filter=issued"
```

---

### Get User's Invoices
```bash
curl "http://localhost:8000/api/invoices/user/770e8400-e29b-41d4-a716-446655440222"
```

**With Status Filter:**
```bash
curl "http://localhost:8000/api/invoices/user/xxx?status_filter=paid"
```

---

### Get Invoice Items

#### All Items
```bash
curl http://localhost:8000/api/invoice-items
```

#### By Invoice
```bash
curl "http://localhost:8000/api/invoice-items/invoice/aa0e8400-e29b-41d4-a716-446655440555"
```

#### By Item Type
```bash
curl "http://localhost:8000/api/invoice-items?item_type=drug"
```

---

### Update Invoice Status
```bash
curl -X PUT http://localhost:8000/api/invoices/aa0e8400-e29b-41d4-a716-446655440555 \
  -H "Content-Type: application/json" \
  -d '{"status": "issued"}'
```

---

### Update Invoice Item
```bash
curl -X PUT http://localhost:8000/api/invoice-items/bb0e8400-e29b-41d4-a716-446655440666 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 3,
    "price": 275.00
  }'
```

---

### Delete Invoice
```bash
curl -X DELETE http://localhost:8000/api/invoices/aa0e8400-e29b-41d4-a716-446655440555
```

**Response:** `204 No Content`

---

### Delete Invoice Item
```bash
curl -X DELETE http://localhost:8000/api/invoice-items/bb0e8400-e29b-41d4-a716-446655440666
```

---

## Response Schemas

### Invoice Object
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "total_amount": "decimal",
  "status": "string",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

### Invoice with Items
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "total_amount": "decimal",
  "status": "string",
  "items": [
    {
      "id": "uuid",
      "invoice_id": "uuid",
      "item_type": "string",
      "item_id": "uuid",
      "quantity": "integer",
      "price": "decimal",
      "created_at": "ISO 8601 timestamp",
      "updated_at": "ISO 8601 timestamp"
    }
  ],
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

### Invoice Item Object
```json
{
  "id": "uuid",
  "invoice_id": "uuid",
  "item_type": "string",
  "item_id": "uuid",
  "quantity": "integer",
  "price": "decimal",
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

## Invoice Status Values

```
• draft              Being prepared
• issued             Sent to customer
• paid               Payment received
• overdue            Payment overdue
• cancelled          Invoice cancelled
```

---

## Item Types

```
• drug               Drug/medication
• consultation       Doctor consultation
• service            Medical service
• lab_test           Laboratory test
• procedure          Surgical/medical procedure
• other              Other items
```

---

## Query Parameters

### List & Filter Query Parameters
- `skip` (int) - Records to skip (default: 0)
- `limit` (int) - Max records to return (default: 10)
- `user_id` (UUID) - Filter by user
- `status_filter` (string) - Filter by status
- `item_type` (string) - Filter items by type

### Example Combinations
```bash
# Skip 20, return 5
?skip=20&limit=5

# User's paid invoices
?user_id=xxx&status_filter=paid

# Pending invoices, paginated
?status_filter=draft&skip=10&limit=5

# Drug items for invoice
?invoice_id=xxx&item_type=drug
```

---

## Request Body Schema

### Create Invoice (POST)
```json
{
  "user_id": "uuid (required)",
  "total_amount": "decimal (required)"
}
```

### Update Invoice (PUT)
```json
{
  "status": "string (optional)",
  "total_amount": "decimal (optional)"
}
```

### Create Invoice Item (POST)
```json
{
  "invoice_id": "uuid (required, from auth/context)",
  "item_type": "string (required, max 50)",
  "item_id": "uuid (required)",
  "quantity": "integer (required, > 0)",
  "price": "decimal (required, > 0)"
}
```

### Update Invoice Item (PUT)
```json
{
  "item_type": "string (optional)",
  "item_id": "uuid (optional)",
  "quantity": "integer (optional)",
  "price": "decimal (optional)"
}
```

---

## Field Validation

| Field | Type | Required | Max Length | Notes |
|-------|------|----------|-----------|-------|
| user_id | UUID | ✓ | - | Must exist in users table |
| total_amount | Decimal | ✓ | - | Must be > 0, 2 decimal places |
| status | String | ✗ | 50 | One of: draft, issued, paid, overdue, cancelled |
| item_type | String | ✓ | 50 | Type of item |
| item_id | UUID | ✓ | - | Reference to item |
| quantity | Integer | ✓ | - | Must be > 0 |
| price | Decimal | ✓ | - | Must be > 0, 2 decimal places |

---

## Filtering & Pagination Guide

### Get All Invoices with Pagination
```bash
# Page 1 (first 10)
curl "http://localhost:8000/api/invoices?skip=0&limit=10"

# Page 2 (next 10)
curl "http://localhost:8000/api/invoices?skip=10&limit=10"

# Page 3 (next 10)
curl "http://localhost:8000/api/invoices?skip=20&limit=10"
```

### Filter by Single Criteria
```bash
# All invoices for user
curl "http://localhost:8000/api/invoices?user_id=xxx"

# All paid invoices
curl "http://localhost:8000/api/invoices?status_filter=paid"
```

### Filter and Paginate
```bash
# User's draft invoices, first 5
curl "http://localhost:8000/api/invoices?user_id=xxx&status_filter=draft&limit=5"

# User's invoices, page 2
curl "http://localhost:8000/api/invoices?user_id=xxx&skip=5&limit=5"

# Drug items, paginated
curl "http://localhost:8000/api/invoice-items?item_type=drug&skip=0&limit=10"
```

---

## Error Codes & Solutions

| Error | Possible Cause | Solution |
|-------|---|-----------|
| 404 Not Found | Invoice doesn't exist | Verify ID is correct |
| 404 Not Found | User doesn't exist | Verify user_id exists |
| 400 Bad Request | Wrong data type | Check UUIDs are valid format |
| 422 Unprocessable | String too long | Trim item_type |
| 422 Unprocessable | Bad amount | Verify amount > 0 with 2 decimals |
| 422 Unprocessable | Bad quantity | Verify quantity > 0 |

---

## Testing in Swagger UI

1. Navigate to: `http://localhost:8000/docs`
2. Scroll to "Invoices" or "Invoice Items" section
3. Click endpoint to expand
4. Click "Try it out"
5. Enter required parameters
6. Click "Execute"
7. View response

---

## Python Example

```python
import requests
from decimal import Decimal

BASE_URL = "http://localhost:8000/api"

# Create invoice
response = requests.post(f"{BASE_URL}/invoices", json={
    "user_id": "770e8400-e29b-41d4-a716-446655440222",
    "total_amount": Decimal("1250.75")
})
invoice = response.json()

# Add item
requests.post(f"{BASE_URL}/invoice-items", json={
    "invoice_id": invoice["id"],
    "item_type": "drug",
    "item_id": "cc0e8400-e29b-41d4-a716-446655440777",
    "quantity": 2,
    "price": Decimal("250.00")
})

# Get invoice with items
response = requests.get(f"{BASE_URL}/invoices/{invoice['id']}")
print(response.json())

# Update status
requests.put(f"{BASE_URL}/invoices/{invoice['id']}", json={
    "status": "issued"
})

# Delete invoice (and items)
requests.delete(f"{BASE_URL}/invoices/{invoice['id']}")
```

---

## JavaScript Example

```javascript
const BASE_URL = "http://localhost:8000/api";

// Create invoice
const response = await fetch(`${BASE_URL}/invoices`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user_id: "770e8400-e29b-41d4-a716-446655440222",
    total_amount: 1250.75
  })
});
const invoice = await response.json();

// Add item
await fetch(`${BASE_URL}/invoice-items`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    invoice_id: invoice.id,
    item_type: "drug",
    item_id: "cc0e8400-e29b-41d4-a716-446655440777",
    quantity: 2,
    price: 250.00
  })
});

// Get invoice with items
const getResponse = await fetch(`${BASE_URL}/invoices/${invoice.id}`);
console.log(await getResponse.json());

// Update status
await fetch(`${BASE_URL}/invoices/${invoice.id}`, {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ status: "issued" })
});

// Delete
await fetch(`${BASE_URL}/invoices/${invoice.id}`, {
  method: "DELETE"
});
```

---

## Common Workflows

### Create Complete Invoice Workflow
```
1. Create invoice
   POST /api/invoices
   
2. Add items to invoice
   POST /api/invoice-items (repeat for each item)
   
3. Issue invoice
   PUT /api/invoices/{id}
   {status: "issued"}
   
4. Mark as paid
   PUT /api/invoices/{id}
   {status: "paid"}
```

### Get Invoice with Details Workflow
```
1. Get invoice (includes items)
   GET /api/invoices/{id}
   
2. Or get items separately
   GET /api/invoice-items/invoice/{id}
```

### Track User Invoices Workflow
```
1. Get user's invoices
   GET /api/invoices/user/{user_id}
   
2. Filter by status
   GET /api/invoices/user/{user_id}?status_filter=paid
   
3. View individual invoice details
   GET /api/invoices/{id}
```

---

## Quick Notes

- All IDs are UUIDs
- Amounts are decimal with 2 decimal places
- Timestamps are ISO 8601 format
- Invoice deletion cascades to items
- User must exist before creating invoice
- Quantity and price must be > 0
- Use pagination for large result sets
- Status transitions: draft → issued → paid/overdue/cancelled

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
✅ **Status:** Ready to Use
