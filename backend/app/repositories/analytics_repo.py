"""
Cartlytics – Analytics Repository
All SQL queries live here. Clean separation from business logic.
"""

from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import text


def _date_filter(start: Optional[date], end: Optional[date], alias: str = "o") -> str:
    parts = []
    if start:
        parts.append(f"{alias}.order_date >= :start_date")
    if end:
        parts.append(f"{alias}.order_date <= :end_date")
    return ("AND " + " AND ".join(parts)) if parts else ""


def _cat_filter(category_id: Optional[int]) -> str:
    return "AND c.id = :category_id" if category_id else ""


def _params(start, end, category_id=None):
    p = {}
    if start:
        p["start_date"] = start
    if end:
        p["end_date"] = end
    if category_id:
        p["category_id"] = category_id
    return p


# ── KPIs ───────────────────────────────────────────────────────────────────────

def get_kpis(db: Session, start: Optional[date], end: Optional[date]) -> dict:
    df = _date_filter(start, end)
    sql = text(f"""
        SELECT
            COALESCE(SUM(oi.line_revenue), 0)                           AS total_revenue,
            COALESCE(SUM(oi.line_profit),  0)                           AS total_profit,
            COUNT(DISTINCT o.id)                                         AS total_orders,
            COALESCE(SUM(oi.line_revenue) / NULLIF(COUNT(DISTINCT o.id), 0), 0) AS avg_order_value,
            COUNT(DISTINCT o.customer_id)                                AS total_customers
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status NOT IN ('returned','cancelled')
        {df}
    """)
    row = db.execute(sql, _params(start, end)).mappings().one()

    # prior-period for growth %
    growth_sql = text(f"""
        SELECT
            COALESCE(SUM(oi.line_revenue), 0) AS prev_revenue,
            COALESCE(SUM(oi.line_profit),  0) AS prev_profit
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status NOT IN ('returned','cancelled')
          AND o.order_date < :cutoff
          AND o.order_date >= DATE_SUB(:cutoff, INTERVAL 1 YEAR)
    """)
    cutoff = start or date.today()
    prev = db.execute(growth_sql, {"cutoff": cutoff}).mappings().one()

    def growth_pct(curr, prev_val):
        if not prev_val or prev_val == 0:
            return None
        return round((curr - prev_val) / abs(prev_val) * 100, 2)

    # repeat customer rate
    rcr_sql = text(f"""
        SELECT
            COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_id END) AS repeat_c,
            COUNT(DISTINCT customer_id) AS total_c
        FROM (
            SELECT customer_id, COUNT(id) AS order_count
            FROM orders o
            WHERE o.status NOT IN ('returned','cancelled')
            {df}
            GROUP BY customer_id
        ) t
    """)
    rcr = db.execute(rcr_sql, _params(start, end)).mappings().one()
    repeat_rate = round(
        rcr["repeat_c"] / rcr["total_c"] * 100 if rcr["total_c"] else 0, 2
    )

    return {
        "total_revenue":        round(float(row["total_revenue"]), 2),
        "total_profit":         round(float(row["total_profit"]),  2),
        "total_orders":         int(row["total_orders"]),
        "avg_order_value":      round(float(row["avg_order_value"]), 2),
        "total_customers":      int(row["total_customers"]),
        "revenue_growth_pct":   growth_pct(float(row["total_revenue"]), float(prev["prev_revenue"])),
        "profit_growth_pct":    growth_pct(float(row["total_profit"]),  float(prev["prev_profit"])),
        "repeat_customer_rate": repeat_rate,
    }


# ── Monthly Sales ──────────────────────────────────────────────────────────────

def get_monthly_sales(db: Session, start: Optional[date], end: Optional[date]) -> list:
    df = _date_filter(start, end)
    sql = text(f"""
        SELECT
            DATE_FORMAT(o.order_date, '%Y-%m')        AS month,
            YEAR(o.order_date)                         AS year,
            MONTH(o.order_date)                        AS month_num,
            COUNT(DISTINCT o.id)                       AS total_orders,
            COUNT(DISTINCT o.customer_id)              AS unique_customers,
            ROUND(SUM(oi.line_revenue), 2)             AS revenue,
            ROUND(SUM(oi.line_cost),    2)             AS cost,
            ROUND(SUM(oi.line_profit),  2)             AS profit,
            ROUND(SUM(oi.line_profit) /
                  NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status NOT IN ('returned','cancelled')
        {df}
        GROUP BY DATE_FORMAT(o.order_date,'%Y-%m'), YEAR(o.order_date), MONTH(o.order_date)
        ORDER BY month
    """)
    rows = db.execute(sql, _params(start, end)).mappings().all()
    return [dict(r) for r in rows]


