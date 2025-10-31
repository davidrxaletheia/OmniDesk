# API para calendario unificado

Este documento muestra el JSON que la UI puede consumir para mostrar un único calendario con: eventos, tickets (como eventos) y alertas.

Formato de respuesta (GET /api/calendar/view?start=...&end=...)

Respuesta: arreglo de `entries`. Cada entrada tiene campos comunes y un `kind` que indica su origen.

[
  {
    "id": "event-123",            # id único en formato {kind}-{pk}
    "kind": "event",             # 'event' | 'ticket' | 'alert'
    "title": "Revisión de ticket #45",
    "description": "Descripción larga...",
    "start": "2025-10-31T10:00:00Z",
    "end": "2025-10-31T11:00:00Z",
    "meta": {                      # datos específicos según kind
      "event_id": 123,
      "ticket_id": 45,
      "created_by": 7
    }
  },
  {
    "id": "ticket-45",
    "kind": "ticket",
    "title": "Ticket: No hay conexión",
    "description": "Cliente reporta pérdida de señal",
    "start": "2025-10-31T09:00:00Z",
    "end": "2025-10-31T10:00:00Z",
    "meta": {
      "ticket_id": 45,
      "status": "abierto",
      "priority": "alta",
      "client_id": 12
    }
  },
  {
    "id": "alert-77",
    "kind": "alert",
    "title": "Recordatorio: llamada con cliente",
    "description": "Llamar a cliente para seguimiento",
    "start": "2025-10-31T08:50:00Z",
    "end": null,
    "meta": {
      "alert_id": 77,
      "ticket_id": 45,
      "sent": false
    }
  }
]

Notas para el frontend
- Consultas por rango: usar `start` y `end` (ISO8601) para paginar/filtrar.
- Para mostrar en librerías tipo FullCalendar, usar `id`, `title`, `start`, `end` y guardar `meta` en extendedProps.
- Origen y color: mapear `kind` a colores/íconos distintos.
- CRUD: exponer endpoints separados para crear tickets/events/alerts; luego el frontend puede crear entradas directamente o crear ticket y dejar que el backend cree el event asociado.

Ejemplo de endpoints útiles a exponer (implementables fácilmente):
- `GET /api/calendar/view?start=...&end=...` → devuelve el arreglo unificado (merge de events, ticket-events y alerts)
- `POST /api/tickets` → puede incluir `create_event=true` para que el backend cree el evento automáticamente
- `POST /api/events` → crear evento manual
- `POST /api/alerts` → crear alerta/recordatorio
- `GET /api/alerts/pending` → listar alertas pendientes (empleados/admin)

