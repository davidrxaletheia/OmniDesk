# Classes (Pydantic + Repos)

Este paquete separa **modelos de datos** (Pydantic `BaseModel`) de **repositorios** (CRUD SQL).
Así puedes **usar BaseModel** en toda tu app sin perder los helpers de acceso a datos.

## Instalación
```bash
pip install pydantic mysql-connector-python
```

## Ejemplo rápido
```python
from Classes import DB
from Classes.models import ClientModel, ProductModel
from Classes.repos import ClientRepo, ProductRepo, CustomerOrderRepo, OrderItemRepo, InvoiceRepo

with DB() as db:
    # Crear cliente con BaseModel
    cm = ClientModel(full_name="Cliente Demo", email="demo@example.com", client_type="normal")
    cid = ClientRepo(db).create(cm.dict(exclude_none=True, exclude_unset=True))

    # Buscar producto
    prod = ProductRepo(db).search("Router", limit=1)[0]

    # Crear pedido + item + factura
    order_repo = CustomerOrderRepo(db)
    oid = order_repo.create({"client_id": cid, "created_at": "NOW()", "notes": "Pedido desde README"})
    OrderItemRepo(db).add_item({
        "order_id": oid, "product_id": prod.product_id, "quantity": 1,
        "product_name": prod.name, "sku": prod.sku, "unit_price": prod.price, "tax_rate": 16.00
    })
    InvoiceRepo(db).create({"order_id": oid, "invoice_number": f"INV-{oid:04d}", "series": "A", "issued_at": "NOW()", "currency_code": "MXN", "status": "emitida"})
```

> Consejo: Los repos **devuelven modelos** Pydantic (no tuplas). Para `create/update` pasa `dict()` desde tu BaseModel.
