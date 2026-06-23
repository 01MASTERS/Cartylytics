import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { ChartCard, ChartTooltip, ProgressBar } from "../components/ui";
import { useAsync } from "../hooks/useAsync";
import { api } from "../services/api";
import type { DateRange } from "../types";
import { fmt$, fmtNum } from "../utils/format";

interface Props { range: DateRange; }

export const GeographyDashboard: React.FC<Props> = ({ range }) => {
  const { data: regions, loading } = useAsync(() => api.regionalSales(range), [range]);

  // Aggregate by region (multiple states per region)
  const regionMap = new Map<string, { revenue: number; profit: number; orders: number; customers: number; states: Set<string> }>();
  (regions ?? []).forEach(r => {
    const entry = regionMap.get(r.region) ?? { revenue: 0, profit: 0, orders: 0, customers: 0, states: new Set() };
    entry.revenue   += r.revenue;
    entry.profit    += r.profit;
    entry.orders    += r.total_orders;
    entry.customers += r.unique_customers;
    entry.states.add(r.state);
    regionMap.set(r.region, entry);
  });

  const aggregated = Array.from(regionMap.entries())
    .map(([region, d]) => ({
      region,
      revenue: d.revenue, profit: d.profit,
      total_orders: d.orders, unique_customers: d.customers,
      profit_margin_pct: d.revenue ? Math.round(d.profit / d.revenue * 1000) / 10 : 0,
      states: Array.from(d.states).sort().join(", "),
    }))
    .sort((a, b) => b.revenue - a.revenue);

  const maxRev = Math.max(...aggregated.map(r => r.revenue), 1);

  const barData = aggregated.map(r => ({ name: r.region, Revenue: r.revenue, Profit: r.profit }));

  return (
    <div>
      {/* Bar chart */}
      <ChartCard title="Revenue & Profit by Region" sub="Completed orders only" style={{ marginBottom: 14 }}>
        {loading
          ? <div style={{ height: 220, background: "var(--bg-card2)", borderRadius: 6 }} />
          : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={barData} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e2d45" vertical={false} />
                <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} tickFormatter={v => fmt$(v, true)} width={55} />
                <Tooltip content={<ChartTooltip prefix="$" />} cursor={{ fill: "transparent" }} />
                <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
                <Bar dataKey="Revenue" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Profit"  fill="#22c55e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )
        }
      </ChartCard>

      {/* Region tiles grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 12 }}>
        {loading
          ? Array.from({ length: 6 }).map((_, i) => (
            <div key={i} style={{ height: 140, background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: "var(--radius)" }} />
          ))
          : aggregated.map(r => (
            <div key={r.region} style={{
              background: "var(--bg-card)", border: "1px solid var(--border)",
              borderRadius: "var(--radius)", padding: "16px 18px",
            }}>
              <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 10, display: "flex", justifyContent: "space-between" }}>
                <span>{r.region}</span>
                <span style={{ fontSize: 10, color: "var(--text-muted)", fontWeight: 400, alignSelf: "center" }}>
                  {r.profit_margin_pct}% margin
                </span>
              </div>
              <ProgressBar value={r.revenue} max={maxRev} color="#3b82f6" />
              <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 5 }}>
                {([
                  ["Revenue",   fmt$(r.revenue, true)],
                  ["Profit",    fmt$(r.profit, true)],
                  ["Orders",    fmtNum(r.total_orders)],
                  ["Customers", fmtNum(r.unique_customers)],
                ] as [string, string][]).map(([label, value]) => (
                  <div key={label} style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ fontSize: 11, color: "var(--text-muted)" }}>{label}</span>
                    <span style={{ fontSize: 12, fontWeight: 600, fontFamily: "monospace" }}>{value}</span>
                  </div>
                ))}
              </div>
            </div>
          ))
        }
      </div>
    </div>
  );
};
