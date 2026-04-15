# Vendor & Vendor Orders API Documentation

## Overview

The Vendor and Vendor Orders APIs are designed for managing pharmaceutical vendors/suppliers and their purchase orders in the Pramith API system.

---

## Database Schema

### Vendors Table

```sql
CREATE TABLE vendors (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  contact_number VARCHAR(20) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  address TEXT NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Vendor Orders Table

```sql
CREATE TABLE vendor_orders (
  id UUID PRIMARY KEY,
  vendor_id UUID REFERENCES vendors(id),
  total_amount DECIMAL(12, 2) NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT valid_order_status CHECK (status IN ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled'))
);
```

---

## Vendor API Endpoints

### 1. Create Vendor
**Endpoint:** `POST /api/vendors`

**Request Body:**
```json
{
  "name": "PharmaCorp Suppliers",
  "contact_number": "+91-9876543210",
  "email": "info@pharmacorp.com",
  "address": "123 Medical Street, Chennai, Tamil Nadu"
}
```

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "PharmaCorp Suppliers",
  "contact_number": "+91-9876543210",
  "email": "info@pharmacorp.com",
  "address": "123 Medical Street, Chennai, Tamil Nadu",
  "is_active": true,
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

**Error Responses:**
- **400 Bad Request:** Vendor with this email already exists
- **422 Unprocessable Entity:** Missing required fields

---

### 2. Get All Vendors
**Endpoint:** `GET /api/vendors`

**Query Parameters:**
- `skip` (int, optional): Number of vendors to skip (default: 0)
- `limit` (int, optional): Maximum number to return (default: 10)
- `is_active` (bool, optional): Filter by active status

**Example Request:**
```
GET /api/vendors?skip=0&limit=10&is_active=true
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "PharmaCorp Suppliers",
    "contact_number": "+91-9876543210",
    "email": "info@pharmacorp.com",
    "address": "123 Medical Street, Chennai, Tamil Nadu",
    "is_active": true,
    "created_at": "2024-04-15T10:30:00",
    "updated_at": "2024-04-15T10:30:00"
  }
]
```

---

### 3. Get Specific Vendor
**Endpoint:** `GET /api/vendors/{vendor_id}`

**Path Parameters:**
- `vendor_id` (UUID): The vendor's ID

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "PharmaCorp Suppliers",
  "contact_number": "+91-9876543210",
  "email": "info@pharmacorp.com",
  "address": "123 Medical Street, Chennai, Tamil Nadu",
  "is_active": true,
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T10:30:00"
}
```

**Error Responses:**
- **404 Not Found:** Vendor not found

---

### 4. Update Vendor
**Endpoint:** `PUT /api/vendors/{vendor_id}`

**Path Parameters:**
- `vendor_id` (UUID): The vendor's ID

**Request Body (all fields optional):**
```json
{
  "name": "PharmaCorp Suppliers Ltd",
  "contact_number": "+91-9876543211",
  "email": "newemail@pharmacorp.com",
  "address": "789 Medical District, Chennai",
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "PharmaCorp Suppliers Ltd",
  "contact_number": "+91-9876543211",
  "email": "newemail@pharmacorp.com",
  "address": "789 Medical District, Chennai",
  "is_active": true,
  "created_at": "2024-04-15T10:30:00",
  "updated_at": "2024-04-15T14:45:00"
}
```

**Error Responses:**
- **404 Not Found:** Vendor not found
- **400 Bad Request:** Email already exists for another vendor

---

### 5. Delete Vendor
**Endpoint:** `DELETE /api/vendors/{vendor_id}`

**Path Parameters:**
- `vendor_id` (UUID): The vendor's ID

**Response (204 No Content)**

**Error Responses:**
- **404 Not Found:** Vendor not found

---

## Vendor Orders API Endpoints

### 1. Create Vendor Order
**Endpoint:** `POST /api/vendor-orders`

**Request Body:**
```json
{
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_amount": 50000.00,
  "status": "pending"
}
```

**Valid Statuses:** `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

**Response (201 Created):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_amount": 50000.00,
  "status": "pending",
  "created_at": "2024-04-15T11:00:00",
  "updated_at": "2024-04-15T11:00:00"
}
```

**Error Responses:**
- **404 Not Found:** Vendor not found
- **400 Bad Request:** Invalid status
- **422 Unprocessable Entity:** Missing required fields or invalid total_amount

---

### 2. Get All Vendor Orders
**Endpoint:** `GET /api/vendor-orders`

**Query Parameters:**
- `skip` (int, optional): Number of orders to skip (default: 0)
- `limit` (int, optional): Maximum number to return (default: 10)
- `vendor_id` (UUID, optional): Filter by vendor
- `status` (string, optional): Filter by order status

**Example Request:**
```
GET /api/vendor-orders?skip=0&limit=10&status=confirmed
```

**Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 50000.00,
    "status": "confirmed",
    "created_at": "2024-04-15T11:00:00",
    "updated_at": "2024-04-15T12:30:00"
  }
]
```

---

### 3. Get Specific Vendor Order
**Endpoint:** `GET /api/vendor-orders/{order_id}`

**Path Parameters:**
- `order_id` (UUID): The order's ID

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_amount": 50000.00,
  "status": "confirmed",
  "vendor": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "PharmaCorp Suppliers",
    "contact_number": "+91-9876543210",
    "email": "info@pharmacorp.com",
    "address": "123 Medical Street, Chennai",
    "is_active": true,
    "created_at": "2024-04-15T10:30:00",
    "updated_at": "2024-04-15T10:30:00"
  },
  "created_at": "2024-04-15T11:00:00",
  "updated_at": "2024-04-15T12:30:00"
}
```

