"""
Cartlytics – Synthetic Dataset Generator
Generates realistic e-commerce CSV data for development & demo.
Run: python scripts/generate_datasets.py
"""

import random
import csv
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("en_US")
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "datasets", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── constants ──────────────────────────────────────────────────────────────────

REGIONS = {
    "CA": "West", "OR": "West", "WA": "West", "NV": "West",
    "TX": "South", "FL": "South", "GA": "South", "NC": "South", "TN": "South",
    "NY": "Northeast", "PA": "Northeast", "MA": "Northeast", "NJ": "Northeast",
    "IL": "Central", "OH": "Central", "MI": "Central", "IN": "Central",
    "CO": "Northwest", "UT": "Northwest", "AZ": "Southwest", "NM": "Southwest",
    "VA": "Southeast", "SC": "Southeast", "AL": "Southeast",
    "MN": "North", "WI": "North", "IA": "North",
}
STATES = list(REGIONS.keys())

CATEGORIES = [
    (1, "Electronics",       None),
    (2, "Clothing",          None),
    (3, "Home & Garden",     None),
    (4, "Sports & Outdoors", None),
    (5, "Books",             None),
    (6, "Laptops",           1),
    (7, "Smartphones",       1),
    (8, "Accessories",       1),
    (9, "Men's Wear",        2),
    (10,"Women's Wear",      2),
]

PRODUCTS = [
    # (id, sku, name, category_id, cost, price, brand)
    (1,  "EL-LAP-001", "ProBook 15 Laptop",          6,  450.00, 899.99,  "TechPro"),
    (2,  "EL-LAP-002", "UltraSlim 13 Laptop",        6,  520.00, 1099.99, "NovaTech"),
    (3,  "EL-PHN-001", "Galaxy X12 Smartphone",      7,  180.00, 499.99,  "Samsung"),
    (4,  "EL-PHN-002", "iPhone 15 Pro",              7,  550.00, 1199.99, "Apple"),
    (5,  "EL-PHN-003", "Pixel 8 Pro",                7,  300.00, 699.99,  "Google"),
    (6,  "EL-ACC-001", "Noise-Cancelling Headphones",8,   45.00, 149.99,  "SoundWave"),
    (7,  "EL-ACC-002", "Wireless Charger 20W",       8,   12.00,  39.99,  "ChargeFast"),
    (8,  "CL-MEN-001", "Classic Chino Pants",        9,   18.00,  59.99,  "UrbanWear"),
    (9,  "CL-MEN-002", "Oxford Button Shirt",        9,   14.00,  49.99,  "UrbanWear"),
    (10, "CL-WOM-001", "Floral Wrap Dress",          10,  16.00,  54.99,  "Blossom"),
    (11, "CL-WOM-002", "Slim Fit Jeans",             10,  20.00,  64.99,  "DenimCo"),
    (12, "HG-001",     "Cordless Drill Set",         3,   55.00, 129.99,  "BuildRight"),
    (13, "HG-002",     "Ceramic Plant Pots (Set 3)", 3,    8.00,  29.99,  "GreenHome"),
    (14, "HG-003",     "Smart Air Purifier",         3,   85.00, 199.99,  "AirPure"),
    (15, "SO-001",     "Yoga Mat Premium",           4,   12.00,  44.99,  "FlexFit"),
    (16, "SO-002",     "Running Shoes Pro",          4,   45.00, 119.99,  "SpeedRun"),
    (17, "SO-003",     "Resistance Bands Set",       4,    8.00,  24.99,  "FlexFit"),
    (18, "BK-001",     "Python for Data Science",   5,   15.00,  39.99,  "TechBooks"),
    (19, "BK-002",     "The Lean Startup",           5,    9.00,  19.99,  "BizPress"),
    (20, "BK-003",     "Atomic Habits",             5,    8.00,  17.99,  "LifeBooks"),
]

SEGMENTS  = ["Consumer", "Corporate", "Home Office", "Small Business"]
GENDERS   = ["Male", "Female", "Other", "Unknown"]
PAY_METHS = ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]
STATUSES  = ["delivered", "delivered", "delivered", "shipped", "returned", "cancelled"]

# ── helpers ────────────────────────────────────────────────────────────────────

def rand_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

# ── generate categories ────────────────────────────────────────────────────────

def gen_categories():
    path = os.path.join(OUTPUT_DIR, "categories.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","name","slug","description","parent_id","is_active"])
        for cid, name, parent in CATEGORIES:
            slug = name.lower().replace(" ", "-").replace("&", "and").replace("'", "")
            w.writerow([cid, name, slug, f"Products in {name} category",
                        parent if parent else "", 1])
    print(f"  ✓ categories.csv  ({len(CATEGORIES)} rows)")

# ── generate products ──────────────────────────────────────────────────────────

def gen_products():
    path = os.path.join(OUTPUT_DIR, "products.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","sku","name","description","category_id",
                    "cost_price","selling_price","stock_qty","brand","is_active"])
        for row in PRODUCTS:
            pid, sku, name, cat, cost, price, brand = row
            w.writerow([pid, sku, name, f"{name} – premium quality product.",
                        cat, cost, price, random.randint(20, 500), brand, 1])
    print(f"  ✓ products.csv    ({len(PRODUCTS)} rows)")

# ── generate customers ─────────────────────────────────────────────────────────

