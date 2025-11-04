# OmniDesk — Documentación de la Base de Datos

> Documentación completa y moderna de la base de datos `omnidesk`.
> Esta guía explica la estructura, reglas de negocio implementadas en SQL (tablas, índices, vistas, triggers, y procedimientos), ejemplos de uso y recomendaciones de mantenimiento y seguridad.

---

## Índice

- Visión general
- Convenciones y buenas prácticas
- Diagrama conceptual (resumen)
- Tablas principales
  - `app_user`
  - `client`
  - `category`
  - `product`
  - `catalog`
  - `catalog_product`
  - `customer_order`
  - `order_item`
  - `invoice`
  - `conversation`, `message`
  - `ticket`, `calendar_event`, `alert`
- Vistas importantes
  - `v_catalog_effective_price`
  - `v_order_totals`
- Procedimientos almacenados
  - `sp_recalc_order_totals`
- Triggers clave y su propósito
- Índices y rendimiento
- Integridad referencial y reglas de negocio
- Migración, despliegue y restauración
- Seguridad y recomendaciones operativas
- Ejemplos de consultas útiles
- Anexos: notas de diseño y decisiones

---

## Visión general

La base de datos `omnidesk` está diseñada para soportar un sistema tipo e‑commerce con módulo de atención al cliente y gestión de tickets. Se prioriza:

- Consistencia y snapshots de datos (precios en los `order_item`).
- Reglas de negocio implementadas en la propia BD (triggers y CHECKs).
- Auditoría básica con marcas temporales y campos `created_by`/`updated_by`.

Está pensada para MySQL 8.0+ (uso de CHECK, triggers con SIGNAL, columnas GENERATED, vistas y procedimientos almacenados).


## Convenciones y buenas prácticas usadas

- Tablas en singular (ej. `product`, `client`).
- Llaves PK con sufijo `_id`.
- Campos temporales con sufijo `_at`.
- Campos `created_by`, `updated_by` referencian `app_user(user_id)` y usan ON DELETE SET NULL.
- Uso de ENUM para estados y roles cuando los dominios son pequeños y controlados.
- CHECKs para validaciones de integridad leve (ej.: precios >= 0).


## Diagrama conceptual (resumen)

- `app_user` — usuarios del sistema (agentes / admin).
- `client` — clientes externos con datos de contacto.
- `product`, `category` — catálogo de productos.
- `catalog` y `catalog_product` — campañas y asociación con productos.
- `customer_order` y `order_item` — pedidos y su detalle con snapshots.
- `invoice` — facturas por pedido.
- `conversation` y `message` — mensajería con clientes (multicanal).
- `ticket`, `calendar_event`, `alert` — módulo de soporte, calendario y recordatorios.

(Para un diagrama ER visual puedes exportar la DDL y usar herramientas como MySQL Workbench o dbdiagram.io). 


## Tablas principales

A continuación se documenta cada tabla con sus columnas clave, constraints, índices y notas de uso.

### `app_user`
Propósito: cuentas internas (administradores y empleados).

Columnas relevantes:
- `user_id` INT PK AUTO_INCREMENT
- `full_name`, `username`, `email`
- `password_hash` — almacenar sólo hashes (bcrypt/argon2id)
- `role` ENUM('admin','empleado')
- `active` BOOLEAN
- `last_login_at`, `password_changed_at`, `failed_login_attempts`, `locked_until`
- `created_at`, `updated_at`

Constraints y índices:
- UNIQUE `username`, UNIQUE `email`
- INDEX `idx_app_user_role_active` sobre `(role, active)`

Notas:
- Nunca guardar contraseñas en claro. Almacena el hash en `password_hash`.
- `failed_login_attempts` y `locked_until` facilitan un mecanismo de bloqueo.


### `client`
Propósito: clientes externos.

Columnas relevantes:
- `client_id` INT PK
- `full_name`, `phone`, `email`, `telegram_*`
- `client_type` ENUM('normal','premium')
- `status` ENUM('active','inactive','blocked')
- `registered_at`, `updated_at`, `deleted_at`
- `created_by`, `updated_by` (FK a `app_user`)

Constraints e índices:
- UNIQUE en `phone`, `email`, `telegram_user_id`
- FK `created_by` / `updated_by` -> `app_user(user_id)` ON DELETE SET NULL
- Índices: `idx_client_name`, `idx_client_type_status`, `idx_client_registered_at`