**Error Responses:**
- **404 Not Found:** Vendor order not found

---

### 4. Get Orders by Vendor
**Endpoint:** `GET /api/vendor-orders/vendor/{vendor_id}`

**Path Parameters:**
- `vendor_id` (UUID): The vendor's ID

**Query Parameters:**
- `skip` (int, optional): Number of orders to skip (default: 0)
- `limit` (int, optional): Maximum number to return (default: 10)
- `status` (string, optional): Filter by order status

**Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440111",
    "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 50000.00,
    "status": "pending",
    "created_at": "2024-04-15T11:00:00",
    "updated_at": "2024-04-15T11:00:00"
  }
]
```

**Error Responses:**
- **404 Not Found:** Vendor not found

---

### 5. Update Vendor Order
**Endpoint:** `PUT /api/vendor-orders/{order_id}`

**Path Parameters:**
- `order_id` (UUID): The order's ID

**Request Body (all fields optional):**
```json
{
  "total_amount": 52000.00,
  "status": "confirmed"
}
```

**Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_amount": 52000.00,
  "status": "confirmed",
  "created_at": "2024-04-15T11:00:00",
  "updated_at": "2024-04-15T14:00:00"
}
```

**Error Responses:**
- **404 Not Found:** Vendor order not found
- **400 Bad Request:** Invalid status

---

### 6. Delete Vendor Order
**Endpoint:** `DELETE /api/vendor-orders/{order_id}`

**Path Parameters:**
- `order_id` (UUID): The order's ID

**Response (204 No Content)**

**Error Responses:**
- **404 Not Found:** Vendor order not found

---

## Order Status Workflow

```
pending → confirmed → shipped → delivered (completed)
   ↓
cancelled (can be done from any state)
```

---

## Example Workflow

### 1. Add a New Vendor
```bash
curl -X POST http://localhost:8000/api/vendors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MediPharm Distributors",
    "contact_number": "+91-9876543210",
    "email": "sales@medipharm.com",
    "address": "456 Healthcare Complex, Bangalore"
  }'
```

### 2. Create an Order
```bash
curl -X POST http://localhost:8000/api/vendor-orders \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount": 100000.00,
    "status": "pending"
  }'
```

### 3. Confirm the Order
```bash
curl -X PUT http://localhost:8000/api/vendor-orders/660e8400-e29b-41d4-a716-446655440111 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed"
  }'
```

### 4. Track Order Status
```bash
curl -X GET http://localhost:8000/api/vendor-orders/660e8400-e29b-41d4-a716-446655440111
```

---

## Pagination

All list endpoints support pagination using `skip` and `limit` parameters:

```
GET /api/vendors?skip=0&limit=10
```

- `skip`: Offset for pagination (default: 0)
- `limit`: Number of items to return (default: 10)

---

## Filtering

### Filter Vendors by Active Status
```
GET /api/vendors?is_active=true
```

### Filter Orders by Vendor
```
GET /api/vendor-orders?vendor_id=550e8400-e29b-41d4-a716-446655440000
```

### Filter Orders by Status
```
GET /api/vendor-orders?status=confirmed
```

### Combine Filters
```
GET /api/vendor-orders?vendor_id=550e8400-e29b-41d4-a716-446655440000&status=pending&limit=5
```

---

## Running Tests

To test the Vendor API endpoints, run the test script:

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the server (in another terminal)
python -m uvicorn app.main:app --reload --port 8000

# Run tests
python test_vendor_api.py
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "detail": "Vendor with this email already exists"
}
```

### 404 Not Found
```json
{
  "detail": "Vendor not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "total_amount"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

---

## Field Validation

### Vendor Fields
- **name** (string, required): 1-255 characters
- **contact_number** (string, required): Valid phone number format
- **email** (string, required): Valid email address, unique
- **address** (string, required): 1-500+ characters
- **is_active** (boolean, optional): Default is `true`

### Vendor Order Fields
- **vendor_id** (UUID, required): Must reference an existing vendor
- **total_amount** (decimal, required): Must be > 0
- **status** (string, optional): One of `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

---

## Best Practices

1. **Always validate vendor exists** before creating orders
2. **Use vendor_id to filter orders** for vendor-specific queries
3. **Track order status progression** for audit trails
4. **Soft delete vendors** by setting `is_active = false` instead of hard delete
5. **Implement transaction management** for multi-step order processes

---

## Integration with Other APIs

### Link with Drugs API
To track drug orders from vendors:
1. Create vendor via `/api/vendors`
2. Create order via `/api/vendor-orders`
3. Update drug stock when order status = `delivered`

### Link with Stock Transactions API
When vendor order is delivered:
```bash
POST /api/stock-transactions
{
  "drug_id": "...",
  "quantity": 100,
  "type": "IN",
  "source": "vendor"
}
```

---

## API Response Time

Expected response times:
- List operations: < 100ms
- Create operations: < 200ms
- Update operations: < 200ms
- Delete operations: < 150ms

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production, consider adding:
- 1000 requests per hour per IP
- 10 requests per second per user

---

## Version & Support

API Version: 1.0
Last Updated: April 15, 2024

For issues or questions, refer to the main API documentation or contact the development team.
