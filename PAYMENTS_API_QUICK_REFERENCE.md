# 📚 Payments API - Quick Reference

## Quick Lookup Guide

### Endpoints at a Glance

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/payments` | Create payment |
| GET | `/api/payments` | List all payments (filterable) |
| GET | `/api/payments/{id}` | Get single payment |
| GET | `/api/payments/user/{id}` | Get user's payments |
| GET | `/api/payments/status/{status}` | Get payments by status |
| PUT | `/api/payments/{id}` | Update payment |
| DELETE | `/api/payments/{id}` | Delete payment |

---

## Quick Examples

### Create Payment
```bash
curl -X POST http://localhost:8000/api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "770e8400-e29b-41d4-a716-446655440222",
    "amount": 150.50,
    "payment_method": "credit_card",
    "transaction_id": "TXN-2024-04-15-001"
  }'
```

**Response (201 Created):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "user_id": "770e8400-e29b-41d4-a716-446655440222",
  "amount": 150.50,
  "payment_method": "credit_card",
  "payment_status": "pending",
  "transaction_id": "TXN-2024-04-15-001",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

---

### Get All Payments
```bash
curl http://localhost:8000/api/payments
```

---

### Filter Payments

#### By User
```bash
curl "http://localhost:8000/api/payments?user_id=770e8400-e29b-41d4-a716-446655440222"
```

#### By Status
```bash
curl "http://localhost:8000/api/payments?payment_status=completed"
```

#### By User AND Status
```bash
curl "http://localhost:8000/api/payments?user_id=770e8400-e29b-41d4-a716-446655440222&payment_status=pending"
```

#### With Pagination
```bash
curl "http://localhost:8000/api/payments?skip=10&limit=5"
```

---

### Get User's Payments
```bash
curl "http://localhost:8000/api/payments/user/770e8400-e29b-41d4-a716-446655440222"
```

**With Optional Status Filter:**
```bash
curl "http://localhost:8000/api/payments/user/770e8400-e29b-41d4-a716-446655440222?payment_status=completed"
```

---

### Get Single Payment
```bash
curl http://localhost:8000/api/payments/aa0e8400-e29b-41d4-a716-446655440555
```

---

### Get Payments by Status
```bash
curl "http://localhost:8000/api/payments/status/pending"
```

---

### Update Payment Status
```bash
curl -X PUT http://localhost:8000/api/payments/aa0e8400-e29b-41d4-a716-446655440555 \
  -H "Content-Type: application/json" \
  -d '{
    "payment_status": "completed"
  }'
```

---

### Delete Payment
```bash
curl -X DELETE http://localhost:8000/api/payments/aa0e8400-e29b-41d4-a716-446655440555
```

**Response:** `204 No Content`

---

## Response Schemas

### Payment Object
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "amount": "decimal",
  "payment_method": "string",
  "payment_status": "string",
  "transaction_id": "string",
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
| 400 | Bad Request - Invalid format or duplicate ID |
| 404 | Not Found - Resource not found |
| 422 | Validation Error - Invalid data |

---

## Payment Methods

```
• credit_card        Credit card
• debit_card         Debit card
• upi                Unified Payments Interface
• bank_transfer      Bank transfer
• wallet             Digital wallet
• cryptocurrency     Cryptocurrency
• paypal             PayPal
• stripe             Stripe
• razorpay           Razorpay
• other              Other methods
```

---

## Payment Status Values

```
• pending            Payment awaiting processing
• completed          Payment successfully processed
• failed             Payment processing failed
• refunded           Payment has been refunded
```

---

## Query Parameters

### List & Filter Query Parameters
- `skip` (int) - Records to skip (default: 0)
- `limit` (int) - Max records to return (default: 10)
- `user_id` (UUID) - Filter by user
- `payment_status` (string) - Filter by status

### Example Combinations
```bash
# Skip 20, return 5
?skip=20&limit=5

# User's recent completed payments
?user_id=xxx&payment_status=completed

# Pending payments, paginated
?payment_status=pending&skip=10&limit=5
```

---

## Request Body Schema

### Create Payment (POST)
```json
{
  "user_id": "uuid (required)",
  "amount": "decimal (required)",
  "payment_method": "string (required, max 50)",
  "transaction_id": "string (required, max 255, unique)"
}
```

### Update Payment (PUT)
```json
{
  "payment_status": "string (optional)",
  "amount": "decimal (optional)",
  "payment_method": "string (optional)"
}
```

---

## Field Validation

| Field | Type | Required | Max Length | Notes |
|-------|------|----------|-----------|-------|
| user_id | UUID | ✓ | - | Must exist in users table |
| amount | Decimal | ✓ | - | Must be > 0, 2 decimal places |
| payment_method | String | ✓ | 50 | Payment method type |
| payment_status | String | ✗ | 50 | One of: pending, completed, failed, refunded |
| transaction_id | String | ✓ | 255 | Unique identifier |

---

## Filtering & Pagination Guide

### Get All Payments with Pagination
```bash
# Page 1 (first 10)
curl "http://localhost:8000/api/payments?skip=0&limit=10"

