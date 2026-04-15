# Stock Transactions API - Quick Reference

## Overview
The Stock Transactions API manages inventory changes for drugs/medicines. It tracks stock movements (IN/OUT), automatically updates drug inventory levels, and provides comprehensive filtering and audit capabilities.

## Base URL
```
/api/stock-transactions
```

## Database Schema

### `stock_transactions` Table
```sql
CREATE TABLE stock_transactions (
  id UUID PRIMARY KEY,
  drug_id UUID REFERENCES drugs(id),
  quantity INT (must be positive),
  type VARCHAR(10) CHECK (type IN ('IN','OUT')),
  source VARCHAR(255), -- vendor/prescription/adjustment
  created_at TIMESTAMP DEFAULT now()
);
```

## API Endpoints

### 1. Create Stock Transaction
**POST** `/api/stock-transactions`

**Request Body:**
```json
{
  "drug_id": "uuid",
  "quantity": 50,
  "type": "IN",
  "source": "vendor"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "drug_id": "uuid",
  "quantity": 50,
  "type": "IN",
  "source": "vendor",
  "created_at": "2026-04-14T15:37:53.854470"
}
```

**Features:**
- Automatically updates drug's `stock_quantity`:
  - **IN**: `stock_quantity += quantity`
  - **OUT**: `stock_quantity -= quantity`
- Validates transaction type ('IN' or 'OUT')
- Prevents negative stock (OUT transactions check available stock)

---

### 2. Get All Transactions
**GET** `/api/stock-transactions`

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10): Results per page
- `drug_id` (UUID, optional): Filter by drug
- `type` (string, optional): Filter by 'IN' or 'OUT'
- `source` (string, optional): Filter by source (partial match)

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "drug_id": "uuid",
    "quantity": 50,
    "type": "IN",
    "source": "vendor",
    "created_at": "2026-04-14T15:37:53.854470"
  }
]
```

---

### 3. Get Transaction by ID
**GET** `/api/stock-transactions/{transaction_id}`

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "drug_id": "uuid",
  "quantity": 50,
  "type": "IN",
  "source": "vendor",
  "created_at": "2026-04-14T15:37:53.854470"
}
```

---

### 4. Get All Transactions for a Drug
**GET** `/api/stock-transactions/drug/{drug_id}`

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10): Results per page

**Response:** `200 OK` (list of transactions)

**Note:** Returns transactions sorted by `created_at` in descending order (newest first)

---

### 5. Update Transaction
**PUT** `/api/stock-transactions/{transaction_id}`

**Request Body:**
```json
{
  "quantity": 60,
  "source": "vendor_adjusted"
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "drug_id": "uuid",
  "quantity": 60,
  "type": "IN",
  "source": "vendor_adjusted",
  "created_at": "2026-04-14T15:37:53.854470"
}
```

**Features:**
- Updates quantity and/or source
- Auto-adjusts drug stock when quantity changes
- Cannot change `drug_id` or `type` after creation

---

### 6. Delete Transaction
**DELETE** `/api/stock-transactions/{transaction_id}`

**Response:** `204 No Content`

**Features:**
- Reverses stock adjustment when deleted:
  - **IN transactions**: decreases stock
  - **OUT transactions**: increases stock (adds back to inventory)

---

## Usage Examples

### Example 1: Record Stock Receipt from Vendor
```bash
curl -X POST http://localhost:8000/api/stock-transactions \
  -H "Content-Type: application/json" \
  -d '{
    "drug_id": "86630e18-39bd-4a0b-919b-0a10f0886f6b",
    "quantity": 100,
    "type": "IN",
    "source": "vendor"
  }'
```

### Example 2: Record Drug Dispensed via Prescription
```bash
curl -X POST http://localhost:8000/api/stock-transactions \
  -H "Content-Type: application/json" \
  -d '{
    "drug_id": "86630e18-39bd-4a0b-919b-0a10f0886f6b",
    "quantity": 5,
    "type": "OUT",
    "source": "prescription"
  }'
```

### Example 3: Get Stock History for a Drug
```bash
curl "http://localhost:8000/api/stock-transactions/drug/86630e18-39bd-4a0b-919b-0a10f0886f6b?limit=20"
```

### Example 4: Filter IN Transactions Only
```bash
curl "http://localhost:8000/api/stock-transactions?type=IN&limit=20"
```

### Example 5: Update Transaction Quantity
```bash
curl -X PUT http://localhost:8000/api/stock-transactions/65d80023-d7ca-4d16-9eef-3828bad35a5c \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 75,
    "source": "vendor_correction"
  }'
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Insufficient stock. Available: 50, Requested: 100"
}
```

### 404 Not Found
```json
{
  "detail": "Drug not found"
}
```

### 400 Invalid Type
```json
{
  "detail": "Type must be one of: IN, OUT"
}
```

---

## Stock Calculation Logic

The API automatically manages drug stock levels:

```
Initial Stock = 100

Transaction 1: IN 50 units (vendor)
New Stock = 100 + 50 = 150

Transaction 2: OUT 20 units (prescription)
New Stock = 150 - 20 = 130

Transaction 3: DELETE Transaction 2
New Stock = 130 + 20 = 150 (reversal)
```

---

## Data Validation

| Field | Rules | Notes |
|-------|-------|-------|
| `drug_id` | UUID, must exist in drugs table | Validates on creation |
| `quantity` | Positive integer > 0 | Cannot be zero or negative |
| `type` | 'IN' or 'OUT' only | Case-sensitive |
| `source` | String, max 255 chars | Examples: vendor, prescription, adjustment |
| `created_at` | Auto-generated timestamp | Set at transaction creation |

---

## Integration with Drugs API

Stock transactions automatically update the `Drug.stock_quantity` field:

```bash
# Create a drug with 100 units
POST /api/drugs
{
  "name": "Aspirin",
  "stock_quantity": 100
}

# Add 50 more units
POST /api/stock-transactions
{
  "drug_id": "...",
  "quantity": 50,
  "type": "IN",
  "source": "vendor"
}

# GET /api/drugs/{id} now shows stock_quantity: 150
```

---

## Files Modified/Created

1. **app/models.py**
   - Added `StockTransaction` SQLAlchemy model

2. **app/schemas.py**
   - Added `StockTransactionBase`, `StockTransactionCreate`, `StockTransactionUpdate`, `StockTransactionResponse`, `StockTransactionDetailResponse` Pydantic schemas
   - Updated `DrugCreate` and `DrugResponse` to handle date parsing for `expiry_date`

3. **app/routes.py**
   - Added `stock_transactions_router` with all CRUD endpoints
   - Added imports for StockTransaction model and schemas
   - Integrated router into main application

4. **test_stock_transactions_api.py**
   - Comprehensive test suite for all API endpoints
   - Tests error handling, validation, and stock calculations

---

## Testing

Run the test suite:
```bash
cd /Users/apple/pythonPramith-api/pramith-python-api
source .venv/bin/activate
python test_stock_transactions_api.py
```

All tests should pass with ✓ indicators for each operation.

