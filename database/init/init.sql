-- =========================================================
-- OmniDesk - MySQL schema (init.sql)
-- Propósito:
--   Script completo para crear la base de datos `omnidesk` y
--   todas las tablas, índices, vistas, procedimientos y triggers
--   necesarios para el funcionamiento básico del sistema.
-- Uso y recomendaciones:
--   - Diseñado para MySQL 8.0+ (usa CHECK constraints, GENERATED
--     columns, SIGNAL, y otras características modernas).
--   - Ejecutar en un entorno controlado. Si lo va a ejecutar en
--     producción, haga una copia de seguridad antes y revise los
--     triggers/procedimientos según su política.
--   - Las sentencias DROP/CREATE están pensadas para inicializar
--     un entorno de desarrollo o pruebas; comente el DROP si no
--     desea perder datos.
-- Convenciones usadas en el esquema:
--   - Nombres de tablas en singular (ej. `product`, `client`).
--   - Campos terminados en `_id` son claves primarias o foráneas.
--   - Campos terminados en `_at` almacenan marcas temporales.
--   - ENUMs y CHECKs se usan para reglas simples; validar
--     compatibilidad si su versión de MySQL no soporta CHECK.
-- Autor / Fecha de comentarios mejorados: 2025-10-28
-- =========================================================

-- PASO 0 (opcional): Reiniciar la base de datos si ya existe (ADVERTENCIA: elimina datos previos)
DROP DATABASE IF EXISTS omnidesk;

-- PASO 1: Crear la base de datos y seleccionarla para las siguientes sentencias
CREATE DATABASE IF NOT EXISTS omnidesk CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE omnidesk;

