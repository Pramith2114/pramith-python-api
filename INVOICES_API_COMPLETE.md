# 📋 Invoices API - Complete Specification

## Overview

The **Invoices API** is a complete REST API for managing invoices and invoice line items. It supports creating invoices, adding multiple items to invoices, tracking invoice status, and managing financial transactions related to billing.

**Features:**
- Create and manage invoices
- Add multiple items to invoices (drugs, consultations, services)
- Track invoice status through lifecycle
- Link invoices to user accounts
- Filter invoices by user/status
- Complete detailed invoice responses
- Automatic calculation of totals
- Complete audit trail with timestamps

---

## Database Tables

### Invoices Table

```sql
CREATE TABLE invoices (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  total_amount DECIMAL(12, 2) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (user_id),
  INDEX (status),
  INDEX (created_at),
  CHECK (status IN ('draft', 'issued', 'paid', 'overdue', 'cancelled'))
);
```

### Invoice Items Table

```sql
CREATE TABLE invoice_items (
  id UUID PRIMARY KEY,
  invoice_id UUID NOT NULL REFERENCES invoices(id),
  item_type VARCHAR(50) NOT NULL,
  item_id UUID NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  price DECIMAL(12, 2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (invoice_id),
  INDEX (item_type)
);
```

**Invoice Fields:**
- `id`: Unique invoice identifier (UUID)
- `user_id`: Reference to the user (customer)
- `total_amount`: Total invoice amount with 2 decimal places
- `status`: Invoice status (draft, issued, paid, overdue, cancelled)
- `created_at`: Timestamp when invoice was created
- `updated_at`: Timestamp when invoice was last modified

**Invoice Item Fields:**
- `id`: Unique item identifier (UUID)
- `invoice_id`: Reference to the invoice
- `item_type`: Type of item (drug, consultation, service, etc.)
- `item_id`: UUID reference to the actual item
- `quantity`: Quantity of items
- `price`: Unit price of item
- `created_at`: Timestamp when item was added
- `updated_at`: Timestamp when item was last modified

---

## API Endpoints

### Invoice Endpoints

#### 1. Create Invoice
**Endpoint:** `POST /api/invoices`

**Status Code:** `201 Created`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_id": "770e8400-e29b-41d4-a716-446655440222",
  "total_amount": 1250.75
}
```

**Success Response:**
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

**Error Responses:**
- `404 Not Found` - User not found
- `400 Bad Request` - Invalid data format
- `422 Unprocessable Entity` - Validation error

---

#### 2. Get All Invoices
**Endpoint:** `GET /api/invoices`

**Query Parameters:**
- `skip` (integer, default: 0) - Number of records to skip
- `limit` (integer, default: 10) - Maximum number to return
- `user_id` (UUID, optional) - Filter by user
- `status_filter` (string, optional) - Filter by status

**Example Requests:**
```bash
# Get all invoices
GET /api/invoices

# Filter by user
GET /api/invoices?user_id=770e8400-e29b-41d4-a716-446655440222

# Filter by status
GET /api/invoices?status_filter=paid

# Combine filters
GET /api/invoices?user_id=xxx&status_filter=issued&skip=0&limit=10
```

**Success Response (200 OK):**
```json
[
  {
    "id": "aa0e8400-e29b-41d4-a716-446655440555",
    "user_id": "770e8400-e29b-41d4-a716-446655440222",
    "total_amount": 1250.75,
    "status": "draft",
    "created_at": "2024-04-15T14:30:00",
    "updated_at": "2024-04-15T14:30:00"
  }
]
```

---

#### 3. Get Single Invoice (with items)
**Endpoint:** `GET /api/invoices/{invoice_id}`

**Path Parameters:**
- `invoice_id` (UUID) - Invoice identifier

**Success Response (200 OK):**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440555",
  "user_id": "770e8400-e29b-41d4-a716-446655440222",
  "total_amount": 1250.75,
  "status": "draft",
  "items": [
    {
      "id": "bb0e8400-e29b-41d4-a716-446655440666",
      "invoice_id": "aa0e8400-e29b-41d4-a716-446655440555",
      "item_type": "drug",
      "item_id": "cc0e8400-e29b-41d4-a716-446655440777",
      "quantity": 2,
      "price": 250.00,
      "created_at": "2024-04-15T14:35:00",
      "updated_at": "2024-04-15T14:35:00"
    }
  ],
  "created_at": "2024-04-15T14:30:00",
  "updated_at": "2024-04-15T14:30:00"
}
```

---

#### 4. Get User Invoices
**Endpoint:** `GET /api/invoices/user/{user_id}`

**Path Parameters:**
- `user_id` (UUID) - User identifier

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)
- `status_filter` (string, optional) - Filter by status

