# User API - Visual Implementation Guide

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │        User API Routes (app/routes.py)             │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ POST   /api/users              CREATE user         │ │
│  │ GET    /api/users              LIST users          │ │
│  │ GET    /api/users/{id}         GET user by ID      │ │
│  │ GET    /api/users/mobile/{m}   GET by mobile       │ │
│  │ PUT    /api/users/{id}         UPDATE user         │ │
│  │ DELETE /api/users/{id}         DELETE user         │ │
│  │ POST   /api/users/{id}/verify  VERIFY user         │ │
│  └────────────────────────────────────────────────────┘ │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │    Pydantic Schemas (app/schemas.py)               │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ • UserCreate (registration)                        │ │
│  │ • UserResponse (API response)                      │ │
│  │ • UserUpdate (update payload)                      │ │
│  │ • UserInDB (database model)                        │ │
│  └────────────────────────────────────────────────────┘ │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │    SQLAlchemy Model (app/models.py)                │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ class User(Base):                                  │ │
│  │   id: UUID (Primary Key)                           │ │
│  │   name: String (optional)                          │ │
│  │   mobile: String (unique, optional)                │ │
│  │   email: String (optional)                         │ │
│  │   password_hash: Text                              │ │
│  │   role: String (patient|doctor|admin|vendor)       │ │
│  │   is_verified: Boolean (default=False)             │ │
│  │   created_at: DateTime                             │ │
│  └────────────────────────────────────────────────────┘ │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │        PostgreSQL Database Connection              │ │
│  │        (app/database.py)                           │ │
│  └────────────────────────────────────────────────────┘ │
│                         ▼                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │          USERS Table (PostgreSQL)                  │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ id (UUID PK) │ name │ mobile (UQ) │ email          │ │
│  │ password_hash │ role (CHK) │ is_verified │ created_at │
│  └────────────────────────────────────────────────────┘ │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Diagram

```
┌─────────────┐
│   Client    │
│ (Browser,   │
│  cURL,      │
│  Python)    │
└──────┬──────┘
       │
       │ HTTP Request
       ▼
┌──────────────────────────────────────┐
│      FastAPI Router                  │
│   (app/routes.py)                    │
│  - Receives request                  │
│  - Validates input                   │
│  - Calls handlers                    │
└──────┬───────────────────────────────┘
       │
       │ Validated Data
       ▼
┌──────────────────────────────────────┐
│   Route Handler (e.g., create_user)  │
│  - Business logic                    │
│  - Password hashing (bcrypt)         │
│  - Duplicate detection               │
│  - Database operations               │
└──────┬───────────────────────────────┘
       │
       │ SQLAlchemy ORM
       ▼
┌──────────────────────────────────────┐
│      Database Layer                  │
│  (app/database.py, SQLAlchemy)       │
│  - Connection pooling                │
│  - Transaction management            │
│  - Session handling                  │
└──────┬───────────────────────────────┘
       │
       │ SQL Queries
       ▼
┌──────────────────────────────────────┐
│     PostgreSQL Database              │
│  - Execute SQL                       │
│  - Return results                    │
│  - Maintain integrity                │
└──────┬───────────────────────────────┘
       │
       │ Data (dict/objects)
       ▼
┌──────────────────────────────────────┐
│   Pydantic Schema (UserResponse)     │
│  - Serialize to JSON                 │
│  - Validate output                   │
│  - Exclude sensitive fields          │
└──────┬───────────────────────────────┘
       │
       │ JSON Response
       ▼
┌──────────────────────────────────────┐
│  HTTP Response (200, 201, 400, 404)  │
│  (Back to Client)                    │
└──────────────────────────────────────┘
```

## 🔄 User Lifecycle

```
1. REGISTRATION (POST /api/users)
   ┌─────────────────────────────┐
   │ User submits:               │
   │ • name, mobile, email       │
   │ • password                  │
   │ • role                      │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ • Validate email format     │
   │ • Check mobile uniqueness   │
   │ • Hash password w/ bcrypt   │
   │ • Create user in DB         │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Return: User + UUID         │
   │ is_verified = false         │
   └─────────────────────────────┘

2. VERIFICATION (POST /api/users/{id}/verify)
   ┌─────────────────────────────┐
   │ Admin/System marks user     │
   │ as verified                 │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Set is_verified = true      │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Return updated user info    │
   └─────────────────────────────┘

3. READ (GET /api/users/{id})
   ┌─────────────────────────────┐
   │ Fetch user by UUID          │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Return user (no password)   │
   └─────────────────────────────┘

4. UPDATE (PUT /api/users/{id})
   ┌─────────────────────────────┐
   │ User can update:            │
   │ • name                      │
   │ • email                     │
   │ • role                      │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Validate changes            │
   │ Check email uniqueness      │
   │ Update in DB                │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Return updated user         │
   └─────────────────────────────┘

5. DELETE (DELETE /api/users/{id})
   ┌─────────────────────────────┐
   │ Delete user by UUID         │
   └──────────┬──────────────────┘
              ▼
   ┌─────────────────────────────┐
   │ Remove from database        │
   │ Return 204 No Content       │
   └─────────────────────────────┘
```

