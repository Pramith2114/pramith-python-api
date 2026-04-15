# Notifications API - Quick Reference

**Version:** 1.0 | **Status:** Production Ready | **Last Updated:** April 2026

---

## Endpoint Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| **POST** | `/api/notifications` | Create notification |
| **GET** | `/api/notifications` | List all notifications (with filters) |
| **GET** | `/api/notifications/{id}` | Get single notification |
| **GET** | `/api/notifications/user/{user_id}` | Get user's notifications |
| **GET** | `/api/notifications/user/{user_id}/unread` | Get unread notifications |
| **PUT** | `/api/notifications/{id}` | Update notification |
| **PUT** | `/api/notifications/{id}/read` | Mark as read |
| **PUT** | `/api/notifications/user/{user_id}/read-all` | Mark all as read |
| **DELETE** | `/api/notifications/{id}` | Delete notification |
| **DELETE** | `/api/notifications/user/{user_id}/all` | Delete all user notifications |

---

## cURL Examples

### Create Notification
```bash
curl -X POST http://localhost:8000/api/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Order Confirmed",
    "message": "Your order has been confirmed",
    "type": "success"
  }'
```

### List All Notifications
```bash
curl http://localhost:8000/api/notifications?skip=0&limit=10
```

### List with Filters
```bash
# Unread alerts for specific user
curl "http://localhost:8000/api/notifications?user_id=550e8400-e29b-41d4-a716-446655440000&type=alert&is_read=false"
```

### Get Single Notification
```bash
curl http://localhost:8000/api/notifications/660e8400-e29b-41d4-a716-446655440001
```

### Get User's Notifications
```bash
curl http://localhost:8000/api/notifications/user/550e8400-e29b-41d4-a716-446655440000
```

### Get Unread Count
```bash
curl "http://localhost:8000/api/notifications/user/550e8400-e29b-41d4-a716-446655440000/unread?limit=100"
```

### Mark as Read
```bash
curl -X PUT http://localhost:8000/api/notifications/660e8400-e29b-41d4-a716-446655440001/read
```

### Mark All as Read
```bash
curl -X PUT http://localhost:8000/api/notifications/user/550e8400-e29b-41d4-a716-446655440000/read-all
```

### Update Notification
```bash
curl -X PUT http://localhost:8000/api/notifications/660e8400-e29b-41d4-a716-446655440001 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title",
    "is_read": true
  }'
```

### Delete Notification
```bash
curl -X DELETE http://localhost:8000/api/notifications/660e8400-e29b-41d4-a716-446655440001
```

### Delete All User Notifications
```bash
curl -X DELETE http://localhost:8000/api/notifications/user/550e8400-e29b-41d4-a716-446655440000/all
```

---

## Python Examples

### Create Notification
```python
import httpx
import uuid

client = httpx.Client()

response = client.post(
    "http://localhost:8000/api/notifications",
    json={
        "user_id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Order Shipped",
        "message": "Your order has been shipped",
        "type": "success"
    }
)
print(response.json())
```

### Get User's Unread Notifications
```python
user_id = "550e8400-e29b-41d4-a716-446655440000"
response = client.get(
    f"http://localhost:8000/api/notifications/user/{user_id}/unread"
)
notifications = response.json()
print(f"Unread: {len(notifications)}")
```

### Mark Notification as Read
```python
notification_id = "660e8400-e29b-41d4-a716-446655440001"
response = client.put(
    f"http://localhost:8000/api/notifications/{notification_id}/read"
)
print(response.status_code)  # 200
```

### List Alerts (Unread)
```python
response = client.get(
    "http://localhost:8000/api/notifications",
    params={
        "type": "alert",
        "is_read": False,
        "limit": 20
    }
)
alerts = response.json()
```

---

## JavaScript Examples

### Create Notification
```javascript
const createNotification = async () => {
  const response = await fetch('http://localhost:8000/api/notifications', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: '550e8400-e29b-41d4-a716-446655440000',
      title: 'Payment Received',
      message: 'Payment of $100 received',
      type: 'success'
    })
  });
  return await response.json();
};
```

### Get Unread Count
```javascript
const getUnreadCount = async (userId) => {
  const response = await fetch(
    `http://localhost:8000/api/notifications/user/${userId}/unread?limit=100`
  );
  const notifications = await response.json();
  return notifications.length;
};
```

### Mark All as Read
```javascript
const markAllAsRead = async (userId) => {
  const response = await fetch(
    `http://localhost:8000/api/notifications/user/${userId}/read-all`,
    { method: 'PUT' }
  );
  return await response.json();
};
```

---

## Response Schemas

### Notification Object
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "String (max 255)",
  "message": "Text (any length)",
  "type": "alert|info|warning|success|error",
  "is_read": false,
  "created_at": "2026-04-15T10:30:00",
  "updated_at": "2026-04-15T10:30:00"
}
```

### Create Request
```json
{
  "user_id": "UUID",
  "title": "String (required)",
  "message": "String (required)",
  "type": "String (required: alert, info, warning, success, error)"
}
```

### Update Request
```json
{
  "title": "String (optional)",
  "message": "String (optional)",
  "type": "String (optional)",
  "is_read": "Boolean (optional)"
}
```

---

## Status Codes

| Code | Meaning | Scenario |
|------|---------|----------|
| **200** | OK | GET, PUT successful |
| **201** | Created | POST successful |
| **204** | No Content | DELETE successful |
| **404** | Not Found | Resource doesn't exist |
| **422** | Invalid Type | Type not in (alert, info, warning, success, error) |

---

## Query Parameters

### Pagination
- `skip` (default: 0) - Records to skip
- `limit` (default: 10) - Records to return

### Filtering
- `user_id` - Filter by user UUID
- `type` - Filter by type (alert, info, warning, success, error)
- `is_read` - Filter by read status (true/false)

### Example
```
/api/notifications?skip=0&limit=5&type=success&is_read=false
```

---

## Common Workflows

### Workflow 1: Send and Read Notification
```bash
# Admin creates alert notification
POST /api/notifications
# User sees unread count
GET /api/notifications/user/{user_id}/unread
# User marks as read
PUT /api/notifications/{id}/read
```

### Workflow 2: Clear All Notifications
```bash
# Mark all as read
PUT /api/notifications/user/{user_id}/read-all
# Delete all
DELETE /api/notifications/user/{user_id}/all
```

### Workflow 3: Filter and Count
```bash
# Get high-priority alerts
GET /api/notifications?type=alert&user_id={user_id}&skip=0&limit=100
# Count in response length
```

---

## Notification Types

| Type | Use Case | Icon Suggestion |
|------|----------|-----------------|
| **alert** | Urgent, requires attention | 🚨 |
| **info** | General information | ℹ️ |
| **warning** | Warning messages | ⚠️ |
| **success** | Successful operations | ✅ |
| **error** | Error messages | ❌ |

---

## Integration Checklist

- [ ] Create notifications for key events (payments, orders, appointments)
- [ ] Display unread count in UI
- [ ] Implement notification tray/inbox view
- [ ] Add mark-as-read functionality
- [ ] Set up background job for stale notification cleanup
- [ ] Configure notification types based on business events
- [ ] Add pagination to large notification lists
- [ ] Implement search/filter functionality for users

---

## Performance Tips

1. **Always use pagination** - Use `limit` parameter to keep responses small
2. **Filter early** - Use query parameters to reduce dataset
3. **Index lookup** - Combine `user_id` with `is_read` for fast queries
4. **Batch operations** - Use `/read-all` instead of updating individually
5. **Archive old** - Periodically delete old notifications to maintain performance

---

**Quick Reference Complete**
