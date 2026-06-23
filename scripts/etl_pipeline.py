"""
Cartlytics – ETL Pipeline
Loads raw CSVs → cleans → validates → inserts into MySQL.
Run: python scripts/etl_pipeline.py
"""

import os
import sys
import logging
from datetime import datetime

import pandas as pd
import numpy as np
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("etl")

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets", "raw")


# ── DB connection ──────────────────────────────────────────────────────────────

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "cartlytics"),
        charset="utf8mb4",
        autocommit=False,
        auth_plugin="mysql_native_password",
    )


# ── helpers ────────────────────────────────────────────────────────────────────

def read_csv(name: str) -> pd.DataFrame:
    path = os.path.join(RAW_DIR, f"{name}.csv")
    df = pd.read_csv(path, keep_default_na=True, encoding_errors='replace')
    log.info("  Loaded %-20s  %d rows, %d cols", name + ".csv", len(df), len(df.columns))
    return df


def coerce_datetime(series: pd.Series, col_name: str) -> pd.Series:
    """Parse datetimes; fill NaT with None for MySQL."""
    parsed = pd.to_datetime(series, errors="coerce")
    bad = parsed.isna() & series.notna() & (series != "")
    if bad.any():
        log.warning("  '%s': %d unparseable date values replaced with NULL", col_name, bad.sum())
    return parsed


def clean_str(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip()


def none_if_nan(val):
    """Convert NaN / NaT / empty string to Python None for MySQL."""
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, pd._libs.tslibs.nattype.NaTType):
        return None
    if isinstance(val, str) and val.strip() == "":
        return None
    if isinstance(val, pd.Timestamp):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    return val


def to_mysql_row(row_dict: dict) -> dict:
    return {k: none_if_nan(v) for k, v in row_dict.items()}


def bulk_insert(cursor, table: str, cols: list, rows: list, batch=500):
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
    for i in range(0, len(rows), batch):
        chunk = rows[i : i + batch]
        cursor.executemany(sql, chunk)
    log.info("  ✓ Inserted %d rows into `%s`", len(rows), table)


# ── clean & load categories ────────────────────────────────────────────────────

def load_categories(conn):
    df = read_csv("categories")

    # deduplicate
    before = len(df)
    df = df.drop_duplicates(subset=["id"])
    if len(df) < before:
        log.warning("  Dropped %d duplicate category rows", before - len(df))

    df["name"]      = clean_str(df["name"])
    df["slug"]      = clean_str(df["slug"])
    df["is_active"] = df["is_active"].fillna(1).astype(int)

    cols = ["id", "name", "slug", "description", "parent_id", "is_active"]
    rows = [tuple(none_if_nan(r[c]) for c in cols) for _, r in df.iterrows()]

    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE categories")
    bulk_insert(cur, "categories", cols, rows)
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cur.close()


# ── clean & load products ──────────────────────────────────────────────────────

def load_products(conn):
    df = read_csv("products")

    before = len(df)
    df = df.drop_duplicates(subset=["sku"])
    if len(df) < before:
        log.warning("  Dropped %d duplicate product SKUs", before - len(df))

    df["name"]          = clean_str(df["name"])
    df["brand"]         = clean_str(df["brand"])
    df["cost_price"]    = pd.to_numeric(df["cost_price"],    errors="coerce").fillna(0)
    df["selling_price"] = pd.to_numeric(df["selling_price"], errors="coerce").fillna(0)
    df["stock_qty"]     = pd.to_numeric(df["stock_qty"],     errors="coerce").fillna(0).astype(int)
    df["is_active"]     = df["is_active"].fillna(1).astype(int)

    # sanity: cost should not exceed selling price
    bad = df["cost_price"] > df["selling_price"]
    if bad.any():
        log.warning("  %d products have cost > price – clamping cost to price * 0.6", bad.sum())
        df.loc[bad, "cost_price"] = (df.loc[bad, "selling_price"] * 0.6).round(2)

    cols = ["id", "sku", "name", "description", "category_id",
            "cost_price", "selling_price", "stock_qty", "brand", "is_active"]
    rows = [tuple(none_if_nan(r[c]) for c in cols) for _, r in df.iterrows()]

    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE products")
    bulk_insert(cur, "products", cols, rows)
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cur.close()


# ── clean & load customers ─────────────────────────────────────────────────────

