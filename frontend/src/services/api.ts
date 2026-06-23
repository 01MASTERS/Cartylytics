// Cartlytics – API Service Layer
// All backend calls live here for clean separation.

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export interface DateRange {
  startDate?: string;
  endDate?: string;
}

function buildQuery(params: Record<string, string | number | undefined>): string {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== "")
    .map(([k, v]) => `${k}=${encodeURIComponent(v!)}`)
    .join("&");
  return qs ? `?${qs}` : "";
}

async function get<T>(path: string, params: Record<string, any> = {}): Promise<T> {
  const url = `${BASE_URL}${path}${buildQuery(params)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`API error ${res.status} – ${path}`);
  return res.json();
}

// ── Types ─────────────────────────────────────────────────────────────────────

export interface KPIs {
  total_revenue:        number;
  total_profit:         number;
  total_orders:         number;
  avg_order_value:      number;
  total_customers:      number;
  revenue_growth_pct:   number | null;
  profit_growth_pct:    number | null;
  repeat_customer_rate: number;
}

export interface MonthlySalesRow {
  month:             string;
  year:              number;
  month_num:         number;
  total_orders:      number;
  unique_customers:  number;
  revenue:           number;
  cost:              number;
  profit:            number;
  profit_margin_pct: number;
}

export interface CategorySalesRow {
  category_id:       number;
  category_name:     string;
  total_orders:      number;
  units_sold:        number;
  revenue:           number;
  cost:              number;
  profit:            number;
  profit_margin_pct: number;
}

export interface ProductRow {
  product_id:        number;
  sku:               string;
  product_name:      string;
  category_name:     string;
  brand:             string;
  total_orders:      number;
  units_sold:        number;
  revenue:           number;
  profit:            number;
  profit_margin_pct: number;
}

export interface CustomerRow {
  customer_id:      number;
  customer_name:    string;
  email:            string;
  segment:          string;
  region:           string;
  state:            string;
  first_order_date: string;
  last_order_date:  string;
  total_orders:     number;
  total_items:      number;
  total_spent:      number;
  avg_order_value:  number;
  customer_type:    string;
}

export interface NewVsReturningRow {
  customer_type: string;
  count:         number;
  pct:           number;
}

export interface PurchaseFrequencyRow {
  order_count: number;
  customers:   number;
}

export interface RegionalSalesRow {
  region:            string;
  state:             string;
  total_orders:      number;
  unique_customers:  number;
  revenue:           number;
  profit:            number;
  profit_margin_pct: number;
}

// ── API calls ─────────────────────────────────────────────────────────────────

export const api = {
  kpis: (range: DateRange) =>
    get<KPIs>("/kpis", { start_date: range.startDate, end_date: range.endDate }),

  monthlySales: (range: DateRange) =>
    get<MonthlySalesRow[]>("/sales/monthly", { start_date: range.startDate, end_date: range.endDate }),

  categorySales: (range: DateRange) =>
    get<CategorySalesRow[]>("/sales/categories", { start_date: range.startDate, end_date: range.endDate }),

  topProductsByRevenue: (range: DateRange, categoryId?: number) =>
    get<ProductRow[]>("/products/top-revenue", {
      start_date: range.startDate, end_date: range.endDate,
      category_id: categoryId, limit: 10,
    }),

  topProductsByProfit: (range: DateRange, categoryId?: number) =>
    get<ProductRow[]>("/products/top-profit", {
      start_date: range.startDate, end_date: range.endDate,
      category_id: categoryId, limit: 10,
    }),

  topCustomers: (range: DateRange) =>
    get<CustomerRow[]>("/customers/top-spenders", {
      start_date: range.startDate, end_date: range.endDate, limit: 20,
    }),

  newVsReturning: (range: DateRange) =>
    get<NewVsReturningRow[]>("/customers/new-vs-returning", {
      start_date: range.startDate, end_date: range.endDate,
    }),

  purchaseFrequency: (range: DateRange) =>
    get<PurchaseFrequencyRow[]>("/customers/purchase-frequency", {
      start_date: range.startDate, end_date: range.endDate,
    }),

  regionalSales: (range: DateRange) =>
    get<RegionalSalesRow[]>("/geography/regions", {
      start_date: range.startDate, end_date: range.endDate,
    }),
};
