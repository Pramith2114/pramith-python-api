# Notifications API - Complete Specification

**API Version:** 1.0  
**Status:** Production Ready  
**Last Updated:** April 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Database Schema](#database-schema)
3. [API Endpoints](#api-endpoints)
4. [Request/Response Examples](#requestresponse-examples)
5. [Error Handling](#error-handling)
6. [Field Validation](#field-validation)
7. [Status Codes](#status-codes)
8. [Integration Points](#integration-points)

---

## Overview

The Notifications API provides a complete system for managing user notifications. It allows applications to:

- Create notifications for users
- Retrieve notifications with advanced filtering and pagination
- Mark notifications as read
- Delete notifications
- Bulk operations for managing all user notifications

**Key Features:**
- UUID-based primary keys for distributed systems
- Automatic timestamping (created_at, updated_at)
- Filterable by type (alert, info, warning, success, error)
- Read status tracking
- User-scoped notification management
- Pagination supports for large result sets

---

## Database Schema

### Notification Table

```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    CHECK (type IN ('alert', 'info', 'warning', 'success', 'error')),
    
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
);
```

### Column Specifications

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique notification identifier |
| user_id | UUID | NOT NULL, FK | Reference to the user |
| title | VARCHAR(255) | NOT NULL | Notification title |
| message | TEXT | NOT NULL | Full notification message content |
| type | VARCHAR(50) | NOT NULL, CHECK | Type: alert, info, warning, success, error |
| is_read | BOOLEAN | DEFAULT FALSE | Read status indicator |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

---

## API Endpoints

### 1. Create Notification

**Endpoint:** `POST /api/notifications`

**Description:** Create a new notification for a user

**Request Body:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Order Confirmed",
  "message": "Your order #12345 has been confirmed and will be delivered within 2-3 days.",
  "type": "success"
}
```

**Success Response:** `201 Created`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Order Confirmed",
  "message": "Your order #12345 has been confirmed and will be delivered within 2-3 days.",
  "type": "success",
  "is_read": false,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

**Error Responses:**
- `404 Not Found`: User does not exist
- `422 Unprocessable Entity`: Invalid type (not in alert, info, warning, success, error)

---

### 2. List All Notifications

**Endpoint:** `GET /api/notifications`

**Description:** Retrieve all notifications with optional filtering and pagination

**Query Parameters:**
- `skip` (integer, default: 0): Offset for pagination
- `limit` (integer, default: 10): Maximum results per page
- `user_id` (UUID, optional): Filter by user ID
- `type` (string, optional): Filter by notification type
- `is_read` (boolean, optional): Filter by read status

**Example Request:**
```
GET /api/notifications?skip=0&limit=10&type=alert&is_read=false
```

**Success Response:** `200 OK`
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Alert: System Maintenance",
    "message": "Scheduled maintenance on 2026-04-20 from 2-4 AM",
    "type": "alert",
    "is_read": false,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

**Notes:**
- Results ordered by creation date (newest first)
- All filters are optional and can be combined
- Pagination helps with performance on large datasets

---

### 3. Get Single Notification

**Endpoint:** `GET /api/notifications/{id}`

**Description:** Retrieve a specific notification by ID

**Path Parameters:**
- `id` (UUID, required): Notification ID

**Success Response:** `200 OK`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Order Confirmed",
  "message": "Your order #12345 has been confirmed.",
  "type": "success",
  "is_read": false,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Notification not found"
}
```

---

### 4. Get User Notifications

**Endpoint:** `GET /api/notifications/user/{user_id}`

**Description:** Retrieve all notifications for a specific user with optional filtering

**Path Parameters:**
- `user_id` (UUID, required): User ID

**Query Parameters:**
- `skip` (integer, default: 0): Offset for pagination
- `limit` (integer, default: 10): Maximum results per page
- `type` (string, optional): Filter by notification type
- `is_read` (boolean, optional): Filter by read status

**Example Request:**
```
GET /api/notifications/user/550e8400-e29b-41d4-a716-446655440000?skip=0&limit=5&type=alert
```

**Success Response:** `200 OK`
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Alert: System Maintenance",
    "message": "Scheduled maintenance...",
    "type": "alert",
    "is_read": false,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User not found"
}
```

---

### 5. Get User Unread Notifications

**Endpoint:** `GET /api/notifications/user/{user_id}/unread`

**Description:** Retrieve unread notifications for a specific user

**Path Parameters:**
- `user_id` (UUID, required): User ID

**Query Parameters:**
- `skip` (integer, default: 0): Offset for pagination
- `limit` (integer, default: 10): Maximum results per page

**Example Request:**
```
GET /api/notifications/user/550e8400-e29b-41d4-a716-446655440000/unread?skip=0&limit=5
```

**Success Response:** `200 OK`
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Order Confirmed",
    "message": "Your order #12345 has been confirmed.",
    "type": "success",
    "is_read": false,
    "created_at": "2026-04-15T10:30:00",
    "updated_at": "2026-04-15T10:30:00"
  }
]
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User not found"
}
```

---

### 6. Update Notification

**Endpoint:** `PUT /api/notifications/{id}`

**Description:** Update a notification's details (title, message, type, is_read)

**Path Parameters:**
- `id` (UUID, required): Notification ID

**Request Body (all fields optional):**
```json
{
  "title": "Updated Title",
  "message": "Updated message content",
  "type": "info",
  "is_read": true
}
```

**Success Response:** `200 OK`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Title",
  "message": "Updated message content",
  "type": "info",
  "is_read": true,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:45:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Notification not found"
}
```

---

### 7. Mark Notification as Read

**Endpoint:** `PUT /api/notifications/{id}/read`

**Description:** Mark a single notification as read

**Path Parameters:**
- `id` (UUID, required): Notification ID

**Request Body:** Empty (no body required)

**Success Response:** `200 OK`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Order Confirmed",
  "message": "Your order #12345 has been confirmed.",
  "type": "success",
  "is_read": true,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:45:00"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Notification not found"
}
```

---

### 8. Mark All User Notifications as Read

**Endpoint:** `PUT /api/notifications/user/{user_id}/read-all`

**Description:** Mark all unread notifications for a user as read

**Path Parameters:**
- `user_id` (UUID, required): User ID

**Request Body:** Empty (no body required)

**Success Response:** `200 OK`
```json
{
  "message": "Marked 5 notification(s) as read"
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "User not found"
}
```

---

### 9. Delete Notification

**Endpoint:** `DELETE /api/notifications/{id}`

**Description:** Delete a single notification

**Path Parameters:**
- `id` (UUID, required): Notification ID

**Success Response:** `204 No Content`

**Error Response:** `404 Not Found`
```json
{
  "detail": "Notification not found"
}
```

---

### 10. Delete All User Notifications

**Endpoint:** `DELETE /api/notifications/user/{user_id}/all`

**Description:** Delete all notifications for a specific user

**Path Parameters:**
- `user_id` (UUID, required): User ID

**Success Response:** `204 No Content`

**Error Response:** `404 Not Found`
```json
{
  "detail": "User not found"
}
```

---

## Request/Response Examples

### Complete Workflow Example

#### Step 1: Create notification for user
```bash
curl -X POST http://localhost:8000/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Payment Received",
    "message": "Payment of $100 received for invoice #INV-001",
    "type": "success"
  }'
```

#### Step 2: Get user's unread notifications
```bash
curl http://localhost:8000/api/notifications/user/550e8400-e29b-41d4-a716-446655440000/unread
```

#### Step 3: Mark specific notification as read
```bash
curl -X PUT http://localhost:8000/api/notifications/660e8400-e29b-41d4-a716-446655440001/read
```

#### Step 4: Get updated notification
```bash
curl http://localhost:8000/api/notifications/660e8400-e29b-41d4-a716-446655440001
```

---

## Error Handling

### Common HTTP Status Codes

| Status Code | Meaning | Common Causes |
|------------|---------|---------------|
| 200 OK | Successful GET request | Notification exists |
| 201 Created | Resource created successfully | POST request successful |
| 204 No Content | Successful DELETE request | Notification deleted |
| 400 Bad Request | Invalid input format | Malformed JSON, invalid UUID format |
| 404 Not Found | Resource not found | Notification ID doesn't exist or user not found |
| 422 Unprocessable Entity | Validation failed | Invalid notification type |

### Error Response Example

```json
{
  "detail": "Notification not found"
}
```

---

## Field Validation

### Title
- **Type:** String
- **Max Length:** 255 characters
- **Required:** Yes
- **Examples:** "Order Shipped", "Payment Confirmed", "System Alert"

### Message
- **Type:** Text
- **Max Length:** No limit (TEXT type)
- **Required:** Yes
- **Examples:** "Your order will be delivered within 2-3 days", "Your payment has been processed successfully"

### Type
- **Type:** String (Enum)
- **Valid Values:** `alert`, `info`, `warning`, `success`, `error`
- **Required:** Yes
- **Constraints:** CHECK constraint ensures only valid types

| Type | Use Case |
|------|----------|
| alert | Urgent alerts requiring immediate attention |
| info | General informational messages |
| warning | Warnings about potential issues |
| success | Successful operation confirmations |
| error | Error notifications |

### is_read
- **Type:** Boolean
- **Default:** false
- **Required:** No
- **Description:** Tracks whether user has read the notification

---

## Status Codes

### Success Codes
- **200 OK** - Successful GET or PUT request
- **201 Created** - Notification successfully created
- **204 No Content** - Successful DELETE request

### Client Error Codes
- **400 Bad Request** - Malformed request (invalid JSON, invalid UUID)
- **404 Not Found** - Notification or user does not exist
- **422 Unprocessable Entity** - Validation failed (invalid type value)

### Server Error Codes
- **500 Internal Server Error** - Unexpected server error
- **503 Service Unavailable** - Database or service unavailable

---

## Integration Points

### Related APIs

The Notifications API integrates with:

1. **User API** (`/api/users`)
   - All notifications require a valid user_id
   - Notifications are deleted when user is deleted (if cascading)

2. **Appointments API** (`/api/appointments`)
   - Create notifications for appointment confirmations, reminders, cancellations

3. **Prescriptions API** (`/api/prescriptions`)
   - Create notifications for prescription updates

4. **Payments API** (`/api/payments`)
   - Create notifications for payment confirmations, failures, refunds

5. **Medical Records API** (`/api/medical-records`)
   - Create notifications for new medical records

### Recommended Notification Flow

```
Event Triggers → Create Notification → User Retrieves → Mark as Read → Delete
```

**Example:** Payment received → Create success notification → User sees unread count → Views notification → Marks as read → Optionally deletes

---

## Pagination Guidelines

When retrieving multiple notifications:
- Default `limit=10` is suitable for most use cases
- Use `skip` parameter to navigate through pages
- Calculate pages: `current_page = skip / limit`

**Example - Page 2 with 10 items per page:**
```
GET /api/notifications?skip=10&limit=10
```

---

## Performance Considerations

1. **Indexing:** Key columns (user_id, type, is_read, created_at) are indexed
2. **Pagination:** Always use limit parameter to prevent large result sets
3. **Filtering:** Filtering by user_id and is_read is most efficient
4. **Batch Operations:** Use `/read-all` and `/all` endpoints for bulk operations

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | April 2026 | Initial implementation with 10 endpoints |

---

**End of Notifications API Specification**
