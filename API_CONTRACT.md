# OmniDesk API Contract

This file documents the minimal API contract for the frontend team. It describes endpoints, parameters, request/response examples (curl) and notes about datetimes, pagination and auth.

All protected endpoints require an Authorization header:

- Header: `Authorization: Bearer <access_token>`

Datetimes
- All datetimes are returned as ISO-8601 strings in UTC (example: `2025-10-29T12:34:56Z`). Query parameters that accept datetimes expect the same format.

Pagination
- List endpoints accept `limit` (default 50) and `offset` (default 0). If omitted, server returns up to 50 items.

Common response envelope (examples use direct JSON arrays/objects — no extra envelope unless noted):
- 2xx: returns JSON body described per endpoint.
- 401: {"detail": "Unauthorized"}
- 400: {"detail": "Bad Request", "errors": {...}}

---

## Authentication

### POST /api/login

Description: Authenticate a user and return a JWT access token.

Request (application/json):

{
  "username": "user1",
  "password": "secret"
}

Response 200:

{
  "access_token": "<jwt.token.here>",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "user_id": 1,
    "username": "user1",
    "full_name": "User One",
    "email": "user@example.com",
    "role": "empleado",
    "active": true
  }
}

Curl example:

curl -X POST "http://localhost:8000/api/login" -H "Content-Type: application/json" -d '{"username":"user1","password":"secret"}'

Notes: Password is not returned. `password_hash` exists in the model but MUST NOT be sent in responses.

### OpenAPI / Swagger UI

The API exposes a Bearer token security scheme in its OpenAPI spec so you can paste the JWT into Swagger UI's Authorize dialog.

- Scheme name: BearerAuth
- Usage: click Authorize in the Swagger UI and paste the token value (the raw JWT). In requests the header must be sent as:

  Authorization: Bearer <your-jwt>

This matches the `Authorization` header used in the examples above. The token is a standard JWT signed with the server secret.

---

## Summary (dashboard)

### GET /api/summary

Protected. Returns a small aggregated summary used in dashboards.

Response 200 example:

{
  "users_count": 12,
  "tickets": {
    "open": 5,
    "in_progress": 3,
    "closed": 20
  },
  "upcoming_events": 4,
  "unread_messages": 7
}

Curl example (with token):

curl -H "Authorization: Bearer <token>" "http://localhost:8000/api/summary"

---

## Events (Calendar)

Model (CalendarEventModel):

{
  "event_id": int | null,
  "title": str,
  "description": str | null,
  "start_time": ISO-8601 datetime,
  "end_time": ISO-8601 datetime,
  "created_by": int | null,
  "ticket_id": int | null
}

### GET /api/events

Query parameters:
- start (ISO datetime) - optional: filter start_time >= start
- end (ISO datetime) - optional: filter end_time <= end
- ticket_id - optional
- created_by - optional
- limit - optional
- offset - optional

Response 200: JSON array of CalendarEventModel

Example:

[
  {
    "event_id": 42,
    "title": "Call with client",
    "description": "Discuss feature X",
    "start_time": "2025-11-01T15:00:00Z",
    "end_time": "2025-11-01T15:30:00Z",
    "created_by": 2,
    "ticket_id": 7
  }
]

Curl example:

curl "http://localhost:8000/api/events?start=2025-11-01T00:00:00Z&end=2025-11-30T23:59:59Z"

### GET /api/events/{event_id}

Response: single CalendarEventModel or 404

### POST /api/events

Protected. Create an event.

Request body: CalendarEventModel without `event_id` and `created_by` (created_by derived from token). Example:

{
  "title": "Demo",
  "description": "Demo event",
  "start_time": "2025-11-01T15:00:00Z",
  "end_time": "2025-11-01T15:30:00Z",
  "ticket_id": 7
}

Response 201: created event object with `event_id` and `created_by` filled.

Curl example (protected):

curl -X POST "http://localhost:8000/api/events" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title":"Demo","start_time":"2025-11-01T15:00:00Z","end_time":"2025-11-01T15:30:00Z"}'

---

## Tickets

Model (TicketModel):

