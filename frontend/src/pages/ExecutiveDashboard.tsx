import React from "react";
import {
  AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import { KpiCard, ChartCard, ChartTooltip } from "../components/ui";
import { useAsync } from "../hooks/useAsync";
import { api } from "../services/api";
import type { DateRange } from "../types";
import { fmt$, fmtNum, fmtMonth } from "../utils/format";

interface Props { range: DateRange; }

const COLORS = ["#3b82f6", "#22c55e", "#a855f7", "#f59e0b", "#06b6d4"];

export const ExecutiveDashboard: React.FC<Props> = ({ range }) => {
  const { data: kpis,       loading: kL } = useAsync(() => api.kpis(range),          [range]);
  const { data: monthly,    loading: mL } = useAsync(() => api.monthlySales(range),  [range]);
  const { data: categories, loading: cL } = useAsync(() => api.categorySales(range), [range]);

  const chartData = (monthly ?? []).map(r => ({
    name: fmtMonth(r.month),
    Revenue: r.revenue,
    Profit:  r.profit,
  }));

  const catData = (categories ?? []).map(c => ({
    name:    c.category_name.replace(" & ", " & "),
    Revenue: c.revenue,
    Profit:  c.profit,
  }));

  const grid = { display: "grid", gap: 14 } as const;

  return (
    <div>
      {/* KPI row */}
      <div style={{ ...grid, gridTemplateColumns: "repeat(auto-fill, minmax(200px,1fr))", marginBottom: 24 }}>
        <KpiCard label="Total Revenue"     value={kpis ? fmt$(kpis.total_revenue, true) : "—"} growth={kpis?.revenue_growth_pct}   accent="blue"   loading={kL} />
        <KpiCard label="Total Profit"      value={kpis ? fmt$(kpis.total_profit,  true) : "—"} growth={kpis?.profit_growth_pct}    accent="green"  loading={kL} />
        <KpiCard label="Total Orders"      value={kpis ? fmtNum(kpis.total_orders)      : "—"} sub="Excl. returns & cancellations" accent="purple" loading={kL} />
        <KpiCard label="Avg Order Value"   value={kpis ? fmt$(kpis.avg_order_value)     : "—"} sub="Per completed order"           accent="amber"  loading={kL} />
        <KpiCard label="Total Customers"   value={kpis ? fmtNum(kpis.total_customers)   : "—"} sub={kpis ? `${kpis.repeat_customer_rate}% repeat rate` : undefined} accent="cyan" loading={kL} />
      </div>

      {/* Area chart */}
      <ChartCard title="Monthly Revenue & Profit" sub="Completed orders · area trend" badge="Trend" style={{ marginBottom: 14 }}>
        {mL
          ? <div style={{ height: 220, background: "var(--bg-card2)", borderRadius: 6, animation: "shimmer 1.4s infinite" }} />
          : (
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={chartData} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
                <defs>
                  <linearGradient id="gRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#3b82f6" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gPro" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#22c55e" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e2d45" />
                <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 10 }} tickLine={false} axisLine={false} interval={2} />
                <YAxis tick={{ fill: "#64748b", fontSize: 10 }} tickLine={false} axisLine={false} tickFormatter={v => fmt$(v, true)} width={55} />
                <Tooltip content={<ChartTooltip prefix="$" />} />
                <Legend wrapperStyle={{ fontSize: 12, color: "#94a3b8" }} />
                <Area type="monotone" dataKey="Revenue" stroke="#3b82f6" fill="url(#gRev)" strokeWidth={2} dot={false} />
                <Area type="monotone" dataKey="Profit"  stroke="#22c55e" fill="url(#gPro)" strokeWidth={2} dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          )
        }
      </ChartCard>

      {/* Category bar charts */}
      <div style={{ ...grid, gridTemplateColumns: "1fr 1fr" }}>
        <ChartCard title="Revenue by Category">
          {cL
            ? <div style={{ height: 200, background: "var(--bg-card2)", borderRadius: 6 }} />
            : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={catData} layout="vertical" margin={{ top: 0, right: 20, bottom: 0, left: 0 }}>
                  <XAxis type="number" tick={{ fill: "#64748b", fontSize: 10 }} tickFormatter={v => fmt$(v, true)} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="name" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} width={115} />
                  <Tooltip content={<ChartTooltip prefix="$" />} cursor={{ fill: "transparent" }} />
                  <Bar dataKey="Revenue" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </ChartCard>

        <ChartCard title="Profit by Category">
          {cL
            ? <div style={{ height: 200, background: "var(--bg-card2)", borderRadius: 6 }} />
            : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={catData} layout="vertical" margin={{ top: 0, right: 20, bottom: 0, left: 0 }}>
                  <XAxis type="number" tick={{ fill: "#64748b", fontSize: 10 }} tickFormatter={v => fmt$(v, true)} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="name" tick={{ fill: "#94a3b8", fontSize: 11 }} axisLine={false} tickLine={false} width={115} />
                  <Tooltip content={<ChartTooltip prefix="$" />} cursor={{ fill: "transparent" }} />
                  <Bar dataKey="Profit" fill="#22c55e" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </ChartCard>
      </div>
    </div>
  );
};
