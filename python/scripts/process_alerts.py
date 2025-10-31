"""
Script sencillo para procesar alertas pendientes: obtiene `AlertRepo.pending()`
marca cada alerta como enviada (`sent=1`) y escribe un log por consola.

Diseñado para ejecutarse periódicamente desde cron o como tarea programada.
"""
from python.app.repos.alert_repo import AlertRepo


def main():
    repo = AlertRepo()
    alerts = repo.pending(limit=100)
    if not alerts:
        print("No pending alerts")
        return
    for a in alerts:
        try:
            aid = a.alert_id if hasattr(a, 'alert_id') else getattr(a, 'id', None)
            print(f"Processing alert {aid}: {getattr(a, 'message', '')}")
            # Aquí puedes integrar envío de email, webhook, etc.
            # Marcar como enviado
            repo.update(aid, {'sent': 1})
        except Exception as exc:
            print(f"Failed to process alert {getattr(a, 'alert_id', '?')}: {exc}")


if __name__ == '__main__':
    main()
