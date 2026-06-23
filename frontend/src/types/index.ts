export interface DateRange {
  startDate?: string;
  endDate?:   string;
}

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