# ── Category Sales ─────────────────────────────────────────────────────────────

def get_category_sales(db: Session, start: Optional[date], end: Optional[date]) -> list:
    df = _date_filter(start, end)
    sql = text(f"""
        SELECT
            c.id                                        AS category_id,
            c.name                                      AS category_name,
            COUNT(DISTINCT o.id)                        AS total_orders,
            SUM(oi.quantity)                            AS units_sold,
            ROUND(SUM(oi.line_revenue), 2)              AS revenue,
            ROUND(SUM(oi.line_cost),    2)              AS cost,
            ROUND(SUM(oi.line_profit),  2)              AS profit,
            ROUND(SUM(oi.line_profit) /
                  NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
        FROM categories c
        JOIN products p     ON p.category_id = c.id
        JOIN order_items oi ON oi.product_id = p.id
        JOIN orders o       ON o.id = oi.order_id
        WHERE o.status NOT IN ('returned','cancelled')
        {df}
        GROUP BY c.id, c.name
        ORDER BY revenue DESC
    """)
    rows = db.execute(sql, _params(start, end)).mappings().all()
    return [dict(r) for r in rows]


# ── Top Products ───────────────────────────────────────────────────────────────

def get_top_products_by_revenue(
    db: Session, start: Optional[date], end: Optional[date],
    category_id: Optional[int], limit: int = 10
) -> list:
    df  = _date_filter(start, end)
    cf  = _cat_filter(category_id)
    sql = text(f"""
        SELECT
            p.id                                        AS product_id,
            p.sku,
            p.name                                      AS product_name,
            c.name                                      AS category_name,
            p.brand,
            COUNT(DISTINCT o.id)                        AS total_orders,
            SUM(oi.quantity)                            AS units_sold,
            ROUND(SUM(oi.line_revenue), 2)              AS revenue,
            ROUND(SUM(oi.line_profit),  2)              AS profit,
            ROUND(SUM(oi.line_profit) /
                  NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
        FROM products p
        JOIN categories c   ON c.id = p.category_id
        JOIN order_items oi ON oi.product_id = p.id
        JOIN orders o       ON o.id = oi.order_id
        WHERE o.status NOT IN ('returned','cancelled')
        {df} {cf}
        GROUP BY p.id, p.sku, p.name, c.name, p.brand
        ORDER BY revenue DESC
        LIMIT :limit
    """)
    p = _params(start, end, category_id)
    p["limit"] = limit
    rows = db.execute(sql, p).mappings().all()
    return [dict(r) for r in rows]


def get_top_products_by_profit(
    db: Session, start: Optional[date], end: Optional[date],
    category_id: Optional[int], limit: int = 10
) -> list:
    df  = _date_filter(start, end)
    cf  = _cat_filter(category_id)
    sql = text(f"""
        SELECT
            p.id                                        AS product_id,
            p.sku,
            p.name                                      AS product_name,
            c.name                                      AS category_name,
            p.brand,
            COUNT(DISTINCT o.id)                        AS total_orders,
            SUM(oi.quantity)                            AS units_sold,
            ROUND(SUM(oi.line_revenue), 2)              AS revenue,
            ROUND(SUM(oi.line_profit),  2)              AS profit,
            ROUND(SUM(oi.line_profit) /
                  NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
        FROM products p
        JOIN categories c   ON c.id = p.category_id
        JOIN order_items oi ON oi.product_id = p.id
        JOIN orders o       ON o.id = oi.order_id
        WHERE o.status NOT IN ('returned','cancelled')
        {df} {cf}
        GROUP BY p.id, p.sku, p.name, c.name, p.brand
        ORDER BY profit DESC
        LIMIT :limit
    """)
    p = _params(start, end, category_id)
    p["limit"] = limit
    rows = db.execute(sql, p).mappings().all()
    return [dict(r) for r in rows]