## 🗂️ Project Structure

```
pramith-python-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py              ← FastAPI app setup
│   ├── config.py            ← Configuration/settings
│   ├── database.py          ← DB connection & session
│   ├── models.py            ← SQLAlchemy models (MODIFIED)
│   │   └── User (UUID PK)
│   ├── schemas.py           ← Pydantic schemas (MODIFIED)
│   │   ├── UserCreate
│   │   ├── UserResponse
│   │   ├── UserUpdate
│   │   └── UserInDB
│   ├── routes.py            ← API endpoints (MODIFIED)
│   │   ├── POST /api/users
│   │   ├── GET /api/users
│   │   ├── GET /api/users/{id}
│   │   ├── GET /api/users/mobile/{m}
│   │   ├── PUT /api/users/{id}
│   │   ├── DELETE /api/users/{id}
│   │   └── POST /api/users/{id}/verify
│   ├── auth.py              ← Authentication logic
│   └── utils.py             ← Utility functions
│
├── tests/                   ← Test suite
│   └── test_main.py
│
├── scripts/                 ← Utility scripts
│   └── ...
│
├── Documentation/
│   ├── README_USER_API.md              ← Quick start (NEW)
│   ├── USER_API_DOCS.md                ← Full docs (NEW)
│   ├── USER_API_QUICK_REFERENCE.md     ← Quick ref (NEW)
│   ├── USER_API_IMPLEMENTATION_SUMMARY.md ← Summary (NEW)
│   ├── SETUP_USER_API.md               ← Setup guide (NEW)
│   └── Other documentation...
│
├── test_user_api.py         ← Test suite (NEW)
├── requirements.txt         ← Dependencies
├── .env                     ← Environment config
└── README.md
```

## 🔐 Security Implementation

```
PASSWORD FLOW:
┌──────────────────────────────────────────────────┐
│ 1. User enters password: "mysecret123"           │
└────────┬─────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│ 2. Validate: min 6 chars ✓                       │
└────────┬─────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│ 3. Hash with bcrypt + salt:                      │
│    bcrypt.hashpw(password.encode(),              │
│                  bcrypt.gensalt())               │
│                                                  │
│    $2b$12$... (60 characters)                    │
└────────┬─────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│ 4. Store hash in database (password_hash field)  │
└────────┬─────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│ 5. Return UserResponse (NO password in response) │
└──────────────────────────────────────────────────┘

DUPLICATE DETECTION:
┌──────────────────────────────────────────────────┐
│ Before inserting new user:                       │
│ 1. Query: SELECT * FROM users                    │
│    WHERE mobile = ?                              │
│    → If exists: Error 400 (duplicate)            │
│                                                  │
│ 2. Query: SELECT * FROM users                    │
│    WHERE email = ?                               │
│    → If exists: Error 400 (duplicate)            │
│                                                  │
│ 3. If both OK: INSERT new user                   │
└──────────────────────────────────────────────────┘
```

## 📈 Database Relations

```
USERS Table:
┌─────────┬──────────┬──────────┬───────────┬───────────┬───────┬──────────────┬────────────┐
│  id     │  name    │  mobile  │  email    │ pwd_hash  │ role  │ is_verified  │ created_at │
│  (UUID) │ (String) │ (String) │ (String)  │ (Text)    │ (PK)  │ (Boolean)    │ (DateTime) │
├─────────┼──────────┼──────────┼───────────┼───────────┼───────┼──────────────┼────────────┤
│ 550e... │ John Doe │ 987654.. │ john@..   │ $2b$12... │ ptnт  │ false        │ 2024-04-14 │
│ 550e... │ Dr. Jane │ 987654.. │ jane@..   │ $2b$12... │ dctr  │ true         │ 2024-04-14 │
│ 550e... │ Admin    │ 987654.. │ admin@..  │ $2b$12... │ adm   │ true         │ 2024-04-14 │
└─────────┴──────────┴──────────┴───────────┴───────────┴───────┴──────────────┴────────────┘

INDEXES:
├─ PRIMARY KEY: id (UUID)
├─ UNIQUE: mobile (for fast mobile lookup)
├─ INDEX: created_at (for sorting)
└─ CHECK: role IN ('patient', 'doctor', 'admin', 'vendor')
```