{
  "ticket_id": int | null,
  "client_id": int,
  "subject": str,
  "description": str | null,
  "priority": "alta"|"media"|"baja",
  "status": "abierto"|"en_progreso"|"cerrado",
  "created_at": ISO datetime | null,
  "due_at": ISO datetime | null,
  "resolved_at": ISO datetime | null,
  "assigned_to": int | null
}

### GET /api/tickets

Query params: status, priority, assigned_to, client_id, limit, offset

Response 200: array of TicketModel.

Example:

[
  {
    "ticket_id": 100,
    "client_id": 55,
    "subject": "Cannot login",
    "description": "User reports login issue",
    "priority": "alta",
    "status": "abierto",
    "created_at": "2025-10-29T09:12:00Z",
    "due_at": null,
    "resolved_at": null,
    "assigned_to": 2
  }
]

Curl example:

curl "http://localhost:8000/api/tickets?status=abierto&limit=20"

### GET /api/tickets/{ticket_id}

Response: TicketModel or 404

### POST /api/tickets

Protected. Create ticket.

Request body (example):

{
  "client_id": 55,
  "subject": "Cannot login",
  "description": "User can't log in since yesterday",
  "priority": "alta"
}

Response 201: created TicketModel with `ticket_id`, `created_at`.

---

## Users

Model (AppUserModel) - note: `password_hash` must never be returned in public responses. Use the following shape for responses:

{
  "user_id": int | null,
  "full_name": str,
  "username": str,
  "email": str | null,
  "role": "admin"|"empleado",
  "active": bool,
  "last_login_at": ISO datetime | null,
  "password_changed_at": ISO datetime | null
}

### GET /api/users

Query params: active, role, limit, offset

Response 200: array of user objects (as above)

Example:

[
  {
    "user_id": 2,
    "full_name": "Support Agent",
    "username": "agent2",
    "email": "agent2@example.com",
    "role": "empleado",
    "active": true,
    "last_login_at": "2025-10-29T08:00:00Z"
  }
]

Curl example:

curl -H "Authorization: Bearer <token>" "http://localhost:8000/api/users?role=empleado"

### POST /api/users

Create user (protected, admin role recommended).

Request (example):

{
  "full_name": "New Agent",
  "username": "newagent",
  "email": "newagent@example.com",
  "password": "ClearTextPassword!",
  "role": "empleado"
}

Response 201: created user (without password or hash). Backend should store `password_hash` only.

---

## Conversations & Messages (brief)

ConversationModel fields: conversation_id, client_id, channel, external_chat_id, active, handled_by_bot, created_at, updated_at, last_message_at

MessageModel fields: message_id, conversation_id, sender (client|user|bot), content, external_message_id, created_at

Endpoints (suggested)
- GET /api/conversations
- GET /api/conversations/{id}
- GET /api/conversations/{id}/messages
- POST /api/conversations/{id}/messages (protected)

Responses follow the models above. Messages should include `created_at` iso-datetimes.

---

## Errors and validation

- Validation errors return 400 with a JSON structure describing invalid fields.
- Unauthorized access returns 401.
- Not found returns 404.

---

## Examples for frontend developers (Postman / curl)

1) Login and get token (curl):

curl -X POST "http://localhost:8000/api/login" -H "Content-Type: application/json" -d '{"username":"user1","password":"secret"}'

2) Use token to fetch events:

curl -H "Authorization: Bearer <token>" "http://localhost:8000/api/events?start=2025-11-01T00:00:00Z&end=2025-11-30T23:59:59Z"

3) Create ticket (curl):

curl -X POST "http://localhost:8000/api/tickets" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"client_id":55,"subject":"Cannot login","priority":"alta"}'

---

Notes / Implementation hints
- Ensure the `password_hash` field in `AppUserModel` is stored but not serialized in responses (use Pydantic `exclude` or separate response model).
- Return datetimes using `.isoformat()` and in UTC (append 'Z' or use timezone-aware datetimes).
- For dev CORS issues, allow `http://localhost:3000` / `file://` origins or serve the simple static HTML from FastAPI.
- Default pagination: limit=50, offset=0.

If you want, I can also export a Postman collection or add direct example responses for additional endpoints (orders, products, clients). Ask and I'll extend this contract.
