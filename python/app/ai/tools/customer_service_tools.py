


from typing import Any, Dict, Optional

"""
A continuación las firmas recomendadas (Python-style) y descripción breve. Puedes usar exactamente estos nombres para crear @tool en LangGraph.

Identificación (sin login)

def identify_by_phone(phone: str) -> dict
    params: phone (E.164 preferred)
    retorna: { "ok": True/False, "data": { "client_id": int, "full_name": str, "client_type": str, "phone": str, "email": str|null }, "error": null|"not_found" }
    nota: útil para iniciar la sesión conversacional; si hay múltiples coincidencias retorna error con lista.

def identify_by_telegram(telegram_user_id: int | str | username:str) -> dict
    params: telegram_user_id (numérico) o username (string)
    retorna igual que arriba.


def whoami(context_token: str|null) -> dict
    params: context_token (opcional) — si usas tokens de sesión.
    retorna: info del actor (user/app) o {ok:False}.

Cliente

def client_get(client_id: int) -> dict

retorna: { ok, data: {client_id, full_name, phone, email, client_type, registered_at, ...}, error }
def client_me(identifier: dict) -> dict

params: identifier puede ser { "phone": "..."} or {"telegram_user_id": ...}
retorna: cliente asociado (idéntico a client_get) o not_found.
Productos / Catálogos

def product_get(product_id: int, client_id: int|null = None) -> dict

retorna: { ok, data: { product_id, name, sku, description, price, stock, effective_price, category_id, image_url }, error }
effective_price = precio con catálogo/descuento aplicado si aplica al client_id.
def product_search(q: str, client_id: int|null=None, catalog_id:int|null=None, limit:int=10, offset:int=0) -> dict

retorna: { ok, data: { total:int, results:[{product_id,name, snippet, effective_price, stock}] } }
def catalog_list(client_type: str|null=None, active_only: bool=True) -> dict

retorna: lista de catálogos visibles.
def catalog_get_products(catalog_id: int) -> dict

retorna: lista de productos con effective_price.
Pedidos / Orders

def order_create(client_identifier: dict, items: list[dict], notes: str|null=None, context_user_id: int|null=None) -> dict

params: client_identifier = { "phone": "..."} or {"telegram_user_id": ...} or { "client_id": 3 }
items = [ { "product_id": int, "quantity": int } ]
retorna: { ok, data: { order_id, status, totals:{subtotal,discount_total,tax_total,grand_total} }, error }
comportamiento: el servidor fija unit_price snapshots, valida stock.
def order_add_item(order_id: int, product_id: int, quantity: int) -> dict

retorna actualizado: item y totals o error (stock).
def order_get(order_id: int, actor_identifier: dict|null = None) -> dict

retorna: order completo (items, totals, status, invoices[]).
def order_list_by_client(client_identifier: dict, limit:int=20, offset:int=0) -> dict

retorna: list summary.
def order_finalize(order_id: int, client_identifier: dict|null=None, want_invoice: bool=False, invoice_splits: list|null=None, billing_info: dict|null=None) -> dict

params: if want_invoice=True, invoice_splits can be None (single invoice) or [{amount, billing_info}] or 2-way split logic handled by caller.
retorna: { ok, data: { order_id, invoices:[{invoice_id,..}], status }, error }
nota: handle DB trigger errors (e.g., requires invoice) and surface friendly messages.
def order_print_ticket(order_id: int, format: str = "text") -> dict

retorna: { ok, data: { text: str } } (or path/url for pdf).
Facturas / Invoices

def invoice_create(order_id:int, billing_info:dict, invoice_number: str|null=None, amount: decimal|null=None) -> dict

retorna: { ok, data: { invoice_id, invoice_number, issued_at }, error }
campos de billing_info: billing_name, rfc, regimen_fiscal, fiscal_postal_code, billing_address, uso_cfdi, forma_pago, metodo_pago, currency_code, exchange_rate
def invoice_list_by_order(order_id:int) -> dict

retorna: lista de facturas.
Tickets (soporte)

def ticket_create(client_identifier: dict, subject: str, description: str|null=None, priority:str='media', due_at: str|null=None) -> dict

retorna: { ok, data: { ticket_id, created_at }, error }
def ticket_get(ticket_id:int, actor_identifier: dict|null=None) -> dict

retorna: ticket con messages[], linked events/alerts.
def ticket_update_status(ticket_id:int, new_status: str, actor_identifier: dict|null=None, resolution_note: str|null=None) -> dict

si new_status=='cerrado' el tool escribe resolved_at y appends note.
def ticket_add_message(ticket_id:int, sender: str, content: str, external_message_id: str|null=None) -> dict

retorna message_id.
"""