**Success Response (200 OK):**
Returns list of invoices for the user, ordered by most recent first.

---

#### 5. Update Invoice
**Endpoint:** `PUT /api/invoices/{invoice_id}`

**Path Parameters:**
- `invoice_id` (UUID) - Invoice identifier

**Request Body:**
```json
{
  "status": "issued",
  "total_amount": 1250.75
}
```

**Success Response (200 OK):**
Returns updated invoice object.

---

#### 6. Delete Invoice
**Endpoint:** `DELETE /api/invoices/{invoice_id}`

**Path Parameters:**
- `invoice_id` (UUID) - Invoice identifier

**Success Response:** `204 No Content`

*Note: Deletes all associated invoice items (cascade delete)*

---

### Invoice Items Endpoints

#### 7. Create Invoice Item
**Endpoint:** `POST /api/invoice-items`

**Status Code:** `201 Created`

**Request Body:**
```json
{
  "invoice_id": "aa0e8400-e29b-41d4-a716-446655440555",
  "item_type": "drug",
  "item_id": "cc0e8400-e29b-41d4-a716-446655440777",
  "quantity": 2,
  "price": 250.00
}
```

**Success Response:**
```json
{
  "id": "bb0e8400-e29b-41d4-a716-446655440666",
  "invoice_id": "aa0e8400-e29b-41d4-a716-446655440555",
  "item_type": "drug",
  "item_id": "cc0e8400-e29b-41d4-a716-446655440777",
  "quantity": 2,
  "price": 250.00,
  "created_at": "2024-04-15T14:35:00",
  "updated_at": "2024-04-15T14:35:00"
}
```

---

#### 8. Get All Invoice Items
**Endpoint:** `GET /api/invoice-items`

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)
- `invoice_id` (UUID, optional) - Filter by invoice
- `item_type` (string, optional) - Filter by item type

---

#### 9. Get Single Invoice Item
**Endpoint:** `GET /api/invoice-items/{item_id}`

**Path Parameters:**
- `item_id` (UUID) - Item identifier

---

#### 10. Get Invoice Items
**Endpoint:** `GET /api/invoice-items/invoice/{invoice_id}`

**Path Parameters:**
- `invoice_id` (UUID) - Invoice identifier

**Query Parameters:**
- `skip` (integer, default: 0)
- `limit` (integer, default: 10)

**Success Response:**
Returns list of items for the invoice.

---

#### 11. Update Invoice Item
**Endpoint:** `PUT /api/invoice-items/{item_id}`

**Path Parameters:**
- `item_id` (UUID) - Item identifier

**Request Body:**
```json
{
  "quantity": 3,
  "price": 275.00
}
```

**Success Response (200 OK):**
Returns updated item object.

---

#### 12. Delete Invoice Item
**Endpoint:** `DELETE /api/invoice-items/{item_id}`

**Path Parameters:**
- `item_id` (UUID) - Item identifier

**Success Response:** `204 No Content`

---

## Invoice Status

Invoice lifecycle statuses:

| Status | Description |
|--------|-------------|
| `draft` | Invoice being prepared |
| `issued` | Invoice sent to customer |
| `paid` | Invoice payment received |
| `overdue` | Payment overdue |
| `cancelled` | Invoice cancelled |

---

## Item Types

Common item types in invoices:

| Type | Description |
|------|-------------|
| `drug` | Drug/medication sold |
| `consultation` | Doctor consultation fee |
| `service` | Medical service provided |
| `lab_test` | Laboratory test |
| `procedure` | Surgical/medical procedure |
| `other` | Other items |

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
| 400 | Bad Request | Invalid data format |
| 404 | Not Found | Invoice or user not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Database or server error |

---

## Workflow Examples

### Workflow 1: Create and Populate Invoice

```bash
# Step 1: Create invoice
curl -X POST http://localhost:8000/api/invoices \
  -d '{
    "user_id":"770e8400-e29b-41d4-a716-446655440222",
    "total_amount":1250.75
  }'
# Returns: invoice_id = aa0e8400-e29b-41d4-a716-446655440555

# Step 2: Add drug item
curl -X POST http://localhost:8000/api/invoice-items \
  -d '{
    "invoice_id":"aa0e8400-e29b-41d4-a716-446655440555",
    "item_type":"drug",
    "item_id":"cc0e8400-e29b-41d4-a716-446655440777",
    "quantity":2,
    "price":250.00
  }'

# Step 3: Add consultation item
curl -X POST http://localhost:8000/api/invoice-items \
  -d '{
    "invoice_id":"aa0e8400-e29b-41d4-a716-446655440555",
    "item_type":"consultation",
    "item_id":"dd0e8400-e29b-41d4-a716-446655440888",
    "quantity":1,
    "price":750.75
  }'

# Step 4: Issue invoice
curl -X PUT http://localhost:8000/api/invoices/aa0e8400-e29b-41d4-a716-446655440555 \
  -d '{"status":"issued"}'
```