def load_customers(conn):
    df = read_csv("customers")

    before = len(df)
    df = df.drop_duplicates(subset=["email"])
    if len(df) < before:
        log.warning("  Dropped %d duplicate customer emails", before - len(df))

    df["email"]      = df["email"].str.strip().str.lower()
    df["first_name"] = clean_str(df["first_name"])
    df["last_name"]  = clean_str(df["last_name"])
    df["phone"]      = clean_str(df["phone"]).str.slice(0, 20)

    # valid genders
    valid_genders = {"Male", "Female", "Other", "Unknown"}
    df["gender"] = df["gender"].where(df["gender"].isin(valid_genders), "Unknown")

    df["date_of_birth"] = coerce_datetime(df["date_of_birth"], "date_of_birth")
    df["created_at"]    = coerce_datetime(df["created_at"],    "created_at")
    df["created_at"]    = df["created_at"].fillna(datetime.now())

    valid_regions = {"North","South","East","West","Northeast","Northwest",
                     "Southeast","Southwest","Central"}
    df["region"] = df["region"].where(df["region"].isin(valid_regions), "Central")

    valid_segs = {"Consumer","Corporate","Home Office","Small Business"}
    df["segment"] = df["segment"].where(df["segment"].isin(valid_segs), "Consumer")

    df["is_active"] = df["is_active"].fillna(1).astype(int)

    cols = ["id","email","first_name","last_name","phone","gender",
            "date_of_birth","city","state","region","country",
            "zip_code","segment","is_active","created_at"]
    rows = [tuple(none_if_nan(r[c]) for c in cols) for _, r in df.iterrows()]

    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE customers")
    bulk_insert(cur, "customers", cols, rows)
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cur.close()


# ── clean & load orders ────────────────────────────────────────────────────────

def load_orders(conn):
    df = read_csv("orders")

    before = len(df)
    df = df.drop_duplicates(subset=["order_number"])
    if len(df) < before:
        log.warning("  Dropped %d duplicate order numbers", before - len(df))

    date_cols = ["order_date", "shipped_date", "delivered_date"]
    for c in date_cols:
        df[c] = coerce_datetime(df[c], c)

    numeric_cols = ["discount_pct", "shipping_fee", "subtotal", "discount_amount", "total_amount"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # clamp discount 0–100
    df["discount_pct"] = df["discount_pct"].clip(0, 100)

    valid_statuses = {"pending","confirmed","shipped","delivered","returned","cancelled"}
    df["status"] = df["status"].where(df["status"].isin(valid_statuses), "pending")

    valid_pay = {"Credit Card","Debit Card","PayPal","Bank Transfer","Cash on Delivery"}
    df["payment_method"] = df["payment_method"].where(df["payment_method"].isin(valid_pay), "Credit Card")

    cols = ["id","order_number","customer_id","status","order_date",
            "shipped_date","delivered_date","shipping_city","shipping_state",
            "shipping_region","shipping_country","shipping_zip",
            "payment_method","discount_pct","shipping_fee",
            "subtotal","discount_amount","total_amount"]
    rows = [tuple(none_if_nan(r[c]) for c in cols) for _, r in df.iterrows()]

    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE orders")
    bulk_insert(cur, "orders", cols, rows)
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cur.close()


# ── clean & load order_items ───────────────────────────────────────────────────

def load_order_items(conn):
    df = read_csv("order_items")

    before = len(df)
    df = df.drop_duplicates(subset=["id"])
    if len(df) < before:
        log.warning("  Dropped %d duplicate order_item rows", before - len(df))

    numeric_cols = ["quantity","unit_price","unit_cost","discount_pct",
                    "line_revenue","line_cost","line_profit"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    df["quantity"] = df["quantity"].clip(lower=1).astype(int)

    # recalculate derived metrics to ensure consistency
    df["line_revenue"] = (
        df["quantity"] * df["unit_price"] * (1 - df["discount_pct"] / 100)
    ).round(2)
    df["line_cost"]    = (df["quantity"] * df["unit_cost"]).round(2)
    df["line_profit"]  = (df["line_revenue"] - df["line_cost"]).round(2)

    cols = ["id","order_id","product_id","quantity","unit_price","unit_cost",
            "discount_pct","line_revenue","line_cost","line_profit"]
    rows = [tuple(none_if_nan(r[c]) for c in cols) for _, r in df.iterrows()]

    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE order_items")
    bulk_insert(cur, "order_items", cols, rows)
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cur.close()


# ── post-load stats ────────────────────────────────────────────────────────────

def print_summary(conn):
    cur = conn.cursor()
    tables = ["categories", "products", "customers", "orders", "order_items"]
    log.info("── Final row counts ──────────────────────────────")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        (cnt,) = cur.fetchone()
        log.info("  %-20s %d", t, cnt)
    cur.close()


# ── main ───────────────────────────────────────────────────────────────────────

def run():
    log.info("╔══════════════════════════════════════════════╗")
    log.info("║     Cartlytics ETL Pipeline  v1.0            ║")
    log.info("╚══════════════════════════════════════════════╝")

    try:
        conn = get_connection()
        log.info("Connected to MySQL: %s/%s", os.getenv("DB_HOST"), os.getenv("DB_NAME"))
    except Exception as e:
        log.error("DB connection failed: %s", e)
        sys.exit(1)

    steps = [
        ("Categories",   load_categories),
        ("Products",     load_products),
        ("Customers",    load_customers),
        ("Orders",       load_orders),
        ("Order Items",  load_order_items),
    ]

    for label, fn in steps:
        log.info("── %s ──", label)
        try:
            fn(conn)
        except Exception as e:
            log.error("  FAILED: %s", e)
            conn.rollback()
            conn.close()
            sys.exit(1)

    print_summary(conn)
    conn.close()
    log.info("ETL complete ✓")


if __name__ == "__main__":
    run()