# Page 2 (next 10)
curl "http://localhost:8000/api/payments?skip=10&limit=10"

# Page 3 (next 10)
curl "http://localhost:8000/api/payments?skip=20&limit=10"
```

### Filter by Single Criteria
```bash
# All payments for user
curl "http://localhost:8000/api/payments?user_id=xxx"

# All pending payments
curl "http://localhost:8000/api/payments?payment_status=pending"
```

### Filter and Paginate
```bash
# User's pending payments, first 5
curl "http://localhost:8000/api/payments?user_id=xxx&payment_status=pending&limit=5"

# User's payments, page 2
curl "http://localhost:8000/api/payments?user_id=xxx&skip=5&limit=5"
```

---

## Error Codes & Solutions

| Error | Possible Cause | Solution |
|-------|---|-----------|
| 404 Not Found | Payment doesn't exist | Verify ID is correct |
| 404 Not Found | User doesn't exist | Verify user_id exists |
| 400 Bad Request | Duplicate transaction_id | Use unique transaction ID |
| 400 Bad Request | Wrong data type | Check UUIDs are valid format |
| 422 Unprocessable | String too long | Trim payment_method or transaction_id |
| 422 Unprocessable | Bad amount | Verify amount > 0 with 2 decimals |

---

## Testing in Swagger UI

1. Navigate to: `http://localhost:8000/docs`
2. Scroll to "Payments" section
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

# Create
response = requests.post(f"{BASE_URL}/payments", json={
    "user_id": "770e8400-e29b-41d4-a716-446655440222",
    "amount": Decimal("150.50"),
    "payment_method": "credit_card",
    "transaction_id": "TXN-2024-04-15-001"
})
payment = response.json()

# Get
response = requests.get(f"{BASE_URL}/payments/{payment['id']}")
print(response.json())

# List
response = requests.get(f"{BASE_URL}/payments?limit=10")
print(response.json())

# Update
requests.put(f"{BASE_URL}/payments/{payment['id']}", json={
    "payment_status": "completed"
})

# Delete
requests.delete(f"{BASE_URL}/payments/{payment['id']}")
```

---

## JavaScript Example

```javascript
const BASE_URL = "http://localhost:8000/api";

// Create
const response = await fetch(`${BASE_URL}/payments`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user_id: "770e8400-e29b-41d4-a716-446655440222",
    amount: 150.50,
    payment_method: "credit_card",
    transaction_id: "TXN-2024-04-15-001"
  })
});
const payment = await response.json();

// Get
const getResponse = await fetch(`${BASE_URL}/payments/${payment.id}`);
console.log(await getResponse.json());

// List
const listResponse = await fetch(`${BASE_URL}/payments?limit=10`);
console.log(await listResponse.json());

// Update
await fetch(`${BASE_URL}/payments/${payment.id}`, {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    payment_status: "completed"
  })
});

// Delete
await fetch(`${BASE_URL}/payments/${payment.id}`, {
  method: "DELETE"
});
```

---

## Common Workflows

### Process Payment Workflow
```
1. Get user ID (from users API)
   GET /api/users?role=patient
   
2. Create payment
   POST /api/payments
   {user_id, amount, payment_method, transaction_id}
   
3. Update status when processed
   PUT /api/payments/{id}
   {payment_status: "completed"}
   
4. Retrieve payment record
   GET /api/payments/{id}
```

### Track Payment History Workflow
```
1. Get user's payments
   GET /api/payments/user/{user_id}
   
2. Filter by status if needed
   GET /api/payments/user/{user_id}?payment_status=completed
   
3. View individual payment details
   GET /api/payments/{id}
```

### Search Payments by Status Workflow
```
1. Get payments with specific status
   GET /api/payments/status/{status}
   
2. View pagination if large result set
   GET /api/payments/status/{status}?skip=10&limit=5
   
3. View individual payment details
   GET /api/payments/{id}
```

---

## Quick Notes

- All IDs are UUIDs
- Amounts are decimal with 2 decimal places
- Timestamps are ISO 8601 format
- Transaction IDs must be unique
- User must exist before creating payment
- Payment status transitions: pending → completed/failed, completed → refunded
- Use pagination for large result sets
- Filter by status for financial reporting

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
✅ **Status:** Ready to Use