# ── Customers ──────────────────────────────────────────────────────────────────

def get_top_customers(
    db: Session, start: Optional[date], end: Optional[date], limit: int = 20
) -> list:
    df  = _date_filter(start, end)
    sql = text(f"""
        SELECT
            cu.id                                           AS customer_id,
            CONCAT(cu.first_name,' ',cu.last_name)          AS customer_name,
            cu.email,
            cu.segment,
            cu.region,
            cu.state,
            MIN(o.order_date)                               AS first_order_date,
            MAX(o.order_date)                               AS last_order_date,
            COUNT(DISTINCT o.id)                            AS total_orders,
            SUM(oi.quantity)                                AS total_items,
            ROUND(SUM(oi.line_revenue), 2)                  AS total_spent,
            ROUND(SUM(oi.line_revenue)/COUNT(DISTINCT o.id),2) AS avg_order_value,
            CASE WHEN COUNT(DISTINCT o.id) > 1
                 THEN 'Returning' ELSE 'New' END            AS customer_type
        FROM customers cu
        JOIN orders o       ON o.customer_id = cu.id
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status NOT IN ('returned','cancelled')
        {df}
        GROUP BY cu.id, cu.first_name, cu.last_name, cu.email, cu.segment, cu.region, cu.state
        ORDER BY total_spent DESC
        LIMIT :limit
    """)
    p = _params(start, end)
    p["limit"] = limit
    rows = db.execute(sql, p).mappings().all()
    return [
        {**dict(r),
         "first_order_date": str(r["first_order_date"]) if r["first_order_date"] else None,
         "last_order_date":  str(r["last_order_date"])  if r["last_order_date"]  else None}
        for r in rows
    ]


def get_new_vs_returning(db: Session, start: Optional[date], end: Optional[date]) -> list:
    df  = _date_filter(start, end)
    sql = text(f"""
        SELECT
            CASE WHEN order_count > 1 THEN 'Returning' ELSE 'New' END AS customer_type,
            COUNT(*) AS count
        FROM (
            SELECT customer_id, COUNT(id) AS order_count
            FROM orders o
            WHERE o.status NOT IN ('returned','cancelled')
            {df}
            GROUP BY customer_id
        ) t
        GROUP BY customer_type
    """)
    rows = db.execute(sql, _params(start, end)).mappings().all()
    total = sum(r["count"] for r in rows)
    return [
        {"customer_type": r["customer_type"],
         "count": r["count"],
         "pct": round(r["count"] / total * 100, 2) if total else 0}
        for r in rows
    ]


def get_purchase_frequency(db: Session, start: Optional[date], end: Optional[date]) -> list:
    df  = _date_filter(start, end)
    sql = text(f"""
        SELECT order_count, COUNT(*) AS customers
        FROM (
            SELECT customer_id, COUNT(id) AS order_count
            FROM orders o
            WHERE o.status NOT IN ('returned','cancelled')
            {df}
            GROUP BY customer_id
        ) t
        GROUP BY order_count
        ORDER BY order_count
    """)
    rows = db.execute(sql, _params(start, end)).mappings().all()
    return [dict(r) for r in rows]


# ── Geography ──────────────────────────────────────────────────────────────────

def get_regional_sales(db: Session, start: Optional[date], end: Optional[date]) -> list:
    df  = _date_filter(start, end)
    sql = text(f"""
        SELECT
            o.shipping_region                           AS region,
            o.shipping_state                            AS state,
            COUNT(DISTINCT o.id)                        AS total_orders,
            COUNT(DISTINCT o.customer_id)               AS unique_customers,
            ROUND(SUM(oi.line_revenue), 2)              AS revenue,
            ROUND(SUM(oi.line_profit),  2)              AS profit,
            ROUND(SUM(oi.line_profit) /
                  NULLIF(SUM(oi.line_revenue), 0) * 100, 2) AS profit_margin_pct
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.status NOT IN ('returned','cancelled')
        {df}
        GROUP BY o.shipping_region, o.shipping_state
        ORDER BY revenue DESC
    """)
    rows = db.execute(sql, _params(start, end)).mappings().all()
    return [dict(r) for r in rows]