Notas:
- `deleted_at` permite soft-delete si la aplicación lo respeta.


### `category`
Propósito: jerarquía de categorías de producto.

Columnas:
- `category_id` INT PK
- `name` UNIQUE
- `parent_id` FK a `category(category_id)` ON DELETE SET NULL


### `product`
Propósito: catálogo maestro de productos.

Columnas clave:
- `product_id`, `sku`, `name`, `description`, `image_url`
- `category_id` FK -> `category` (ON DELETE SET NULL)
- `price` DECIMAL(10,2) CHECK (price >= 0)
- `stock` INT UNSIGNED DEFAULT 0 CHECK (stock >= 0)
- `status` ENUM('draft','active','archived')

Índices:
- `idx_product_name`
- FULLTEXT `ftx_product_nd` sobre `(name, description)` (útil para búsquedas textuales)

Notas:
- `sku` es UNIQUE (puede ser NULL). Manténlo si se integra con inventarios externos.


### `catalog`
Propósito: campañas/colecciones de productos con descuentos y visibilidad.

Columnas:
- `catalog_id`, `name`, `description`
- `discount_percentage` DECIMAL(5,2) CHECK entre 0 y 100
- `start_date`, `end_date`, `visible_to` ENUM
- `active` BOOLEAN

Restricciones:
- CHECK sobre fechas (start <= end si ambos presentes)
- UNIQUE `name`
- INDEX `idx_catalog_active_dates`


### `catalog_product`
Propósito: asociar productos a catálogos con `special_price` o `assigned_stock`.

PK: (catalog_id, product_id)
FKs: a `catalog` y `product` ON DELETE CASCADE

Checks y triggers:
- CHECKs para evitar precios negativos.
- Triggers `trg_cp_before_ins` y `trg_cp_before_upd` que:
  - Validan que `assigned_stock` no exceda `product.stock`.
  - Validan que `special_price` no supere `product.price`.

Índices:
- `idx_cp_product(product_id)`


### `customer_order`
Propósito: encabezado del pedido.

Columnas clave:
- `order_id`, `client_id` FK -> `client` (ON DELETE RESTRICT)
- `status` ENUM de flujo (`borrador`, `confirmado`, `preparando`, `enviado`, `entregado`, `cancelado`, `devuelto`)
- `payment_status` ENUM
- Totales: `subtotal`, `discount_total`, `tax_total`, `shipping_total`
- `grand_total` GENERATED ALWAYS AS ROUND(subtotal - discount_total + tax_total + shipping_total,2) STORED
- `created_by`, `updated_by`

Índices:
- `idx_order_client_created`, `idx_order_status_payment`, `idx_order_updated_at`

Notas:
- `grand_total` se calcula en la base de datos para garantizar consistencia.
- Existen triggers para forzar la existencia de una factura al cambiar a ciertos estados (ver `trg_order_require_invoice`).


### `order_item`
Propósito: detalle del pedido con snapshot del producto.

PK: (order_id, product_id)
Columnas clave:
- `quantity`, `product_name`, `sku`, `unit_price`, `discount_pct`, `discount_amount`, `tax_rate`
- Columnas GENERATED: `line_subtotal`, `line_discount`, `line_tax_base`, `line_tax`, `line_total`

FKs:
- `order_id` -> `customer_order` ON DELETE CASCADE
- `product_id` -> `product` ON DELETE RESTRICT

Índices:
- `idx_oi_product`, `idx_oi_totals`

Notas:
- Guardar snapshot (nombre, SKU, unit_price) protege contra cambios posteriores en `product`.
- Triggers AFTER INSERT/UPDATE/DELETE llaman `sp_recalc_order_totals` para mantener los totales del encabezado sincronizados.


### `invoice`
Propósito: facturas asociadas a pedidos.

