# User API Setup Guide

## What Was Created

A complete User API with the following components:

### 1. Database Table
- **Table**: `users`
- **Primary Key**: UUID (auto-generated)
- **Fields**:
  - `id`: UUID (Primary Key)
  - `name`: VARCHAR (optional)
  - `mobile`: VARCHAR (unique, optional)
  - `email`: VARCHAR (optional)
  - `password_hash`: TEXT
  - `role`: VARCHAR with CHECK constraint (patient, doctor, admin, vendor)
  - `is_verified`: BOOLEAN (default: false)
  - `created_at`: TIMESTAMP

### 2. SQLAlchemy Model
Location: `app/models.py`
- User model with UUID primary key
- Automatic timestamp generation
- Role-based access control with validation

### 3. Pydantic Schemas
Location: `app/schemas.py`
- `UserCreate`: For creating new users
- `UserResponse`: For API responses
- `UserUpdate`: For updating user information
- `UserInDB`: For database operations

### 4. API Routes
Location: `app/routes.py`

**User Endpoints:**
- `POST /api/users` - Create new user
- `GET /api/users` - Get all users (with optional role filter)
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/mobile/{mobile}` - Get user by mobile
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user
- `POST /api/users/{user_id}/verify` - Mark user as verified

**Features:**
- Password hashing with bcrypt
- Duplicate mobile/email detection
- Role-based validation
- Full CRUD operations

## Getting Started

### 1. Install Dependencies

Make sure all required packages are installed:

```bash
cd /Users/apple/pythonPramith-api/pramith-python-api
pip install -r requirements.txt
```

Required packages include:
- fastapi
- sqlalchemy
- psycopg2-binary (PostgreSQL driver)
- passlib[bcrypt] (Password hashing)
- pydantic-settings

### 2. Configure Database

Ensure your `.env` file has the database configuration:

```bash
# Standard PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# OR AWS RDS with password authentication
USE_AWS_RDS=true
RDS_HOST=your-rds-endpoint.amazonaws.com
RDS_PORT=5432
RDS_USERNAME=postgres
RDS_PASSWORD=your_password
RDS_DATABASE=postgres

# OR AWS RDS with IAM Authentication
USE_AWS_RDS=true
RDS_HOST=your-rds-endpoint.amazonaws.com
RDS_PORT=5432
RDS_USERNAME=your_iam_user
RDS_DATABASE=postgres
USE_IAM_AUTH=true
AWS_REGION=us-east-1
```

### 3. Start the Application

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Run the FastAPI server
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

The tables will be automatically created on startup.

### 4. Verify Installation

Open your browser and visit:
- API Documentation: http://localhost:8000/docs (Swagger UI)
- Alternative Docs: http://localhost:8000/redoc

## API Usage Examples

### Create a User

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "mobile": "9876543210",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "patient"
  }'
```

### Get All Users

```bash
curl http://localhost:8000/api/users
```

### Get Users by Role

```bash
curl http://localhost:8000/api/users?role=doctor
```

### Get User by ID

```bash
curl http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000
```

### Get User by Mobile

```bash
curl http://localhost:8000/api/users/mobile/9876543210
```

### Update User

```bash
curl -X PUT http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "role": "doctor",
    "email": "newemail@example.com"
  }'
```

### Verify User

```bash
curl -X POST http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/verify
```

### Delete User

```bash
curl -X DELETE http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000
```

## Test the API

### Automated Test Suite

Run the comprehensive test suite:

```bash
# Make sure the server is running in another terminal
python test_user_api.py
```

This will:
- Create multiple users with different roles
- Test all CRUD operations
- Test filtering and search operations
- Verify duplicate detection
- Display formatted results

### Manual Testing with Swagger UI

1. Open http://localhost:8000/docs in your browser
2. Expand the `/api/users` endpoints
3. Click "Try it out" on any endpoint
4. Fill in the request body/parameters
5. Click "Execute"

## Password Security

- Passwords are hashed using **bcrypt** before storage
- Minimum password length: 6 characters
- Passwords are never returned in API responses
- Use HTTPS in production to encrypt data in transit

## User Roles

Four predefined roles are available:

| Role   | Description |
|--------|-------------|
| patient | Regular patient user |
| doctor | Medical professional |
| admin | System administrator |
| vendor | Service provider |

## Files Modified

1. **app/models.py**
   - Updated User model with UUID and new fields

2. **app/schemas.py**
   - Added UserCreate, UserUpdate, UserResponse schemas

3. **app/routes.py**
   - Added complete user API endpoints
   - Added password hashing functions

4. **USER_API_DOCS.md** (New)
   - Comprehensive API documentation

5. **test_user_api.py** (New)
   - Automated test suite

6. **SETUP_USER_API.md** (New)
   - This setup guide

## Troubleshooting

### Database Connection Issues

If you get database connection errors:

```python
# Verify database configuration
python -c "from app.config import settings; print(settings.DATABASE_URL)"
```

### Module Import Errors

If you get import errors, make sure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### UUID Issues in PostgreSQL

If PostgreSQL doesn't support UUID, install the uuid extension:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### bcrypt Installation Issues

If bcrypt fails to install:

```bash
pip install bcrypt --no-cache-dir
```

## Performance Considerations

1. **Indexing**: Mobile and ID fields are indexed for fast lookups
2. **Pagination**: Use `skip` and `limit` parameters for large datasets
3. **Role Filtering**: Filter by role in the API to reduce data transfer
4. **Connection Pooling**: SQLAlchemy handles connection pooling automatically

## Next Steps

1. Implement authentication/JWT tokens
2. Add role-based access control (RBAC)
3. Implement email verification flow
4. Add OTP verification for mobile
5. Implement password recovery
6. Add audit logging
7. Set up API rate limiting
8. Add comprehensive error handling

## Support

For API documentation, see `USER_API_DOCS.md`

For detailed endpoint information, visit the Swagger UI at `/docs` when the server is running.

