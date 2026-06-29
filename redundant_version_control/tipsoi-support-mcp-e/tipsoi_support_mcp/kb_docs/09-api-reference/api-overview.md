---
title: "API Overview"
description: "REST API documentation and overview for developers"
category: "API Reference"
difficulty: "advanced"
tags: ["api", "rest", "integration", "developers", "endpoints"]
version: "1.0"
updated_at: "2026-04-26"
---

# API Overview

## What is the Tipsoi API?

The **Tipsoi API** is a REST API that allows external systems to integrate with Tipsoi. You can:
- Fetch employee data
- Get attendance records
- Manage leave requests
- Execute payroll
- Retrieve reports
- Sync data with external systems

## Base URL

```
https://hrm.tipsoi.pro/inovace-client/api/v1
```

## Authentication

All API requests require:
- **Bearer Token** (JWT) in Authorization header
- **API Key** for service accounts

**Example**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Get token**:
1. Login to Tipsoi
2. Go to **Settings → API Keys**
3. Click "Create New Key"
4. Generate API token
5. Use in Authorization header

## Request/Response Format

### Request

```json
{
  "method": "GET",
  "url": "https://hrm.tipsoi.pro/inovace-client/api/v1/employee",
  "headers": {
    "Authorization": "Bearer {TOKEN}",
    "Content-Type": "application/json"
  },
  "params": {
    "org_id": "8",
    "status": 1
  }
}
```

### Response

All responses are JSON:

**Success (200)**:
```json
{
  "success": true,
  "data": [
    {
      "id": "348229",
      "name": "Ali Hassan",
      "email": "ali@company.com"
    }
  ],
  "meta": {
    "timestamp": "2026-04-26T10:30:00Z"
  }
}
```

**Error (400/500)**:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required parameter: org_id"
  }
}
```

## Main API Endpoints

### Employee Management

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /employee | Get employee list |
| GET | /employee/:id | Get single employee |
| POST | /employee | Create new employee |
| PUT | /employee/:id | Update employee |
| DELETE | /employee/:id | Delete employee |

### Attendance

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /attendance | Get attendance records |
| POST | /attendance/punch | Create punch record |
| GET | /reports/attendance | Attendance report |

### Leave

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /leave-balance | Get employee leave balance |
| POST | /leave-request | Create leave request |
| GET | /leave-management/applied-leaves | Get all leave requests |
| POST | /leave-management/approve-leave | Approve leave |

### Payroll

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /payroll/status | Check payroll status |
| POST | /payroll/run | Execute payroll |
| GET | /payroll/validate | Validate before payroll |
| GET | /reports/payroll | Payroll report |

### Reports

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /reports/monthly-attendance | Attendance report |
| GET | /reports/daily-summary | Daily summary |
| GET | /reports/late-report | Late arrivals |
| GET | /reports/monthly-overtime | Overtime report |

## API Rate Limiting

To prevent abuse, API has rate limits:

- **Requests per minute**: 60 (standard), 300 (premium)
- **Burst limit**: 10 requests per second
- **Daily quota**: 10,000 requests (standard), unlimited (premium)

**Rate limit headers**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1619419200
```

If limit exceeded:
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "You've exceeded your rate limit. Try again in 60 seconds."
  }
}
```

## Common Patterns

### Pagination

For endpoints returning lists:

```
GET /employee?page=1&per_page=50&sort=name&order=asc
```

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "total": 300,
    "page": 1,
    "per_page": 50,
    "total_pages": 6
  }
}
```

### Filtering

Filter results by parameters:

```
GET /attendance?date_from=2026-04-01&date_to=2026-04-30&employee_id=348229&status=present
```

### Sorting

Sort results:

```
GET /employee?sort=name&order=asc
GET /attendance?sort=date&order=desc
```

## Error Codes

| Code | Status | Meaning |
|---|---|---|
| INVALID_REQUEST | 400 | Missing or invalid parameters |
| UNAUTHORIZED | 401 | Invalid or expired token |
| FORBIDDEN | 403 | Don't have permission for this |
| NOT_FOUND | 404 | Resource doesn't exist |
| CONFLICT | 409 | Resource already exists |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |

## Multi-Tenancy

Tipsoi is multi-tenant. Always include `org_id`:

```
GET /employee?org_id=8
```

**org_id** determines which organization's data you access. You can only access your own org_id (enforced by JWT).

## Authentication Methods

