# OTP Verification API - Visual Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATION                   │
│  (Mobile App, Web App, Desktop App)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP Requests
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   FASTAPI SERVER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        OTP Verification API Routes                   │  │
│  │  - POST   /api/otp-verification      (Create)       │  │
│  │  - GET    /api/otp-verification      (List)         │  │
│  │  - GET    /api/otp-verification/{id} (Get by ID)    │  │
│  │  - GET    /api/otp-verification/by-mobile/{mobile}  │  │
│  │  - POST   /api/otp-verification/verify (Verify)     │  │
│  │  - PUT    /api/otp-verification/{id} (Update)       │  │
│  │  - DELETE /api/otp-verification/{id} (Delete)       │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                   │
│                          │ ORM Queries                       │
│                          │                                   │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │         SQLAlchemy ORM Layer                        │   │
│  │    (Database Models & Session Management)          │   │
│  └──────────────────────┬──────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ SQL Queries
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  PostgreSQL Database                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  otp_verifications                                   │  │
│  │  ├─ id (UUID, PK)                                   │  │
│  │  ├─ mobile (VARCHAR, Indexed)                       │  │
│  │  ├─ otp (VARCHAR)                                   │  │
│  │  ├─ expires_at (TIMESTAMP, Indexed)                 │  │
│  │  ├─ is_verified (BOOLEAN, Indexed)                  │  │
│  │  ├─ created_at (TIMESTAMP, Indexed)                 │  │
│  │  └─ updated_at (TIMESTAMP)                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## User Authentication Flow with OTP

```
┌─────────┐
│  START  │
└────┬────┘
     │
     ▼
┌──────────────────────────────────────────┐
│ 1. User Enters Mobile Number             │
│    POST /api/otp-verification            │
│    {                                     │
│      "mobile": "+919876543210",          │
│      "otp": "123456",                    │
│      "expires_at": "2026-04-16T12:30"    │
│    }                                     │
└────┬─────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────┐
│ 2. OTP Stored in Database                │
│    - id: UUID                            │
│    - mobile: entered number              │
│    - otp: generated code                 │
│    - is_verified: false                  │
│    - expires_at: +10 minutes             │
└────┬─────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────┐
│ 3. Send OTP via SMS                      │
│    (Integration with SMS service)        │
└────┬─────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────┐
│ 4. User Receives OTP & Enters Code       │
│    POST /api/otp-verification/verify     │
│    {                                     │
│      "mobile": "+919876543210",          │
│      "otp": "123456"                     │
│    }                                     │
└────┬─────────────────────────────────────┘
     │
     ├─── OTP Valid & Not Expired ───┐
     │                                │
     ▼                                ▼
┌──────────────────────────┐    ┌──────────────┐
│ 5. OTP Verified          │    │ OTP Invalid  │
│ - is_verified: true      │    │ Show Error   │
│ - Return success = true  │    │ message      │
└────┬─────────────────────┘    └──────────────┘
     │                                │
     ▼                                │
┌──────────────────────────────────────────┐
│ 6. Create User Account / Login User      │
│    - Generate access token               │
│    - Return user details                 │
└────┬─────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────┐
│ 7. User Authenticated                    │
│    Access granted to app                 │
└──────────────────────────────────────────┘
```

## Request-Response Flow

```
CLIENT                          SERVER                          DATABASE
  │                               │                               │
  │ 1. Create OTP                 │                               │
  ├──────────────────────────────►│                               │
  │  POST /api/otp-verification   │                               │
  │  { mobile, otp, expires_at }  │                               │
  │                               │ 2. Validate Input             │
  │                               ├─────────────────┐             │
  │                               │                 │             │
  │                               │◄────────────────┘             │
  │                               │                               │
  │                               │ 3. Check Existing OTP         │
  │                               ├──────────────────────────────►│
  │                               │     SELECT * WHERE mobile     │
  │                               │◄──────────────────────────────┤
  │                               │                               │
  │                               │ 4. Insert New Record          │
  │                               ├──────────────────────────────►│
  │                               │     INSERT INTO ...           │
  │                               │◄──────────────────────────────┤
  │                               │                               │
  │◄──────────────────────────────┤                               │
  │ 201 Created + OTP Record      │                               │
  │ { id, mobile, expires_at... } │                               │
  │                               │                               │
  │ [OTP sent via SMS]            │                               │
  │                               │                               │
  │ 5. Verify OTP                 │                               │
  ├──────────────────────────────►│                               │
  │ POST /api/otp-verification/   │                               │
  │       verify                  │                               │
  │ { mobile, otp }               │                               │
  │                               │ 6. Query OTP Record          │
  │                               ├──────────────────────────────►│
  │                               │     SELECT * WHERE mobile     │
  │                               │◄──────────────────────────────┤
  │                               │                               │
  │                               │ 7. Validate:                 │
  │                               │    - Not expired?            │
  │                               │    - OTP matches?            │
  │                               │                               │
  │                               │ 8. Update is_verified        │
  │                               ├──────────────────────────────►│
  │                               │  UPDATE is_verified = true   │
  │                               │◄──────────────────────────────┤
  │◄──────────────────────────────┤                               │
  │ 200 OK                        │                               │
  │ { success: true, is_verified: │                               │
  │   true, message: "Verified" } │                               │
  │                               │                               │
```