## 📝 API Request/Response Flow

```
CLIENT REQUEST:
┌─────────────────────────────────────┐
│ POST /api/users                     │
│ Content-Type: application/json      │
│                                     │
│ {                                   │
│   "name": "John",                   │
│   "mobile": "9876543210",           │
│   "email": "john@example.com",      │
│   "password": "secret123",          │
│   "role": "patient"                 │
│ }                                   │
└─────────────┬───────────────────────┘
              │
      VALIDATION LAYER
              │
              ▼
┌─────────────────────────────────────┐
│ Pydantic Validation:                │
│ ✓ email format (if provided)        │
│ ✓ password min length (6)           │
│ ✓ role value check                  │
│ ✓ Required fields present           │
└─────────────┬───────────────────────┘
              │
      BUSINESS LOGIC LAYER
              │
              ▼
┌─────────────────────────────────────┐
│ create_user handler:                │
│ ✓ Check mobile uniqueness           │
│ ✓ Check email uniqueness            │
│ ✓ Hash password with bcrypt         │
│ ✓ Insert into database              │
└─────────────┬───────────────────────┘
              │
        DATABASE LAYER
              │
              ▼
┌─────────────────────────────────────┐
│ INSERT INTO users VALUES (...)      │
│ Return: created user object         │
└─────────────┬───────────────────────┘
              │
      SERIALIZATION LAYER
              │
              ▼
┌─────────────────────────────────────┐
│ UserResponse schema:                │
│ {                                   │
│   "id": "550e8400-...",            │
│   "name": "John",                   │
│   "mobile": "9876543210",           │
│   "email": "john@example.com",      │
│   "role": "patient",                │
│   "is_verified": false,             │
│   "created_at": "2024-04-14T10:.."  │
│ }                                   │
│ (NO password_hash returned)         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│ HTTP 201 Created                    │
│ Return JSON above                   │
└─────────────────────────────────────┘
```

## 🎯 Complete Feature Checklist

```
✅ CRUD Operations
   ✓ Create user (POST /api/users)
   ✓ Read user (GET /api/users/{id})
   ✓ Update user (PUT /api/users/{id})
   ✓ Delete user (DELETE /api/users/{id})
   ✓ List all users (GET /api/users)

✅ Advanced Queries
   ✓ Get user by mobile (GET /api/users/mobile/{mobile})
   ✓ Filter by role (GET /api/users?role=doctor)
   ✓ Pagination (skip, limit)

✅ Security
   ✓ Bcrypt password hashing
   ✓ Duplicate mobile detection
   ✓ Duplicate email detection
   ✓ Role validation
   ✓ Password minimum length enforcement

✅ Data Management
   ✓ UUID primary key
   ✓ Automatic timestamps
   ✓ Transaction support
   ✓ Referential integrity

✅ Documentation
   ✓ Full API docs (USER_API_DOCS.md)
   ✓ Setup guide (SETUP_USER_API.md)
   ✓ Quick reference (USER_API_QUICK_REFERENCE.md)
   ✓ Implementation summary

✅ Testing
   ✓ Comprehensive test suite
   ✓ All endpoints covered
   ✓ Edge cases tested
   ✓ Duplicate detection verified

✅ Database
   ✓ Automatic table creation
   ✓ PostgreSQL compatible
   ✓ AWS RDS compatible
   ✓ UUID support
```

## 🚀 Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure database (.env)
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# 3. Start server
uvicorn app.main:app --reload

# 4. Test API
# Option A: Use interactive docs
# → Visit: http://localhost:8000/docs

# Option B: Run test suite
python test_user_api.py

# Option C: Use curl
curl -X GET http://localhost:8000/api/users
```

## 📊 Success Indicators

Once running, you should see:
1. ✅ FastAPI server starts on http://localhost:8000
2. ✅ "Database tables created" message on startup
3. ✅ Swagger UI available at /docs
4. ✅ All endpoints responding (test with curl or browser)
5. ✅ Test suite passes (python test_user_api.py)

---

**You're all set!** 🎉 The User API is ready to use!