Columnas:
- `invoice_id`, `order_id` FK, `invoice_number`, `series`, `issued_at`, `due_at`, `currency_code`, `status`
- UNIQUE (order_id, invoice_number)
 - Campos adicionales (información fiscal / facturación):
   - `billing_name` VARCHAR(150) NULL — Nombre / Razón social del receptor
   - `rfc` VARCHAR(13) NULL — RFC del receptor (si aplica)
   - `regimen_fiscal` VARCHAR(120) NULL — Régimen fiscal (CFDI)
   - `fiscal_postal_code` VARCHAR(10) NULL — Código Postal del domicilio fiscal (CFDI)
   - `billing_address` TEXT NULL — Dirección para comprobante interno / logística
   - `uso_cfdi` VARCHAR(10) NULL — Uso CFDI (si timbras)
   - `forma_pago` VARCHAR(50) NULL — Forma de pago (si timbras)
   - `metodo_pago` VARCHAR(50) NULL — Método de pago (si timbras)
   - `exchange_rate` DECIMAL(18,6) NULL — Tipo de cambio si aplica

Triggers:
- `trg_invoice_before_delete` impide borrar la última factura si el pedido aún activo (no en borrador/cancelado).

Índices:
- `idx_invoice_issued_at`, `idx_invoice_number`


### `conversation` y `message`
Propósito: mensajería multicanal con clientes.

`conversation`:
- `conversation_id`, `client_id` FK -> `client` (ON DELETE SET NULL)
- `channel` ENUM, `external_chat_id`, `active`, `handled_by_bot`, `last_message_at`
- UNIQUE (channel, external_chat_id)

`message`:
- `message_id`, `conversation_id` FK -> `conversation` ON DELETE CASCADE
- `sender` ENUM('client','user','bot')
- `content`, `external_message_id`, `created_at`
- UNIQUE (conversation_id, external_message_id)

Triggers:
- `trg_msg_ai` AFTER INSERT en `message` actualiza `conversation.last_message_at`.


### `ticket`, `calendar_event`, `alert`
Propósito: soporte y recordatorios.

`ticket`:
- `ticket_id`, `client_id`, `subject`, `description`, `priority`, `status`, `created_at`, `due_at`, `resolved_at`, `assigned_to`
- Trigger `trg_ticket_set_resolved` establece `resolved_at` al cambiar `status` a `cerrado`.

`calendar_event`:
- Eventos con `start_time`, `end_time`, `created_by`, `ticket_id`.

`alert`:
- Recordatorios con `alert_time`, `message`, `kind`, `ticket_id` o `event_id` (al menos uno requerido por CHECK), `sent` flag.


## Vistas importantes

### `v_catalog_effective_price`
Descripción: Devuelve el precio efectivo de un producto dentro de un catálogo considerando `special_price`, `discount_percentage` o `price` base.

Uso típico: listar productos de un catálogo con precios ya calculados. Filtra catálogos activos y vigentes.

Nota: La vista usa ROUND en la fórmula de descuento para normalizar moneda.


### `v_order_totals`
Descripción: Suma los subtotales, descuentos y impuestos del detalle (`order_item`) agrupados por `order_id`. Utilizada por el procedimiento `sp_recalc_order_totals`.


## Procedimientos almacenados

### `sp_recalc_order_totals(IN p_order_id INT)`
Propósito: Recalcula `subtotal`, `discount_total` y `tax_total` en `customer_order` a partir de `order_item`.

Se llama desde triggers AFTER INSERT/UPDATE/DELETE en `order_item`.


## Triggers clave y su propósito

- `trg_cp_before_ins`, `trg_cp_before_upd` (catalog_product): Validan `assigned_stock` y `special_price` contra `product`.
- `trg_oi_ai`, `trg_oi_au`, `trg_oi_ad` (order_item): Tras cambios en detalle llaman `sp_recalc_order_totals`.
- `trg_msg_ai` (message): Mantiene `conversation.last_message_at` actualizado.
- `trg_ticket_set_resolved` (ticket): Pone `resolved_at` al cerrar el ticket.
- `trg_order_require_invoice` (customer_order): Evita cambiar a ciertos estados si no hay factura.
- `trg_invoice_before_delete` (invoice): Evita borrar la última factura en pedidos activos.

Los triggers usan SIGNAL para abortar la operación con mensajes claros — ideal para que la capa de aplicación capture y muestre errores de negocio.


## Índices y rendimiento

