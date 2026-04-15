# 💳 Payments API - Complete Specification

## Overview

The **Payments API** is a complete REST API for managing payment transactions and processing financial records. It enables creation, tracking, and management of payments with multiple payment methods and status tracking.

**Features:**
- Process payment transactions
- Track payment status through lifecycle
- Support multiple payment methods
- Link payments to user accounts
- Filter payments by user/status
- Complete transaction audit trail
- Automatic timestamp tracking

---

## Database Table

### Payments Table

```sql
CREATE TABLE payments (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  amount DECIMAL(12, 2) NOT NULL,
  payment_method VARCHAR(50) NOT NULL,
  payment_status VARCHAR(50) NOT NULL DEFAULT 'pending',
  transaction_id VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (user_id),
  INDEX (payment_status),
  INDEX (transaction_id),
  INDEX (created_at),
  CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded'))
);
```

**Fields:**
- `id`: Unique payment identifier (UUID)
- `user_id`: Reference to the user making the payment
- `amount`: Payment amount with 2 decimal places precision
- `payment_method`: Method used for payment (credit_card, debit_card, upi, bank_transfer, etc.)
- `payment_status`: Status of the payment (pending, completed, failed, refunded)
- `transaction_id`: Unique transaction identifier (unique constraint)
- `created_at`: Timestamp when payment was created
- `updated_at`: Timestamp when payment was last modified

---

## API Endpoints

### Payment Endpoints

#### 1. Create Payment
**Endpoint:** `POST /api/payments`

**Status Code:** `201 Created`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "770e8400-e29b-41d4-a716-446655440222",
  "amount": 150.50,
  "payment_method": "credit_card",
  "transaction_id": "TXN-2024-04-15-001"
}
```

**Success Response:**
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

**Error Responses:**
- `404 Not Found` - User not found
- `400 Bad Request` - Transaction ID already exists or invalid data
- `422 Unprocessable Entity` - Validation error

---

#### 2. Get All Payments
**Endpoint:** `GET /api/payments`

**Query Parameters:**
- `skip` (integer, default: 0) - Number of records to skip
- `limit` (integer, default: 10) - Maximum number to return
- `user_id` (UUID, optional) - Filter by user
- `payment_status` (string, optional) - Filter by status (pending, completed, failed, refunded)

**Example Requests:**
```bash
# Get all payments
GET /api/payments

# Filter by user
GET /api/payments?user_id=770e8400-e29b-41d4-a716-446655440222

# Filter by status
GET /api/payments?payment_status=completed

# Combine filters
GET /api/payments?user_id=770e8400-e29b-41d4-a716-446655440222&payment_status=completed&skip=0&limit=10
```

**Success Response (200 OK):**
```json
[
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440555",
    "user_id": "770e8400-e29b-41d4-a716-446655440222",
    "amount": 150.50,
    "payment_method": "credit_card",
    "payment_status": "completed",
    "transaction_id": "TXN-2024-04-15-001",
    "created_at": "2024-04-15T14:30:00",
    "updated_at": "2024-04-15T14:35:00"
  }
]
```

---

#### 3. Get Single Payment
**Endpoint:** `GET /api/payments/{payment_id}`

**Path Parameters:**
- `payment_id` (UUID) - Payment identifier

**Success Response (200 OK):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "user_id": "770e8400-e29b-41d4-a716-446655440222",
  "amount": 150.50,
  "payment_method": "credit_card",
  "payment_status": "completed",
  "transaction_id": "TXN-2024-04-15-001",
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:35:00"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Payment not found"
}
```

---

#### 4. Get User Payments
**Endpoint:** `GET /api/payments/user/{user_id}`

**Path Parameters:**
- `user_id` (UUID) - User identifier

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)
- `payment_status` (string, optional) - Filter by status

**Success Response (200 OK):**
Returns list of payments for the user, ordered by most recent first.

---

#### 5. Get Payments by Status
**Endpoint:** `GET /api/payments/status/{status}`

**Path Parameters:**
- `status` (string) - Payment status (pending, completed, failed, refunded)

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)

**Success Response (200 OK):**
Returns list of all payments with the specified status.

---

#### 6. Update Payment
**Endpoint:** `PUT /api/payments/{payment_id}`

**Path Parameters:**
- `payment_id` (UUID) - Payment identifier

**Request Body:**
```json
{
  "payment_status": "completed",
  "amount": 150.50,
  "payment_method": "credit_card"
}
```

**Success Response (200 OK):**
Returns updated payment object.

---

#### 7. Delete Payment
**Endpoint:** `DELETE /api/payments/{payment_id}`

**Path Parameters:**
- `payment_id` (UUID) - Payment identifier

**Success Response:** `204 No Content`

---

## Payment Methods

Common payment methods:

| Method | Description |
|--------|-------------|
| `credit_card` | Credit card payment |
| `debit_card` | Debit card payment |
| `upi` | Unified Payments Interface |
| `bank_transfer` | Direct bank transfer |
| `wallet` | Digital wallet payment |
| `cryptocurrency` | Cryptocurrency payment |
| `paypal` | PayPal payment |
| `stripe` | Stripe payment |
| `razorpay` | Razorpay payment |
| `other` | Other payment methods |

---

## Payment Status

Payment lifecycle statuses:

| Status | Description | Allowed Transitions |
|--------|-------------|-------------------|
| `pending` | Payment initiated, awaiting processing | completed, failed |
| `completed` | Payment successfully processed | refunded |
| `failed` | Payment processing failed | - |
| `refunded` | Payment has been refunded | - |

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
| 400 | Bad Request | Transaction ID already exists |
| 404 | Not Found | Payment or user not found |
| 422 | Unprocessable Entity | Invalid field format or value |
| 500 | Internal Server Error | Database or server error |