def gen_customers(n=500):
    path = os.path.join(OUTPUT_DIR, "customers.csv")
    start = datetime(2020, 1, 1)
    end   = datetime(2024, 12, 31)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id","email","first_name","last_name","phone","gender",
                    "date_of_birth","city","state","region","country",
                    "zip_code","segment","is_active","created_at"])
        emails = set()
        i = 1
        while i <= n:
            email = fake.email()
            if email in emails:
                continue
            emails.add(email)
            state  = random.choice(STATES)
            region = REGIONS[state]
            dob    = fake.date_of_birth(minimum_age=18, maximum_age=70)
            gender = random.choices(GENDERS, weights=[45, 45, 5, 5])[0]
            seg    = random.choices(SEGMENTS, weights=[60, 20, 10, 10])[0]
            created = rand_date(start, end)
            # ~5% missing phone
            phone = fake.phone_number() if random.random() > 0.05 else ""
            w.writerow([i, email, fake.first_name(), fake.last_name(),
                        phone, gender, dob, fake.city(), state, region,
                        "United States", fake.zipcode(), seg, 1,
                        created.strftime("%Y-%m-%d %H:%M:%S")])
            i += 1
    print(f"  ✓ customers.csv   ({n} rows)")
    return n

# ── generate orders + order_items ─────────────────────────────────────────────

def gen_orders(n_customers=500, n_orders=3000):
    orders_path = os.path.join(OUTPUT_DIR, "orders.csv")
    items_path  = os.path.join(OUTPUT_DIR, "order_items.csv")
    start = datetime(2022, 1, 1)
    end   = datetime(2024, 12, 31)

    prod_map = {p[0]: p for p in PRODUCTS}

    with open(orders_path, "w", newline="") as of, \
         open(items_path,  "w", newline="") as itf:

        ow = csv.writer(of)
        iw = csv.writer(itf)

        ow.writerow(["id","order_number","customer_id","status","order_date",
                     "shipped_date","delivered_date","shipping_city","shipping_state",
                     "shipping_region","shipping_country","shipping_zip",
                     "payment_method","discount_pct","shipping_fee",
                     "subtotal","discount_amount","total_amount"])
        iw.writerow(["id","order_id","product_id","quantity","unit_price",
                     "unit_cost","discount_pct","line_revenue","line_cost","line_profit"])

        # weight customers so some are repeat buyers
        cust_weights = []
        for c in range(1, n_customers + 1):
            if c <= 50:      cust_weights.append(8)   # top 50 = heavy buyers
            elif c <= 150:   cust_weights.append(4)
            else:            cust_weights.append(1)

        item_id = 1
        for oid in range(1, n_orders + 1):
            cid     = random.choices(range(1, n_customers + 1), weights=cust_weights)[0]
            state   = random.choice(STATES)
            region  = REGIONS[state]
            status  = random.choices(STATUSES, weights=[70, 70, 70, 15, 10, 5])[0]
            odate   = rand_date(start, end)
            shipped = odate + timedelta(days=random.randint(1, 3)) if status in ("shipped","delivered","returned") else ""
            deliv   = shipped + timedelta(days=random.randint(2, 7)) if status in ("delivered","returned") and shipped else ""

            discount_pct = random.choices([0, 5, 10, 15, 20], weights=[50, 20, 15, 10, 5])[0]
            shipping_fee = round(random.choices([0, 4.99, 7.99, 9.99], weights=[30, 30, 25, 15])[0], 2)
            pay_method   = random.choice(PAY_METHS)

            # 1–4 items per order
            n_items  = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
            prod_ids = random.sample([p[0] for p in PRODUCTS], min(n_items, len(PRODUCTS)))

            subtotal = 0.0
            rows_buf = []
            for pid in prod_ids:
                _, _, _, _, cost, price, _ = prod_map[pid]
                qty     = random.randint(1, 3)
                item_disc = discount_pct
                rev     = round(qty * price * (1 - item_disc / 100), 2)
                cst     = round(qty * cost, 2)
                profit  = round(rev - cst, 2)
                subtotal += round(qty * price, 2)
                rows_buf.append([item_id, oid, pid, qty, price, cost,
                                 item_disc, rev, cst, profit])
                item_id += 1

            discount_amount = round(subtotal * discount_pct / 100, 2)
            total_amount    = round(subtotal - discount_amount + shipping_fee, 2)

            order_num = f"ORD-{odate.year}-{oid:06d}"
            ow.writerow([oid, order_num, cid, status,
                         odate.strftime("%Y-%m-%d %H:%M:%S"),
                         shipped.strftime("%Y-%m-%d %H:%M:%S") if shipped else "",
                         deliv.strftime("%Y-%m-%d %H:%M:%S")   if deliv   else "",
                         fake.city(), state, region, "United States", fake.zipcode(),
                         pay_method, discount_pct, shipping_fee,
                         round(subtotal, 2), discount_amount, total_amount])

            for r in rows_buf:
                iw.writerow(r)

    print(f"  ✓ orders.csv      ({n_orders} rows)")
    print(f"  ✓ order_items.csv (~{item_id-1} rows)")


if __name__ == "__main__":
    print("Generating Cartlytics synthetic datasets …")
    gen_categories()
    gen_products()
    n = gen_customers(500)
    gen_orders(n, 3000)
    print("Done. Files saved to datasets/raw/")