- Se crearon índices en columnas de búsqueda y joins frecuentes (cliente, producto, fechas, estado).
- `product` tiene índice FULLTEXT para búsquedas por nombre/descripcion.
- Las vistas no tienen índices propios; cualquier consulta a `v_catalog_effective_price` debería paginar y/o filtrar por `catalog_id` o `product_id` para evitar escaneos grandes.
- Para volúmenes altos, considera:
  - Desnormalizar contadores críticos o totales calculados en la aplicación o con jobs periódicos.
  - Crear índices compuestos adicionales basados en consultas reales (query profiling).


## Integridad referencial y reglas de negocio

- Se prioriza ON DELETE SET NULL en relaciones donde se quiere preservar objetos históricos (`client` en `conversation`, `created_by` en varias tablas).
- ON DELETE RESTRICT para relaciones que no deben perderse (por ejemplo `customer_order.client_id`).
- CHECKs y triggers implementan reglas que no conviene confiar únicamente a la capa de la aplicación (ej.: stock asignado en campañas).


## Migración, despliegue y restauración

- El script `database/init/init.sql` crea y poblates (si añadieras seeds) la base `omnidesk` — úsalo para inicializar entornos de desarrollo.

Sugerencias:
- En entornos de producción, no ejecutar `DROP DATABASE IF EXISTS omnidesk;` sin respaldo previo.
- Mantén migraciones incrementales (Flyway, Liquibase o herramientas ORM) en lugar de reejecutar el DDL completo.
- Para restaurar backups: usar dumps de mysqldump con --single-transaction para InnoDB.

Ejemplo (entorno local):
```powershell
# Crear la BD localmente (MySQL 8+)
# Ajusta host, user y password según tu entorno
mysql -u root -p < "c:/Users/aleth/Documents/OmniDesk/database/init/init.sql"
```


## Seguridad y recomendaciones operativas

- Nunca exponer puertos de administración sin VPN/ACL.
- Acceso a la BD con cuentas mínimas (principio de privilegio mínimo).
- Proteger `password_hash` con algoritmos robustos (bcrypt o argon2id) en la capa de aplicación.
- Registrar y monitorear intentos fallidos de login (usar `failed_login_attempts` y `locked_until`).
- Copias de seguridad diarias y pruebas de restauración periódicas.


## Ejemplos de consultas útiles

1) Obtener precio efectivo de productos para un catálogo:

```sql
SELECT * FROM v_catalog_effective_price WHERE catalog_id = 123 ORDER BY effective_price;
```

2) Recalcular totales manualmente para un pedido (útil en migraciones o reparaciones):

```sql
CALL sp_recalc_order_totals(456);
SELECT * FROM customer_order WHERE order_id = 456;
```

3) Buscar clientes con conversaciones recientes:

```sql
SELECT c.client_id, c.full_name, conv.last_message_at
FROM client c
JOIN conversation conv ON conv.client_id = c.client_id
WHERE conv.last_message_at > NOW() - INTERVAL 30 DAY
ORDER BY conv.last_message_at DESC;
```

4) Reporte simple: pedidos con totales y número de facturas

```sql
SELECT o.order_id, o.created_at, o.grand_total, COUNT(i.invoice_id) AS invoices
FROM customer_order o
LEFT JOIN invoice i ON i.order_id = o.order_id
GROUP BY o.order_id
ORDER BY o.created_at DESC
LIMIT 100;
```


## Anexos: notas de diseño y decisiones

- Uso de columnas GENERATED y CHECKs: facilitan integridad y reducen lógica en la aplicación, pero pueden limitar compatibilidad con versiones antiguas de MySQL.
- Triggers con SIGNAL ayudan a centralizar reglas de negocio; sin embargo, complejizan migraciones. Documenta cada trigger y testea sus mensajes de error en la capa de aplicación.
- Se prefirieron ON DELETE SET NULL para relaciones de auditoría para preservar históricos.


---

## ¿Qué sigue?

- Recomendado: generar un diagrama ER visual a partir del script y añadirlo a este repo (`docs/er_diagram.png`).
- Añadir scripts de migración incremental (por ejemplo, con Flyway) y tests de integridad automatizados.


---

Documentación generada automáticamente a partir de `database/init/init.sql`. Si quieres, puedo:
- Añadir el diagrama ER y/o un archivo SVG.
- Extraer una lista de todas las columnas y tipos en formato CSV.
- Generar tests SQL que verifiquen CHECKs y triggers en un entorno de staging.

Dime cuál de estas tareas quieres que haga ahora.