-- ---------------------------------------------------------
-- TABLA: app_user
-- Propósito:
--   Mantener las cuentas de los usuarios que operan el sistema
--   (administradores y empleados). Aquí se guardan hashes de
--   contraseña, roles básicos, estados y datos de auditoría.
-- Buenas prácticas:
--   - Almacena sólo hashes de contraseña (bcrypt/argon2id).
--   - Usa el campo `role` para controlar accesos de forma simple.
--   - `failed_login_attempts` y `locked_until` sirven para
--     medidas de seguridad frente a intentos de acceso.
-- ---------------------------------------------------------
CREATE TABLE app_user (
  user_id                 INT AUTO_INCREMENT PRIMARY KEY,
  full_name               VARCHAR(100) NOT NULL,
  username                VARCHAR(50)  NOT NULL,           -- único, usado para login
  email                   VARCHAR(150) NULL,               -- opcional pero recomendable
  password_hash           VARCHAR(255) NOT NULL,           -- guarda hash (bcrypt/argon2id), nunca en claro
  role                    ENUM('admin','empleado') NOT NULL DEFAULT 'empleado',
  active                  BOOLEAN NOT NULL DEFAULT TRUE,

  last_login_at           DATETIME NULL,
  password_changed_at     DATETIME NULL,
  failed_login_attempts   TINYINT UNSIGNED NOT NULL DEFAULT 0,
  locked_until            DATETIME NULL,                   -- para lockout temporal

  created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT uq_app_user_username UNIQUE (username),
  CONSTRAINT uq_app_user_email    UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_app_user_role_active ON app_user (role, active);

-- ---------------------------------------------------------
-- TABLA: category
-- Propósito:
--   Normalizar categorías de productos en una estructura
--   jerárquica (cada categoría puede tener una `parent_id`).
-- Notas:
--   - Útil para filtros y navegaciones en el catálogo.
--   - `parent_id` usa ON DELETE SET NULL para evitar borrados
--     en cascada accidentales.
-- ---------------------------------------------------------
CREATE TABLE client (
  client_id          INT AUTO_INCREMENT PRIMARY KEY,
  full_name          VARCHAR(100) NOT NULL,
  phone              VARCHAR(20)  NULL,
  email              VARCHAR(150) NULL,
  telegram_username  VARCHAR(50)  NULL,        -- no siempre es único
  telegram_user_id   BIGINT UNSIGNED NULL,     -- este sí suele ser único

  client_type        ENUM('normal','premium') NOT NULL DEFAULT 'normal',
  status             ENUM('active','inactive','blocked') NOT NULL DEFAULT 'active',

  registered_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at         DATETIME NULL,            -- soft-delete (opcional)

  -- auditoría (opcional): quién creó/actualizó el cliente
  created_by         INT NULL,
  updated_by         INT NULL,

  -- Unicidades prácticas (permiten múltiples NULLs)
  CONSTRAINT uq_client_phone         UNIQUE (phone),
  CONSTRAINT uq_client_email         UNIQUE (email),
  CONSTRAINT uq_client_telegram_id   UNIQUE (telegram_user_id),

  CONSTRAINT fk_client_created_by FOREIGN KEY (created_by)
    REFERENCES app_user(user_id) ON DELETE SET NULL ON UPDATE CASCADE,

  CONSTRAINT fk_client_updated_by FOREIGN KEY (updated_by)
    REFERENCES app_user(user_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_client_name           ON client (full_name);
CREATE INDEX idx_client_type_status    ON client (client_type, status);
CREATE INDEX idx_client_registered_at  ON client (registered_at);


-- CATEGORÍAS (normaliza la categoría)
CREATE TABLE category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  parent_id   INT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT uq_category_name UNIQUE (name),
  CONSTRAINT fk_category_parent
    FOREIGN KEY (parent_id) REFERENCES category(category_id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ---------------------------------------------------------
-- TABLA: product
-- Propósito:
--   Almacenar la información maestra de productos, incluyendo
--   precio base, stock y estado. Se busca conservar un
--   "snapshot" del catálogo de productos para operaciones de
--   venta y reportes.
-- Notas importantes:
--   - `price` y `stock` tienen CHECK para evitar valores negativos.
--   - `sku` es opcional pero recomendable para integraciones.
-- ---------------------------------------------------------
CREATE TABLE product (
  product_id   INT AUTO_INCREMENT PRIMARY KEY,
  sku          VARCHAR(64) NULL,                       -- SKU opcional, utilísimo para integración
  name         VARCHAR(150) NOT NULL,
  description  TEXT,
  image_url    VARCHAR(255),
  category_id  INT NULL,
  price        DECIMAL(10,2) NOT NULL CHECK (price >= 0),
  stock        INT UNSIGNED NOT NULL DEFAULT 0 CHECK (stock >= 0),
  status       ENUM('draft','active','archived') NOT NULL DEFAULT 'active',
  created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT fk_product_category
    FOREIGN KEY (category_id) REFERENCES category(category_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  CONSTRAINT uq_product_sku UNIQUE (sku)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_product_name       ON product (name);
CREATE FULLTEXT INDEX ftx_product_nd ON product (name, description); -- si usarás búsqueda de texto

-- ---------------------------------------------------------
-- TABLA: catalog
-- Propósito:
--   Definir campañas o agrupaciones de productos con descuentos
--   y visibilidad controlada (por ejemplo, solo para clientes
--   premium). Incluye periodos de vigencia y flags de visibilidad.
-- ---------------------------------------------------------
CREATE TABLE catalog (
  catalog_id          INT AUTO_INCREMENT PRIMARY KEY,
  name                VARCHAR(120) NOT NULL,
  description         TEXT,
  discount_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.00 CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
  start_date          DATE NULL,
  end_date            DATE NULL,
  visible_to          ENUM('todos','premium','interno') NOT NULL DEFAULT 'todos',
  active              BOOLEAN NOT NULL DEFAULT TRUE,  -- BOOLEAN es alias de TINYINT(1) en MySQL
  created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  CONSTRAINT uq_catalog_name UNIQUE (name),
  CONSTRAINT chk_catalog_dates CHECK (end_date IS NULL OR start_date IS NULL OR start_date <= end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_catalog_active_dates ON catalog (active, start_date, end_date, visible_to);

-- ---------------------------------------------------------
-- TABLA: catalog_product
-- Propósito:
--   Asociar productos a catálogos con precios especiales y/o
--   stock asignado para la campaña. Contiene reglas para evitar
--   inconsistencias mediante triggers (p. ej. assigned_stock).
-- ---------------------------------------------------------
CREATE TABLE catalog_product (
  catalog_id     INT NOT NULL,
  product_id     INT NOT NULL,
  special_price  DECIMAL(10,2) NULL CHECK (special_price IS NULL OR special_price >= 0),
  assigned_stock INT UNSIGNED NULL CHECK (assigned_stock IS NULL OR assigned_stock >= 0),
  PRIMARY KEY (catalog_id, product_id),

  CONSTRAINT fk_cp_catalog
    FOREIGN KEY (catalog_id) REFERENCES catalog(catalog_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_cp_product
    FOREIGN KEY (product_id) REFERENCES product(product_id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_cp_product ON catalog_product (product_id);

-- ---------------------------------------------------------
-- VISTA: v_catalog_effective_price
-- Propósito:
--   Proveer el precio "efectivo" de un producto dentro de un
--   catálogo en un momento dado. Prioriza `special_price`, si
--   no existe toma el `discount_percentage` del catálogo, y
--   si no aplica devuelve el `price` base del producto.
-- Uso:
--   Ideal para listados de catálogo con precio ya calculado.
-- ---------------------------------------------------------
CREATE OR REPLACE VIEW v_catalog_effective_price AS
SELECT
  cp.catalog_id,
  cp.product_id,
  p.name        AS product_name,
  c.name        AS catalog_name,
  p.price       AS base_price,
  c.discount_percentage,
  cp.special_price,
  CASE
    WHEN cp.special_price IS NOT NULL THEN cp.special_price
    WHEN c.discount_percentage > 0 THEN ROUND(p.price * (1 - c.discount_percentage/100), 2)
    ELSE p.price
  END AS effective_price
FROM catalog_product cp
JOIN product p  ON p.product_id  = cp.product_id
JOIN catalog c  ON c.catalog_id  = cp.catalog_id
WHERE c.active = 1
  AND (c.start_date IS NULL OR c.start_date <= CURRENT_DATE())
  AND (c.end_date   IS NULL OR c.end_date   >= CURRENT_DATE());

-- ---------------------------------------------------------
-- TRIGGERS: validaciones en catalog_product
-- Propósito:
--   Evitar inconsistencias cuando se asocian productos a
--   catálogos: p. ej. que assigned_stock sea mayor al stock
--   disponible o que special_price supere el precio base.
-- Consejo:
--   Adapte los mensajes y reglas a su política comercial.
-- ---------------------------------------------------------
DELIMITER //
CREATE TRIGGER trg_cp_before_ins
BEFORE INSERT ON catalog_product
FOR EACH ROW
BEGIN
  DECLARE base_price DECIMAL(10,2);
  DECLARE prod_stock INT UNSIGNED;

  SELECT price, stock INTO base_price, prod_stock
  FROM product
  WHERE product_id = NEW.product_id;

  IF NEW.assigned_stock IS NOT NULL AND NEW.assigned_stock > prod_stock THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'assigned_stock excede el stock disponible del producto';
  END IF;

  IF NEW.special_price IS NOT NULL AND NEW.special_price > base_price THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'special_price no puede ser mayor que el precio base';
  END IF;
END//
CREATE TRIGGER trg_cp_before_upd
BEFORE UPDATE ON catalog_product
FOR EACH ROW
BEGIN
  DECLARE base_price DECIMAL(10,2);
  DECLARE prod_stock INT UNSIGNED;

  SELECT price, stock INTO base_price, prod_stock
  FROM product
  WHERE product_id = NEW.product_id;

  IF NEW.assigned_stock IS NOT NULL AND NEW.assigned_stock > prod_stock THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'assigned_stock excede el stock disponible del producto';
  END IF;

  IF NEW.special_price IS NOT NULL AND NEW.special_price > base_price THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'special_price no puede ser mayor que el precio base';
  END IF;
END//
DELIMITER ;



-- ---------------------------------------------------------
-- TABLA: customer_order
-- Propósito:
--   Encabezado del pedido que referencia al cliente y guarda
--   totales calculados, estado del pedido y del pago.
-- Notas:
--   - `grand_total` es una columna generada basada en los totales
--     parciales para proteger consistencia.
--   - Triggers y procedimientos mantienen los totales sincronizados
--     con el detalle (`order_item`).
-- ---------------------------------------------------------
CREATE TABLE customer_order (
  order_id        INT AUTO_INCREMENT PRIMARY KEY,
  client_id       INT NOT NULL,                                -- FK a cliente
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  -- Estados operativos y de pago
  status          ENUM('borrador','confirmado','preparando','enviado','entregado','cancelado','devuelto')
                  NOT NULL DEFAULT 'borrador',
  payment_status  ENUM('pendiente','pagado','reembolsado','fallido')
                  NOT NULL DEFAULT 'pendiente',

  -- Totales del pedido (encabezado)
  subtotal        DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (subtotal >= 0),
  discount_total  DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (discount_total >= 0),
  tax_total       DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (tax_total >= 0),
  shipping_total  DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (shipping_total >= 0),
  grand_total     DECIMAL(12,2) GENERATED ALWAYS AS (
                     ROUND(subtotal - discount_total + tax_total + shipping_total, 2)
                   ) STORED,

  notes           TEXT NULL,

  -- Auditoría (si usas app_user)
  created_by      INT NULL,
  updated_by      INT NULL,

  CONSTRAINT fk_order_client
    FOREIGN KEY (client_id) REFERENCES client(client_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,

  CONSTRAINT fk_order_created_by
    FOREIGN KEY (created_by) REFERENCES app_user(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  CONSTRAINT fk_order_updated_by
    FOREIGN KEY (updated_by) REFERENCES app_user(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_order_client_created     ON customer_order (client_id, created_at);
CREATE INDEX idx_order_status_payment     ON customer_order (status, payment_status);
CREATE INDEX idx_order_updated_at         ON customer_order (updated_at);

-- ---------------------------------------------------------
-- TABLA: order_item
-- Propósito:
--   Detalle de cada pedido: producto, cantidad y snapshot de
--   precios/tasas en el momento de la compra. Contiene columnas
--   GENERATED para subtotal, impuestos y totales de línea.
-- Consideraciones:
--   - Mantener snapshot para auditoría y para evitar problemas
--     cuando el precio del producto cambia posteriormente.
-- ---------------------------------------------------------
CREATE TABLE order_item (
  order_id        INT NOT NULL,
  product_id      INT NOT NULL,
  quantity        INT UNSIGNED NOT NULL CHECK (quantity > 0),

  -- Snapshot del producto al momento del pedido
  product_name    VARCHAR(150) NOT NULL,
  sku             VARCHAR(64) NULL,

  -- Precio e impuestos al momento
  unit_price      DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
  discount_pct    DECIMAL(5,2)  NULL CHECK (discount_pct >= 0 AND discount_pct <= 100),
  discount_amount DECIMAL(10,2) NULL CHECK (discount_amount >= 0),
  tax_rate        DECIMAL(5,2)  NOT NULL DEFAULT 0.00 CHECK (tax_rate >= 0 AND tax_rate <= 100),

  -- Totales de línea (generados)
  line_subtotal   DECIMAL(12,2) GENERATED ALWAYS AS (
                     ROUND(quantity * unit_price, 2)
                   ) STORED,
  line_discount   DECIMAL(12,2) GENERATED ALWAYS AS (
                     ROUND(
                       COALESCE(discount_amount, (quantity * unit_price) * COALESCE(discount_pct,0)/100)
                     , 2)
                   ) STORED,
  line_tax_base   DECIMAL(12,2) GENERATED ALWAYS AS (
                     ROUND(line_subtotal - line_discount, 2)
                   ) STORED,
  line_tax        DECIMAL(12,2) GENERATED ALWAYS AS (
                     ROUND(line_tax_base * tax_rate/100, 2)
                   ) STORED,
  line_total      DECIMAL(12,2) GENERATED ALWAYS AS (
                     line_tax_base + line_tax
                   ) STORED,

  PRIMARY KEY (order_id, product_id),

  CONSTRAINT fk_oi_order
    FOREIGN KEY (order_id)   REFERENCES customer_order(order_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_oi_product
    FOREIGN KEY (product_id) REFERENCES product(product_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_oi_product        ON order_item (product_id);
CREATE INDEX idx_oi_totals         ON order_item (order_id, line_total);

-- ---------------------------------------------------------
-- TABLA: invoice
-- Propósito:
--   Facturas asociadas a pedidos. Cada factura tiene su número
--   y estado; la tabla asegura unicidad por (order_id, invoice_number).
-- Reglas de negocio:
--   - Se impone (mediante triggers) que no se avance el estado del
--     pedido sin al menos una factura cuando aplique.
-- ---------------------------------------------------------
CREATE TABLE invoice (
  invoice_id      INT AUTO_INCREMENT PRIMARY KEY,
  order_id        INT NOT NULL,
  invoice_number  VARCHAR(40) NOT NULL,            -- número de factura por pedido
  series          VARCHAR(10) NULL,                -- opcional: serie
  issued_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_at          DATETIME NULL,
  currency_code   CHAR(3) NOT NULL DEFAULT 'MXN',
  status          ENUM('emitida','pagada','parcial','cancelada') NOT NULL DEFAULT 'emitida',
  notes           TEXT NULL,

  CONSTRAINT uq_invoice_order_number UNIQUE (order_id, invoice_number),

  CONSTRAINT fk_invoice_order
    FOREIGN KEY (order_id) REFERENCES customer_order(order_id)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_invoice_issued_at  ON invoice (issued_at);
CREATE INDEX idx_invoice_number     ON invoice (invoice_number);

-- VISTA: totales calculados desde el detalle (auditoría/reportes)
CREATE OR REPLACE VIEW v_order_totals AS
SELECT
  oi.order_id,
  ROUND(SUM(oi.line_subtotal), 2) AS v_subtotal,
  ROUND(SUM(oi.line_discount), 2) AS v_discount_total,
  ROUND(SUM(oi.line_tax), 2)      AS v_tax_total,
  ROUND(SUM(oi.line_total), 2)    AS v_items_total
FROM order_item oi
GROUP BY oi.order_id;

-- SP: recalcular totales del encabezado desde el detalle
DELIMITER //
CREATE PROCEDURE sp_recalc_order_totals(IN p_order_id INT)
BEGIN
  DECLARE v_sub DECIMAL(12,2) DEFAULT 0.00;
  DECLARE v_dis DECIMAL(12,2) DEFAULT 0.00;
  DECLARE v_tax DECIMAL(12,2) DEFAULT 0.00;

  SELECT
    COALESCE(SUM(line_subtotal),0),
    COALESCE(SUM(line_discount),0),
    COALESCE(SUM(line_tax),0)
  INTO v_sub, v_dis, v_tax
  FROM order_item
  WHERE order_id = p_order_id;

  UPDATE customer_order
  SET
    subtotal       = v_sub,
    discount_total = v_dis,
    tax_total      = v_tax
  WHERE order_id = p_order_id;
END//
DELIMITER ;

-- Triggers: recalcular totales del pedido al tocar el detalle
DELIMITER //
CREATE TRIGGER trg_oi_ai AFTER INSERT ON order_item
FOR EACH ROW BEGIN
  CALL sp_recalc_order_totals(NEW.order_id);
END//
CREATE TRIGGER trg_oi_au AFTER UPDATE ON order_item
FOR EACH ROW BEGIN
  CALL sp_recalc_order_totals(NEW.order_id);
END//
CREATE TRIGGER trg_oi_ad AFTER DELETE ON order_item
FOR EACH ROW BEGIN
  CALL sp_recalc_order_totals(OLD.order_id);
END//
DELIMITER ;

-- Trigger: exigir al menos una factura para avanzar de 'borrador'
DELIMITER //
CREATE TRIGGER trg_order_require_invoice
BEFORE UPDATE ON customer_order
FOR EACH ROW
BEGIN
  IF NEW.status IN ('confirmado','preparando','enviado','entregado','devuelto') THEN
    IF (SELECT COUNT(*) FROM invoice WHERE order_id = NEW.order_id) = 0 THEN
      SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El pedido requiere al menos una factura para cambiar a ese estado.';
    END IF;
  END IF;
END//
DELIMITER ;

-- Trigger: impedir borrar la última factura si el pedido no está en borrador/cancelado
DELIMITER //
CREATE TRIGGER trg_invoice_before_delete
BEFORE DELETE ON invoice
FOR EACH ROW
BEGIN
  DECLARE v_status VARCHAR(20);
  DECLARE v_count  INT;

  SELECT status INTO v_status
  FROM customer_order
  WHERE order_id = OLD.order_id
  FOR UPDATE;

  SELECT COUNT(*) INTO v_count
  FROM invoice
  WHERE order_id = OLD.order_id;

  IF v_count = 1 AND v_status NOT IN ('borrador','cancelado') THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'No puedes eliminar la última factura de un pedido activo.';
  END IF;
END//
DELIMITER ;













-- Conversaciones
CREATE TABLE conversation (
  conversation_id   INT AUTO_INCREMENT PRIMARY KEY,
  client_id         INT NULL,  -- si borras el cliente, se mantiene la conversación
  channel           ENUM('web','telegram','whatsapp','sms','email','other')
                     NOT NULL DEFAULT 'web',
  external_chat_id  VARCHAR(128) NULL,  -- p.ej. chat_id de Telegram (opcional)
  active            BOOLEAN NOT NULL DEFAULT TRUE,
  handled_by_bot    BOOLEAN NOT NULL DEFAULT TRUE,

  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  last_message_at   DATETIME NULL,

  CONSTRAINT fk_conv_client
    FOREIGN KEY (client_id) REFERENCES client(client_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  -- Evita duplicados del mismo chat externo por canal (permite NULL)
  CONSTRAINT uq_conv_channel_ext UNIQUE (channel, external_chat_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_conversation_client   ON conversation (client_id);
CREATE INDEX idx_conversation_lastmsg  ON conversation (last_message_at);

-- Mensajes
CREATE TABLE message (
  message_id          INT AUTO_INCREMENT PRIMARY KEY,
  conversation_id     INT NOT NULL,
  sender              ENUM('client','user','bot') NOT NULL,  -- 'user' = agente interno
  content             MEDIUMTEXT NOT NULL,
  external_message_id VARCHAR(128) NULL,  -- id del mensaje en el canal (opcional)
  created_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_msg_conversation
    FOREIGN KEY (conversation_id) REFERENCES conversation(conversation_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  -- Evita duplicar el mismo mensaje externo dentro de la conversación
  CONSTRAINT uq_msg_conv_ext UNIQUE (conversation_id, external_message_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_message_created_at ON message (created_at);

-- Mantén actualizado el "último mensaje" de la conversación (simple y útil)
DELIMITER //
CREATE TRIGGER trg_msg_ai
AFTER INSERT ON message
FOR EACH ROW
BEGIN
  UPDATE conversation
     SET last_message_at = NEW.created_at
   WHERE conversation_id = NEW.conversation_id;
END//
DELIMITER ;




-- =========================================================
-- SECCIÓN: Soporte (tickets), calendario y alertas
-- Propósito:
--   Componentes simples para gestionar tickets de soporte,
--   eventos de calendario relacionados y alertas/reminders.
-- Diseño:
--   - Tablas ligeras pensadas para integración con el resto del
--     sistema; use índices y triggers para eficiencia básica.
-- =========================================================
-- ---------------------------------------------------------
-- TABLA: ticket
-- Propósito:
--   Registrar incidencias o solicitudes de clientes, con estado,
--   prioridad, asignación y fechas clave. Ideal para flujo de
--   soporte básico dentro de OmniDesk.
-- ---------------------------------------------------------
CREATE TABLE ticket (
  ticket_id    INT AUTO_INCREMENT PRIMARY KEY,
  client_id    INT NOT NULL,                                -- cliente que reporta
  subject      VARCHAR(150) NOT NULL,                       -- asunto
  description  TEXT NULL,                                   -- detalle
  priority     ENUM('alta','media','baja') NOT NULL DEFAULT 'media',
  status       ENUM('abierto','en_progreso','cerrado') NOT NULL DEFAULT 'abierto',
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- fecha del ticket
  due_at       DATETIME NULL,                               -- fecha tentativa de resolución
  resolved_at  DATETIME NULL,                               -- cuándo se resolvió (si aplica)
  assigned_to  INT NULL,                                    -- agente asignado (opcional)

  CONSTRAINT fk_ticket_client
    FOREIGN KEY (client_id) REFERENCES client(client_id)
    ON DELETE RESTRICT ON UPDATE CASCADE,

  CONSTRAINT fk_ticket_assigned
    FOREIGN KEY (assigned_to) REFERENCES app_user(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK (due_at IS NULL OR due_at >= created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_ticket_client     ON ticket (client_id);
CREATE INDEX idx_ticket_status     ON ticket (status, priority);
CREATE INDEX idx_ticket_created_at ON ticket (created_at);
CREATE INDEX idx_ticket_due_at     ON ticket (due_at);

-- Marca resolved_at automáticamente al cerrar
DELIMITER //
CREATE TRIGGER trg_ticket_set_resolved
BEFORE UPDATE ON ticket
FOR EACH ROW
BEGIN
  IF NEW.status = 'cerrado' AND OLD.status <> 'cerrado' AND NEW.resolved_at IS NULL THEN
    SET NEW.resolved_at = CURRENT_TIMESTAMP;
  END IF;
END//
DELIMITER ;

-- ===========================
-- EVENTOS DE CALENDARIO
-- ===========================
CREATE TABLE calendar_event (
  event_id     INT AUTO_INCREMENT PRIMARY KEY,
  title        VARCHAR(150) NOT NULL,
  description  TEXT NULL,
  start_time   DATETIME NOT NULL,
  end_time     DATETIME NOT NULL,
  created_by   INT NULL,          -- admin/empleado que crea el evento
  ticket_id    INT NULL,          -- opcional: evento ligado a ticket

  CONSTRAINT fk_event_creator
    FOREIGN KEY (created_by) REFERENCES app_user(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  CONSTRAINT fk_event_ticket
    FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  CHECK (end_time >= start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_event_start   ON calendar_event (start_time);
CREATE INDEX idx_event_creator ON calendar_event (created_by);
CREATE INDEX idx_event_ticket  ON calendar_event (ticket_id);

-- ===========================
-- ALERTAS (recordatorios / fallas)
-- Pueden asociarse a un ticket o a un evento del calendario.
-- ===========================
CREATE TABLE alert (
  alert_id     INT AUTO_INCREMENT PRIMARY KEY,
  alert_time   DATETIME NOT NULL,             -- cuándo disparar/mostrar
  message      VARCHAR(255) NOT NULL,         -- texto breve
  kind         ENUM('ticket','event','incident') NOT NULL DEFAULT 'incident',
  ticket_id    INT NULL,
  event_id     INT NULL,
  sent         BOOLEAN NOT NULL DEFAULT FALSE, -- ya se envió/mostró
  created_by   INT NULL,                       -- quién la creó (opcional)
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_alert_ticket
    FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_alert_event
    FOREIGN KEY (event_id) REFERENCES calendar_event(event_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_alert_creator
    FOREIGN KEY (created_by) REFERENCES app_user(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE,

  -- al menos una referencia (ticket o evento)
  CHECK (ticket_id IS NOT NULL OR event_id IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE INDEX idx_alert_time ON alert (alert_time);
CREATE INDEX idx_alert_sent ON alert (sent, kind);




