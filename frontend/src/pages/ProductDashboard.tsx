import React, { useState, useMemo } from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { ChartCard, TabBar, Badge, ProgressBar, ChartTooltip } from "../components/ui";
import { useAsync } from "../hooks/useAsync";
import { api } from "../services/api";
import type { DateRange, ProductRow, CategorySalesRow } from "../types";
import { fmt$, fmtNum } from "../utils/format";

interface Props { range: DateRange; }

const COLORS = ["#3b82f6", "#22c55e", "#a855f7", "#f59e0b", "#06b6d4", "#ef4444", "#f97316", "#8b5cf6"];

const RANK_COLORS = ["#fbbf24", "#9ca3af", "#b45309"];

export const ProductDashboard: React.FC<Props> = ({ range }) => {
  const [tab,    setTab]    = useState("Revenue");
  const [search, setSearch] = useState("");

  const { data: byRevenue, loading: rL } = useAsync(() => api.topProductsByRevenue(range), [range]);
  const { data: byProfit,  loading: pL } = useAsync(() => api.topProductsByProfit(range),  [range]);
  const { data: categories }             = useAsync(() => api.categorySales(range),         [range]);

  const products = tab === "Revenue" ? (byRevenue ?? []) : (byProfit ?? []);
  const loading  = tab === "Revenue" ? rL : pL;

  const filtered = useMemo(() =>
    products.filter((p: ProductRow) =>
      p.product_name.toLowerCase().includes(search.toLowerCase()) ||
      p.category_name.toLowerCase().includes(search.toLowerCase()) ||
      p.brand?.toLowerCase().includes(search.toLowerCase())
    ), [products, search]);

  const maxVal = Math.max(...filtered.map((p: ProductRow) => tab === "Revenue" ? p.revenue : p.profit), 1);

  const pieData = (categories ?? []).map((c: CategorySalesRow) => ({ name: c.category_name, value: c.revenue }));

  const segBadge = (seg: string): "blue" | "green" | "amber" | "purple" =>
    ({ Electronics: "blue", Clothing: "green", "Home & Garden": "amber", "Sports & Outdoors": "purple" }[seg] ?? "blue") as any;

  return (
    <div>
      <div className="dash-controls">
        <TabBar tabs={["Revenue", "Profit"]} active={tab} onChange={setTab} />
        <input
          placeholder="Search products…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{
            background: "var(--bg)", border: "1px solid var(--border-2)", color: "var(--text)",
            borderRadius: 6, padding: "6px 10px 6px 10px", fontSize: 12, outline: "none", width: 180,
          }}
        />
      </div>

      <div className="chart-grid-2-1">
        {/* Table */}
        <ChartCard title={`Top 10 Products by ${tab}`} sub="Filtered by date range & category">
          <div className="table-wrapper">
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
              <thead>
                <tr>
                  {["#", "Product", "Category", "Units", tab === "Revenue" ? "Revenue" : "Profit", "Margin %", "Share"].map(h => (
                    <th key={h} style={{
                      textAlign: "left", padding: "8px 10px", color: "var(--text-muted)",
                      fontWeight: 600, fontSize: 11, letterSpacing: "0.4px", textTransform: "uppercase",
                      borderBottom: "1px solid var(--border)", whiteSpace: "nowrap",
                    }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {loading
                  ? Array.from({ length: 8 }).map((_, i: number) => (
                    <tr key={i}><td colSpan={7} style={{ padding: "10px" }}>
                      <div style={{ height: 16, background: "var(--bg-card2)", borderRadius: 4 }} />
                    </td></tr>
                  ))
                  : filtered.map((p: ProductRow, i: number) => {
                    const val = tab === "Revenue" ? p.revenue : p.profit;
                    return (
                      <tr key={p.product_id}>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                          <span style={{ fontFamily: "monospace", fontSize: 11, color: RANK_COLORS[i] ?? "var(--text-muted)" }}>
                            #{i + 1}
                          </span>
                        </td>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                          <div style={{ color: "var(--text)", fontWeight: 500, maxWidth: 160, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                            {p.product_name}
                          </div>
                          <div style={{ fontSize: 10, color: "var(--text-muted)", fontFamily: "monospace" }}>{p.sku}</div>
                        </td>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                          <Badge variant={segBadge(p.category_name)}>{p.category_name}</Badge>
                        </td>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", fontFamily: "monospace", color: "var(--text-dim)" }}>
                          {fmtNum(p.units_sold)}
                        </td>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", fontFamily: "monospace", color: "var(--green)" }}>
                          {fmt$(val, true)}
                        </td>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", fontFamily: "monospace", color: "var(--text-dim)" }}>
                          {p.profit_margin_pct.toFixed(1)}%
                        </td>
                        <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", width: 80 }}>
                          <ProgressBar value={val} max={maxVal} color={tab === "Revenue" ? "#3b82f6" : "#22c55e"} />
                        </td>
                      </tr>
                    );
                  })
                }
              </tbody>
            </table>
          </div>
        </ChartCard>

        {/* Donut */}
        <ChartCard title="Category Revenue Mix" sub="Share of total revenue">
          <ResponsiveContainer width="100%" height={190}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={52} outerRadius={78} dataKey="value" stroke="none">
                {pieData.map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip formatter={(v: number) => [fmt$(v, true), "Revenue"]} />
            </PieChart>
          </ResponsiveContainer>
          <div className="pie-legend">
            {pieData.map((d: { name: string, value: number }, i: number) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12, color: "var(--text-dim)" }}>
                <div style={{ width: 8, height: 8, borderRadius: "50%", background: COLORS[i % COLORS.length], flexShrink: 0 }} />
                <span style={{ flex: 1, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{d.name}</span>
                <span style={{ fontFamily: "monospace", color: "var(--text)" }}>{fmt$(d.value, true)}</span>
              </div>
            ))}
          </div>
        </ChartCard>
      </div>
    </div>
  );
};
