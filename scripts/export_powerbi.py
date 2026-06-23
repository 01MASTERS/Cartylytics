"""
Cartlytics – Power BI Export Script
Exports analysis-ready CSVs from MySQL views for Power BI consumption.
Run: python scripts/export_powerbi.py
"""

import os
import logging
from datetime import datetime

import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s")
log = logging.getLogger("pbi_export")

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets", "powerbi_exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "cartlytics"),
    )


EXPORTS = {
    "monthly_sales":         "SELECT * FROM vw_monthly_sales",
    "category_sales":        "SELECT * FROM vw_category_sales",
    "product_performance":   "SELECT * FROM vw_product_performance ORDER BY revenue DESC",
    "customer_stats":        "SELECT * FROM vw_customer_stats",
    "regional_sales":        "SELECT * FROM vw_regional_sales",
    "orders_flat": """
        SELECT
            o.id            AS order_id,
            o.order_number,
            o.order_date,
            o.status,
            o.shipping_region AS region,
            o.shipping_state  AS state,
            o.payment_method,
            o.discount_pct,
            o.shipping_fee,
            o.total_amount,
            c.id            AS customer_id,
            CONCAT(c.first_name,' ',c.last_name) AS customer_name,
            c.segment       AS customer_segment,
            oi.product_id,
            p.name          AS product_name,
            cat.name        AS category_name,
            oi.quantity,
            oi.unit_price,
            oi.unit_cost,
            oi.line_revenue,
            oi.line_cost,
            oi.line_profit
        FROM orders o
        JOIN customers c   ON c.id = o.customer_id
        JOIN order_items oi ON oi.order_id = o.id
        JOIN products p    ON p.id = oi.product_id
        JOIN categories cat ON cat.id = p.category_id
        WHERE o.status NOT IN ('returned','cancelled')
    """,
}


def run():
    conn = get_conn()
    for name, sql in EXPORTS.items():
        df = pd.read_sql(sql, conn)
        out = os.path.join(EXPORT_DIR, f"{name}_{TIMESTAMP}.csv")
        df.to_csv(out, index=False)
        log.info("  ✓ %-30s  %d rows", name + ".csv", len(df))
    conn.close()
    log.info("Power BI exports saved to datasets/powerbi_exports/")


if __name__ == "__main__":
    run()
