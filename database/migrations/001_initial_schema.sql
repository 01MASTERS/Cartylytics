-- ============================================================
-- Cartlytics – Customer, Sales & Revenue Analytics Platform
-- Database Schema v1.0
-- ============================================================

-- Database created via Aiven console

-- ============================================================
-- CATEGORIES
-- ============================================================
CREATE TABLE categories (
    id            INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    name          VARCHAR(100)     NOT NULL,
    slug          VARCHAR(110)     NOT NULL,
    description   TEXT,
    parent_id     INT UNSIGNED     DEFAULT NULL,
    is_active     TINYINT(1)       NOT NULL DEFAULT 1,
    created_at    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_categories_slug (slug),
    KEY idx_categories_parent (parent_id),
    KEY idx_categories_active (is_active),
    CONSTRAINT fk_categories_parent
        FOREIGN KEY (parent_id) REFERENCES categories (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- PRODUCTS
-- ============================================================
CREATE TABLE products (
    id              INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    sku             VARCHAR(50)      NOT NULL,
    name            VARCHAR(255)     NOT NULL,
    description     TEXT,
    category_id     INT UNSIGNED     NOT NULL,
    cost_price      DECIMAL(12, 2)   NOT NULL DEFAULT 0.00,
    selling_price   DECIMAL(12, 2)   NOT NULL DEFAULT 0.00,
    stock_qty       INT              NOT NULL DEFAULT 0,
    brand           VARCHAR(100),
    is_active       TINYINT(1)       NOT NULL DEFAULT 1,
    created_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_products_sku (sku),
    KEY idx_products_category (category_id),
    KEY idx_products_active (is_active),
    KEY idx_products_brand (brand),
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- CUSTOMERS
-- ============================================================
CREATE TABLE customers (
    id              INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    email           VARCHAR(255)     NOT NULL,
    first_name      VARCHAR(100)     NOT NULL,
    last_name       VARCHAR(100)     NOT NULL,
    phone           VARCHAR(20),
    gender          ENUM('Male','Female','Other','Unknown') NOT NULL DEFAULT 'Unknown',
    date_of_birth   DATE,
    city            VARCHAR(100),
    state           VARCHAR(100),
    region          ENUM('North','South','East','West','Northeast','Northwest','Southeast','Southwest','Central')
                    NOT NULL DEFAULT 'Central',
    country         VARCHAR(100)     NOT NULL DEFAULT 'United States',
    zip_code        VARCHAR(20),
    segment         ENUM('Consumer','Corporate','Home Office','Small Business')
                    NOT NULL DEFAULT 'Consumer',
    is_active       TINYINT(1)       NOT NULL DEFAULT 1,
    created_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_customers_email (email),
    KEY idx_customers_region (region),
    KEY idx_customers_segment (segment),
    KEY idx_customers_state (state),
    KEY idx_customers_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- ORDERS
-- ============================================================
CREATE TABLE orders (
    id              INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    order_number    VARCHAR(30)      NOT NULL,
    customer_id     INT UNSIGNED     NOT NULL,
    status          ENUM('pending','confirmed','shipped','delivered','returned','cancelled')
                    NOT NULL DEFAULT 'pending',
    order_date      DATETIME         NOT NULL,
    shipped_date    DATETIME,
    delivered_date  DATETIME,
    shipping_city   VARCHAR(100),
    shipping_state  VARCHAR(100),
    shipping_region ENUM('North','South','East','West','Northeast','Northwest','Southeast','Southwest','Central')
                    NOT NULL DEFAULT 'Central',
    shipping_country VARCHAR(100)    NOT NULL DEFAULT 'United States',
    shipping_zip    VARCHAR(20),
    payment_method  ENUM('Credit Card','Debit Card','PayPal','Bank Transfer','Cash on Delivery')
                    NOT NULL DEFAULT 'Credit Card',
    discount_pct    DECIMAL(5, 2)    NOT NULL DEFAULT 0.00,
    shipping_fee    DECIMAL(10, 2)   NOT NULL DEFAULT 0.00,
    subtotal        DECIMAL(14, 2)   NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(14, 2)   NOT NULL DEFAULT 0.00,
    total_amount    DECIMAL(14, 2)   NOT NULL DEFAULT 0.00,
    notes           TEXT,
    created_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    UNIQUE KEY uq_orders_number (order_number),
    KEY idx_orders_customer (customer_id),
    KEY idx_orders_status (status),
    KEY idx_orders_date (order_date),
    KEY idx_orders_region (shipping_region),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- ORDER ITEMS
-- ============================================================
CREATE TABLE order_items (
    id              INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    order_id        INT UNSIGNED     NOT NULL,
    product_id      INT UNSIGNED     NOT NULL,
    quantity        INT UNSIGNED     NOT NULL DEFAULT 1,
    unit_price      DECIMAL(12, 2)   NOT NULL,
    unit_cost       DECIMAL(12, 2)   NOT NULL DEFAULT 0.00,
    discount_pct    DECIMAL(5, 2)    NOT NULL DEFAULT 0.00,
    line_revenue    DECIMAL(14, 2)   NOT NULL
                    COMMENT 'quantity * unit_price * (1 - discount_pct/100)',
    line_cost       DECIMAL(14, 2)   NOT NULL
                    COMMENT 'quantity * unit_cost',
    line_profit     DECIMAL(14, 2)   NOT NULL
                    COMMENT 'line_revenue - line_cost',
    created_at      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    KEY idx_oi_order (order_id),
    KEY idx_oi_product (product_id),
    CONSTRAINT fk_oi_order
        FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    CONSTRAINT fk_oi_product
        FOREIGN KEY (product_id) REFERENCES products (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- ANALYTICS VIEWS
-- ============================================================

-- Monthly revenue & profit
CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    YEAR(o.order_date)                 AS year,
    MONTH(o.order_date)                AS month_num,
    COUNT(DISTINCT o.id)               AS total_orders,
    COUNT(DISTINCT o.customer_id)      AS unique_customers,
    ROUND(SUM(oi.line_revenue), 2)     AS revenue,
    ROUND(SUM(oi.line_cost), 2)        AS cost,
    ROUND(SUM(oi.line_profit), 2)      AS profit,
    ROUND(SUM(oi.line_profit) / NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.status NOT IN ('returned', 'cancelled')
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m'), YEAR(o.order_date), MONTH(o.order_date)
ORDER BY month;


-- Category-wise revenue & profit
CREATE OR REPLACE VIEW vw_category_sales AS
SELECT
    c.id                               AS category_id,
    c.name                             AS category_name,
    COUNT(DISTINCT o.id)               AS total_orders,
    SUM(oi.quantity)                   AS units_sold,
    ROUND(SUM(oi.line_revenue), 2)     AS revenue,
    ROUND(SUM(oi.line_cost), 2)        AS cost,
    ROUND(SUM(oi.line_profit), 2)      AS profit,
    ROUND(SUM(oi.line_profit) / NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
FROM categories c
JOIN products p     ON p.category_id = c.id
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o       ON o.id = oi.order_id
WHERE o.status NOT IN ('returned', 'cancelled')
GROUP BY c.id, c.name;


-- Top products
CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    p.id                               AS product_id,
    p.sku,
    p.name                             AS product_name,
    c.name                             AS category_name,
    p.brand,
    COUNT(DISTINCT o.id)               AS total_orders,
    SUM(oi.quantity)                   AS units_sold,
    ROUND(SUM(oi.line_revenue), 2)     AS revenue,
    ROUND(SUM(oi.line_profit), 2)      AS profit,
    ROUND(SUM(oi.line_profit) / NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
FROM products p
JOIN categories c   ON c.id = p.category_id
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o       ON o.id = oi.order_id
WHERE o.status NOT IN ('returned', 'cancelled')
GROUP BY p.id, p.sku, p.name, c.name, p.brand;


-- Customer lifetime value & purchase frequency
CREATE OR REPLACE VIEW vw_customer_stats AS
SELECT
    cu.id                              AS customer_id,
    CONCAT(cu.first_name, ' ', cu.last_name) AS customer_name,
    cu.email,
    cu.segment,
    cu.region,
    cu.state,
    MIN(o.order_date)                  AS first_order_date,
    MAX(o.order_date)                  AS last_order_date,
    COUNT(DISTINCT o.id)               AS total_orders,
    SUM(oi.quantity)                   AS total_items,
    ROUND(SUM(oi.line_revenue), 2)     AS total_spent,
    ROUND(SUM(oi.line_revenue) / COUNT(DISTINCT o.id), 2) AS avg_order_value,
    CASE WHEN COUNT(DISTINCT o.id) > 1 THEN 'Returning' ELSE 'New' END AS customer_type
FROM customers cu
JOIN orders o       ON o.customer_id = cu.id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.status NOT IN ('returned', 'cancelled')
GROUP BY cu.id, cu.first_name, cu.last_name, cu.email, cu.segment, cu.region, cu.state;


-- Regional sales
CREATE OR REPLACE VIEW vw_regional_sales AS
SELECT
    o.shipping_region                  AS region,
    o.shipping_state                   AS state,
    COUNT(DISTINCT o.id)               AS total_orders,
    COUNT(DISTINCT o.customer_id)      AS unique_customers,
    ROUND(SUM(oi.line_revenue), 2)     AS revenue,
    ROUND(SUM(oi.line_profit), 2)      AS profit,
    ROUND(SUM(oi.line_profit) / NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.status NOT IN ('returned', 'cancelled')
GROUP BY o.shipping_region, o.shipping_state;
