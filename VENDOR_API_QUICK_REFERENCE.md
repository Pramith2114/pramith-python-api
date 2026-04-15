# Vendor & Vendor Orders API - Quick Reference

## Overview
- **Base Path:** `/api`
- **Vendor Endpoint:** `/api/vendors`
- **Orders Endpoint:** `/api/vendor-orders`

---

## Vendor CRUD Operations

### CREATE Vendor
```bash
POST /api/vendors
Content-Type: application/json

{
  "name": "Supplier Name",
  "contact_number": "+91-XXXXXXXXXX",
  "email": "email@supplier.com",
  "address": "Address"
}
```
**Returns:** 201 Created

### READ All Vendors
```bash
GET /api/vendors?skip=0&limit=10&is_active=true
```
**Returns:** 200 OK - Array of vendors

### READ Single Vendor
```bash
GET /api/vendors/{vendor_id}
```
**Returns:** 200 OK - Vendor object

### UPDATE Vendor
```bash
PUT /api/vendors/{vendor_id}
Content-Type: application/json

{
  "name": "New Name",
  "contact_number": "New Number",
  "email": "new@email.com",
  "address": "New Address",
  "is_active": true
}
```
**Returns:** 200 OK - Updated vendor

### DELETE Vendor
```bash
DELETE /api/vendors/{vendor_id}
```
**Returns:** 204 No Content

---

## Vendor Orders CRUD Operations

### CREATE Order
```bash
POST /api/vendor-orders
Content-Type: application/json

{
  "vendor_id": "UUID",
  "total_amount": 50000.00,
  "status": "pending"
}
```
**Status Options:** `pending` | `confirmed` | `shipped` | `delivered` | `cancelled`
**Returns:** 201 Created

### READ All Orders
```bash
GET /api/vendor-orders?skip=0&limit=10&vendor_id=UUID&status=pending
```
**Returns:** 200 OK - Array of orders

### READ Single Order
```bash
GET /api/vendor-orders/{order_id}
```
**Returns:** 200 OK - Order object with vendor details

### READ Orders by Vendor
```bash
GET /api/vendor-orders/vendor/{vendor_id}?skip=0&limit=10&status=pending
```
**Returns:** 200 OK - Array of vendor's orders

### UPDATE Order
```bash
PUT /api/vendor-orders/{order_id}
Content-Type: application/json

{
  "total_amount": 52000.00,
  "status": "confirmed"
}
```
**Returns:** 200 OK - Updated order

### DELETE Order
```bash
DELETE /api/vendor-orders/{order_id}
```
**Returns:** 204 No Content

---

## Response Objects

### Vendor Response
```json
{
  "id": "UUID",
  "name": "Vendor Name",
  "contact_number": "+91-1234567890",
  "email": "vendor@email.com",
  "address": "Vendor Address",
  "is_active": true,
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

### Vendor Order Response
```json
{
  "id": "UUID",
  "vendor_id": "UUID",
  "total_amount": 50000.00,
  "status": "pending",
  "created_at": "2024-04-15T11:00:00",
  "updated_at": "2024-04-15T11:00:00"
}
```

### Vendor Order Detail Response (includes vendor)
```json
{
  "id": "UUID",
  "vendor_id": "UUID",
  "total_amount": 50000.00,
  "status": "pending",
  "vendor": { /* vendor object */ },
  "created_at": "2024-04-15T11:00:00",
  "updated_at": "2024-04-15T11:00:00"
}
```

---

## Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Delete successful |
| 400 | Bad Request - Invalid data |
| 404 | Not Found - Resource doesn't exist |
| 422 | Unprocessable Entity - Validation error |

---

## Example cURL Commands

### Create Vendor
```bash
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PharmaCorp",
    "contact_number": "+91-9876543210",
    "email": "contact@pharmacorp.com",
    "address": "Chennai, India"
  }'
```

### Get All Vendors
```bash
curl http://localhost:8000/api/vendors?limit=10
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/vendor-orders \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 50000,
    "status": "pending"
  }'
```

### Update Order Status
```bash
curl -X PUT http://localhost:8000/api/vendor-orders/ORDER_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}'
```

### Get Vendor Orders
```bash
curl 'http://localhost:8000/api/vendor-orders/vendor/VENDOR_ID?status=pending'
```

---

## Order Status Workflow

```
Start: pending
  ↓
confirmed (approved order)
  ↓
shipped (in transit)
  ↓
delivered (completed)

OR

cancelled (can be from any state)
```

---

## Filtering & Pagination

### Pagination Example
```bash
GET /api/vendors?skip=10&limit=20
```
- Shows vendors 11-30

### Filter by Status
```bash
GET /api/vendor-orders?status=confirmed
```

### Filter by Vendor
```bash
GET /api/vendor-orders?vendor_id=UUID
```

### Multiple Filters
```bash
GET /api/vendor-orders?vendor_id=UUID&status=pending&limit=5
```

---

## Field Validation Rules

### Vendor Fields
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| name | string | Yes | 1-255 chars |
| contact_number | string | Yes | Valid phone |
| email | string | Yes | Unique, valid email |
| address | string | Yes | 1+ chars |
| is_active | boolean | No | Default: true |

### Order Fields
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| vendor_id | UUID | Yes | Must exist |
| total_amount | decimal | Yes | > 0 |
| status | string | No | Predefined values |

---

## Database Tables

### Vendors Table
```
vendors
├── id (UUID, PK)
├── name (VARCHAR)
├── contact_number (VARCHAR)
├── email (VARCHAR, UNIQUE)
├── address (TEXT)
├── is_active (BOOLEAN)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

### Vendor Orders Table
```
vendor_orders
├── id (UUID, PK)
├── vendor_id (UUID, FK → vendors.id)
├── total_amount (DECIMAL)
├── status (VARCHAR, CHECK)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

---

## Test Script

Run the comprehensive test suite:
```bash
source .venv/bin/activate
python test_vendor_api.py
```

This tests:
- ✓ Create vendors
- ✓ Get all vendors
- ✓ Get single vendor
- ✓ Update vendor
- ✓ Filter vendors
- ✓ Create orders
- ✓ Get orders
- ✓ Update order status
- ✓ Delete orders

---

## Integration Notes

### With Stock Transactions
When an order is delivered, create a stock transaction:
```bash
POST /api/stock-transactions
{
  "drug_id": "UUID",
  "quantity": 100,
  "type": "IN",
  "source": "vendor"
}
```

### With Drugs API
- Link vendor orders to drug inventory
- Track supply chain
- Manage stock levels

---

## Tips & Best Practices

1. **Always verify vendor exists** before creating orders
2. **Use pagination** for large datasets
3. **Track order status** through workflow
4. **Soft delete** vendors (set is_active=false)
5. **Validate email uniqueness** before creating
6. **Filter by status** to monitor orders
7. **Combined filters** for complex queries

---

## Troubleshooting

### Vendor Not Found (404)
- Check vendor_id format (should be valid UUID)
- Verify vendor exists with GET /api/vendors/{id}

### Duplicate Email Error (400)
- Email must be unique
- Check if vendor already exists

### Invalid Status Error (400)
- Use only: `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

### Field Validation Error (422)
- Check all required fields are provided
- Verify field formats and constraints
- total_amount must be > 0

---

## API Performance

Expected Response Times:
- List operations: < 100ms
- Create: < 200ms
- Update: < 200ms
- Delete: < 150ms

---

**Last Updated:** April 15, 2024
**API Version:** 1.0