### Workflow 2: Get Invoice with Details

```bash
# Get invoice with all items
curl http://localhost:8000/api/invoices/aa0e8400-e29b-41d4-a716-446655440555
```

### Workflow 3: Track User Invoices

```bash
# Get all invoices for user
curl "http://localhost:8000/api/invoices/user/770e8400-e29b-41d4-a716-446655440222"

# Get only paid invoices
curl "http://localhost:8000/api/invoices/user/770e8400-e29b-41d4-a716-446655440222?status_filter=paid"

# Get draft invoices
curl "http://localhost:8000/api/invoices/user/770e8400-e29b-41d4-a716-446655440222?status_filter=draft"
```

---

## Field Validation

### Invoice Fields

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| user_id | UUID | ✓ | Must exist in users table |
| total_amount | Decimal | ✓ | Must be > 0, max 2 decimal places |
| status | String | ✗ | One of: draft, issued, paid, overdue, cancelled |

### Invoice Item Fields

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| invoice_id | UUID | ✓ | Must exist in invoices table |
| item_type | String | ✓ | Max 50 characters |
| item_id | UUID | ✓ | Reference to actual item |
| quantity | Integer | ✓ | Must be > 0 |
| price | Decimal | ✓ | Must be > 0, max 2 decimal places |

---

## Performance Characteristics

### Query Performance

| Operation | Expected Time |
|-----------|----------------|
| Create invoice | 100-200ms |
| Get single invoice | 20-50ms |
| List invoices (10) | 80-120ms |
| Filter by user | 100-150ms |
| Filter by status | 100-150ms |
| Get detailed invoice | 150-250ms |
| Update invoice | 80-120ms |
| Delete invoice | 150-250ms |

### Indexing Strategy

Indexes on:
- `id` (PK)
- `user_id` (FK)
- `status` (for filtering)
- `created_at` (for sorting)
- `invoice_id` (FK in items)
- `item_type` (for filtering in items)

---

## Integration with Other APIs

### Dependencies

- **Users API** - User IDs and validation

### Related Operations

**Before creating invoice:**
1. Ensure user exists

**Before adding item:**
1. Ensure invoice exists
2. Item reference (drug_id, consultation_id, etc.)

---

## Best Practices

### Do's ✓

- Always verify user exists before creating invoice
- Use meaningful item types
- Update status as invoice progresses
- Archive completed invoices
- Regularly reconcile invoice totals
- Maintain detailed audit trails
- Delete/archive old invoices safely

### Don'ts ✗

- Don't create invoices for non-existent users
- Don't delete invoices without archiving
- Don't allow arbitrary status changes
- Don't store sensitive payment details in items
- Don't modify user_id after creation
- Don't ignore invoice notifications

---

## Testing

### Using cURL

```bash
# Invoices
curl -X POST http://localhost:8000/api/invoices -d '{...}'
curl http://localhost:8000/api/invoices
curl http://localhost:8000/api/invoices/{id}
curl "http://localhost:8000/api/invoices/user/{id}"
curl -X PUT http://localhost:8000/api/invoices/{id} -d '{...}'
curl -X DELETE http://localhost:8000/api/invoices/{id}

# Items
curl -X POST http://localhost:8000/api/invoice-items -d '{...}'
curl http://localhost:8000/api/invoice-items
curl http://localhost:8000/api/invoice-items/{id}
curl "http://localhost:8000/api/invoice-items/invoice/{id}"
curl -X PUT http://localhost:8000/api/invoice-items/{id} -d '{...}'
curl -X DELETE http://localhost:8000/api/invoice-items/{id}
```

### Using Swagger UI

Navigate to: `http://localhost:8000/docs`

---

## Troubleshooting

### 404 Not Found

**Cause:** Invoice or user doesn't exist

**Solution:**
1. Verify invoice ID is correct UUID
2. Check if invoice was deleted
3. Confirm user exists: `GET /api/users/{id}`

### 400 Bad Request

**Cause:** Missing required fields or invalid data

**Solution:**
1. Verify all required fields are present
2. Check data types match schema
3. Ensure UUIDs are valid format

### 422 Unprocessable Entity

**Cause:** Invalid field values

**Solution:**
1. Check amount is > 0 with max 2 decimals
2. Verify item_type is valid
3. Ensure quantity is > 0

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-04-15 | Initial release |

---

**Last Updated:** April 15, 2024  
**API Version:** 1.0  
**Status:** Production Ready ✅