## Data Lifecycle

```
┌─────────────┐
│  CREATE OTP │  
└────┬────────┘
     │
     │ INSERT INTO otp_verifications
     │ (id, mobile, otp, expires_at, is_verified, created_at, updated_at)
     │ VALUES (...)
     │
     ▼
┌────────────────────┐
│ OTP STORED         │  
│ is_verified: false │  (Inactive state)
│ expires_at: T+10m  │
└────┬───────────────┘
     │
     │ [User receives OTP]
     │ [User submits OTP for verification]
     │
     │ POST /verify with mobile + otp
     │
     ▼
     │
     ├─ OTP Valid & Not Expired?
     │
     ├──YES── UPDATE is_verified = true ───┐
     │                                      │
     │                                      ▼
     │                                   ┌─────────────────┐
     │                                   │ OTP VERIFIED    │  
     │                                   │ is_verified: true│ (Active - Confirmed)
   ├─NO─── Return error ────────┐      └─────────────────┘
     │                          │         │
     ▼                          ▼         │
┌──────────────────┐     ┌───────────────┼──────────────┐
│ EXPIRED/INVALID  │     │ User authenticated/registered│
│ Show user error  │     │ Grant access/process signup │
└──────────────────┘     └───────────────┬──────────────┘
                                         │
                                         │ Time passes...
                                         │ 
                                         ▼
                              ┌──────────────────────┐
                              │ CLEANUP (Optional)   │  
                              │ - Delete old records │
                              │ - Archive verified   │
                              │   OTPs              │
                              └──────────────────────┘
```

## Query Performance - Index Usage

```
REQUEST                          INDEX USED               QUERY TIME
────────────────────────────────────────────────────────────────────
GET /by-mobile/{mobile}     ──► idx_mobile          O(log n)
    WHERE mobile = X

GET /?is_verified=false     ──► idx_is_verified     O(log n)
    WHERE is_verified = false

GET /?expires_at>now()      ──► idx_expires_at      O(log n)
    WHERE expires_at > NOW()

GET /created_at>date        ──► idx_created_at      O(log n)
    WHERE created_at > DATE

VERIFY /mobile + otp        ──► idx_mobile          O(log n)
    WHERE mobile = X AND
    expires_at > NOW()

GET /?skip=X&limit=Y        ──► Multiple Indexes    O(k*log n)
    WHERE is_verified = Z
```

## API Response Status Flow

```
REQUEST RECEIVED
       │
       ▼
   VALIDATE INPUT ──[ERROR]──► 422 Unprocessable Entity
       │                       │
    [OK] ──┐                   return error
       │   │
       ▼   │
   QUERY DB ──[NOT FOUND]──► 404 Not Found
       │   │                │
    [OK] │   return error
       │   │
       ▼   │
   BUSINESS LOGIC ──[ERROR]──► 400 Bad Request
       │                       │
    [OK]                       return error
       │
       ▼
   MODIFY/CREATE ──[ERROR]──► 500 Internal Error
       │                       │
    [OK]                       return error
       │
       ▼
   COMMIT/RESPOND ──► 200/201/204 Success
                     + Response Body
```

## Mobile Number Validation Pattern

```
Pattern: ^\+?1?\d{9,15}$

Examples:
✓ +919876543210         (India with country code)
✓ +14155552671          (USA with country code)
✓ 9876543210            (India without code, 10 digits)
✓ 14155552671           (USA without code, 10 digits)
✓ +1234567890           (Generic with prefix)

✗ 123                   (Too short)
✗ abc9876543210         (Contains letters)
✗ +91-98765-43210       (Contains special chars except +)
```

## Feature Implementation Timeline

```
PHASE 1: Core API (✓ Completed)
├─ Create OTP
├─ Verify OTP
├─ Get OTP by ID
├─ Get OTP by Mobile
├─ Update OTP
└─ Delete OTP

PHASE 2: Enhancement (Recommended)
├─ SMS Integration
├─ Rate Limiting
├─ Audit Logging
├─ Cleanup Job
└─ Email Fallback

PHASE 3: Advanced Features
├─ Retry Logic
├─ Multi-factor Auth
├─ OTP Templates
├─ Analytics
└─ Performance Optimization
```

## Notes

- All timestamps are in UTC format
- UUIDs are PostgreSQL native UUIDs
- OTP strings can be numeric or alphanumeric
- Mobile numbers follow E.164 international format
- Indexes improve query performance significantly
- Delete expired OTPs periodically to manage database size