### Common Errors

**Payment Not Found:**
```json
{
  "detail": "Payment not found"
}
```

**User Not Found:**
```json
{
  "detail": "User not found"
}
```

**Duplicate Transaction ID:**
```json
{
  "detail": "Transaction ID already exists"
}
```

---

## Workflow Examples

### Workflow 1: Process a Payment

```bash
# Step 1: Get user ID (from users API)
curl http://localhost:8000/api/users?role=patient&limit=1

# Step 2: Create payment
curl -X POST http://localhost:8000/api/payments \
  -d '{
    "user_id":"770e8400-e29b-41d4-a716-446655440222",
    "amount":150.50,
    "payment_method":"credit_card",
    "transaction_id":"TXN-2024-04-15-001"
  }'

# Step 3: Retrieve payment to confirm
curl http://localhost:8000/api/payments/aa0e8400-e29b-41d4-a716-446655440555
```

### Workflow 2: Check User Payment History

```bash
# Get all payments for user
curl "http://localhost:8000/api/payments/user/770e8400-e29b-41d4-a716-446655440222"

# Get only completed payments
curl "http://localhost:8000/api/payments/user/770e8400-e29b-41d4-a716-446655440222?payment_status=completed"

# Get only pending payments
curl "http://localhost:8000/api/payments/user/770e8400-e29b-41d4-a716-446655440222?payment_status=pending"
```

### Workflow 3: Track Payment Status

```bash
# Get all pending payments
curl "http://localhost:8000/api/payments/status/pending"

# Get all completed payments
curl "http://localhost:8000/api/payments/status/completed"

# Get all failed payments
curl "http://localhost:8000/api/payments/status/failed"
```

### Workflow 4: Update Payment Status

```bash
# Mark payment as completed
curl -X PUT http://localhost:8000/api/payments/aa0e8400-e29b-41d4-a716-446655440555 \
  -d '{
    "payment_status":"completed"
  }'

# Refund a completed payment
curl -X PUT http://localhost:8000/api/payments/aa0e8400-e29b-41d4-a716-446655440555 \
  -d '{
    "payment_status":"refunded"
  }'
```

---

## Field Validation

### Payment Fields

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| user_id | UUID | ✓ | Must exist in users table |
| amount | Decimal | ✓ | Must be > 0, max 2 decimal places |
| payment_method | String | ✓ | Max 50 characters |
| payment_status | String | ✗ | One of: pending, completed, failed, refunded |
| transaction_id | String | ✓ | Max 255 chars, must be unique |

---

## Performance Characteristics

### Query Performance

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Create payment | 100-200ms | User validation |
| Get single payment | 20-50ms | Direct lookup by ID |
| List payments (10) | 80-120ms | With pagination |
| Filter by user | 100-150ms | Indexed on user_id |
| Filter by status | 100-150ms | Indexed on payment_status |
| Update payment | 80-120ms | |
| Delete payment | 80-120ms | |

### Indexing Strategy

Indexes on:
- `id` (PK)
- `user_id` (FK)
- `payment_status` (for filtering)
- `transaction_id` (unique constraint)
- `created_at` (for sorting)

---

## Integration with Other APIs

### Dependencies

- **Users API** - User IDs and validation

### Related Operations

**Before creating a payment:**
1. Ensure user exists: `GET /api/users/{id}`

**After creating a payment:**
1. Can link to appointments
2. Can associate with prescription orders
3. Can track in financial reports
4. Can include in user billing history

---

## Best Practices

### Do's ✓

- Always verify user exists before creating payment
- Use unique, meaningful transaction IDs
- Track payment status updates consistently
- Archive completed/refunded payments
- Regularly reconcile payment records
- Maintain detailed transaction audit trails
- Use secure payment processing services

### Don'ts ✗

- Don't create payments for non-existent users
- Don't reuse transaction IDs
- Don't allow arbitrary status changes
- Don't delete payment records without archiving
- Don't expose sensitive payment details in logs
- Don't modify user_id after creation
- Don't store raw credit card information

---

## Testing

### Using cURL

```bash
# Create
curl -X POST http://localhost:8000/api/payments \
  -H "Content-Type: application/json" \
  -d '{...}'

# List
curl http://localhost:8000/api/payments

# Get
curl http://localhost:8000/api/payments/{id}

# Filter by user
curl "http://localhost:8000/api/payments/user/{id}"

# Filter by status
curl "http://localhost:8000/api/payments/status/{status}"

# Update
curl -X PUT http://localhost:8000/api/payments/{id} \
  -H "Content-Type: application/json" \
  -d '{...}'

# Delete
curl -X DELETE http://localhost:8000/api/payments/{id}
```

### Using Swagger UI

Navigate to: `http://localhost:8000/docs`

---

## Troubleshooting

### 404 Not Found

**Cause:** Payment or user doesn't exist

**Solution:**
1. Verify payment ID is correct UUID
2. Check if payment was deleted
3. Confirm user exists: `GET /api/users/{id}`

### 400 Bad Request

**Cause:** Duplicate transaction ID or invalid data

**Solution:**
1. Verify transaction_id is unique
2. Check user_id is valid UUID
3. Ensure amount is valid decimal

### 422 Unprocessable Entity

**Cause:** Invalid field values

**Solution:**
1. Check payment_method length (max 50 chars)
2. Verify amount has max 2 decimal places
3. Check transaction_id format (max 255 chars)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-04-15 | Initial release |

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
**Status:** Production Ready ✅
