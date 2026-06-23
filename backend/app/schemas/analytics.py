from pydantic import BaseModel
from typing import Optional, List
from datetime import date


# ── shared ─────────────────────────────────────────────────────────────────────

class DateRangeParams(BaseModel):
    start_date: Optional[date] = None
    end_date:   Optional[date] = None
    category_id: Optional[int] = None


# ── KPIs ───────────────────────────────────────────────────────────────────────

class KPIResponse(BaseModel):
    total_revenue:        float
    total_profit:         float
    total_orders:         int
    avg_order_value:      float
    total_customers:      int
    revenue_growth_pct:   Optional[float]
    profit_growth_pct:    Optional[float]
    repeat_customer_rate: float


# ── Sales ──────────────────────────────────────────────────────────────────────

class MonthlySalesRow(BaseModel):
    month:             str
    year:              int
    month_num:         int
    total_orders:      int
    unique_customers:  int
    revenue:           float
    cost:              float
    profit:            float
    profit_margin_pct: float


class CategorySalesRow(BaseModel):
    category_id:       int
    category_name:     str
    total_orders:      int
    units_sold:        int
    revenue:           float
    cost:              float
    profit:            float
    profit_margin_pct: float


# ── Products ───────────────────────────────────────────────────────────────────

class ProductPerformanceRow(BaseModel):
    product_id:        int
    sku:               str
    product_name:      str
    category_name:     str
    brand:             Optional[str]
    total_orders:      int
    units_sold:        int
    revenue:           float
    profit:            float
    profit_margin_pct: float


# ── Customers ──────────────────────────────────────────────────────────────────

class CustomerStatsRow(BaseModel):
    customer_id:       int
    customer_name:     str
    email:             str
    segment:           str
    region:            str
    state:             str
    first_order_date:  Optional[str]
    last_order_date:   Optional[str]
    total_orders:      int
    total_items:       int
    total_spent:       float
    avg_order_value:   float
    customer_type:     str


class NewVsReturningRow(BaseModel):
    customer_type: str
    count:         int
    pct:           float


class PurchaseFrequencyRow(BaseModel):
    order_count: int
    customers:   int


# ── Geography ──────────────────────────────────────────────────────────────────

class RegionalSalesRow(BaseModel):
    region:            str
    state:             str
    total_orders:      int
    unique_customers:  int
    revenue:           float
    profit:            float
    profit_margin_pct: float