### 1. Personal API Token

Generate from **Settings → API Keys**:
- Associated with your user account
- Restricted to your org_id
- Revocable anytime

**Use case**: Personal integrations, testing

### 2. Service Account Token

For automated integrations:
- Not associated with user
- Can be scoped to specific permissions
- Better for production

**Request access**: Contact support

### 3. OAuth 2.0

For third-party integrations:
- User grants permission
- Token expires after period
- Can be revoked by user

**Documentation**: See OAuth Reference

## API Versioning

Current version: **v1**

Base URL contains version:
```
https://hrm.tipsoi.pro/inovace-client/api/v1
```

Future versions (v2, v3) will have different URLs. v1 will continue to work.

## Webhooks

Real-time events via webhooks:

- **Attendance punch recorded**
- **Leave request created/approved**
- **Payroll executed**
- **Employee data updated**

**Setup**: **Settings → Webhooks → Create New**

## Libraries & SDKs

### JavaScript/Node.js

```bash
npm install @tipsoi/api-sdk
```

```javascript
const Tipsoi = require('@tipsoi/api-sdk');
const client = new Tipsoi({
  apiKey: process.env.TIPSOI_API_KEY,
  baseUrl: 'https://hrm.tipsoi.pro/inovace-client/api/v1'
});

// Fetch employees
const employees = await client.employees.list({
  org_id: '8',
  status: 1
});
```

### Python

```bash
pip install tipsoi-sdk
```

```python
from tipsoi import Client

client = Client(
    api_key=os.environ['TIPSOI_API_KEY'],
    base_url='https://hrm.tipsoi.pro/inovace-client/api/v1'
)

# Fetch employees
employees = client.employees.list(org_id='8', status=1)
```

### PHP/Laravel

```bash
composer require tipsoi/laravel-sdk
```

## Common Use Cases

### 1. Sync Employee Data

Pull employee list daily and sync to your HRIS:

```javascript
const employees = await client.employees.list({org_id: '8'});
// Push to your database
updateYourDatabase(employees);
```

### 2. Attendance Integration

Pull attendance records and sync to payroll system:

```javascript
const attendance = await client.reports.monthlyAttendance({
  org_id: '8',
  month: '2026-04'
});
// Send to payroll
processPayroll(attendance);
```

### 3. Automated Leave Approval

Auto-approve leave requests from specific department:

```javascript
const leaves = await client.leave.listRequests({org_id: '8', status: 'pending'});
for (let leave of leaves) {
  if (leave.department === 'IT') {
    await client.leave.approve({leave_id: leave.id});
  }
}
```

### 4. Payroll Trigger

Run payroll on schedule:

```javascript
const payrollStatus = await client.payroll.getStatus({org_id: '8'});
if (payrollStatus.can_proceed) {
  await client.payroll.run({org_id: '8', month: '2026-04'});
}
```

## Best Practices

1. **Use service accounts** for automated integrations (not personal tokens)
2. **Handle rate limits** - implement exponential backoff
3. **Cache data** when possible (reduces API calls)
4. **Use webhooks** instead of polling (more efficient)
5. **Validate input** before sending to API
6. **Log errors** for debugging
7. **Use pagination** for large datasets
8. **Secure API keys** - never commit to git
9. **Monitor usage** to stay within rate limits
10. **Version your integration** for future API changes

## Related Documents

- [Authentication](./authentication.md)
- [Employee Endpoints](./employee-endpoints.md)
- [Attendance Endpoints](./attendance-endpoints.md)
- [Leave Endpoints](./leave-endpoints.md)
- [Payroll Endpoints](./payroll-endpoints.md)
- [Report Endpoints](./report-endpoints.md)
- [Error Codes](./error-codes.md)

## Support

**API Documentation**: docs.tipsoi.com/api
**API Issues**: support@inovacetech.com
**Slack Community**: community.slack.tipsoi.com (for developers)

## FAQ

**Q: Can I use the API for real-time integrations?**
A: Yes, but with rate limits. Use webhooks for event-driven real-time.

**Q: Is API data encrypted?**
A: Yes, all API communication is over HTTPS with TLS 1.2+.

**Q: What's the maximum payload size?**
A: POST/PUT requests limited to 10 MB.

**Q: Can I test API without production data?**
A: Yes, request sandbox environment from support.

**Q: How do I report API bugs?**
A: Email support@inovacetech.com with details and API request.
