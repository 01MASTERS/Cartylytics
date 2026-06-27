import React, { useState, useMemo } from "react";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { ChartCard, Badge, ChartTooltip } from "../components/ui";
import { useAsync } from "../hooks/useAsync";
import { api } from "../services/api";
import type { DateRange } from "../types";
import { fmt$, fmtNum } from "../utils/format";

interface Props { range: DateRange; }

const RANK_COLORS = ["#fbbf24", "#9ca3af", "#b45309"];

export const CustomerDashboard: React.FC<Props> = ({ range }) => {
  const [search, setSearch] = useState("");

  const { data: customers, loading: cL } = useAsync(() => api.topCustomers(range),      [range]);
  const { data: nvr,       loading: nL } = useAsync(() => api.newVsReturning(range),    [range]);
  const { data: freq,      loading: fL } = useAsync(() => api.purchaseFrequency(range), [range]);

  const filtered = useMemo(() =>
    (customers ?? []).filter(c =>
      c.customer_name.toLowerCase().includes(search.toLowerCase()) ||
      c.segment.toLowerCase().includes(search.toLowerCase()) ||
      c.region.toLowerCase().includes(search.toLowerCase())
    ), [customers, search]);

  const nvrColors = ["#3b82f6", "#22c55e"];
  const segBadge = (s: string): "blue" | "green" | "amber" | "purple" =>
    ({ Consumer: "blue", Corporate: "purple", "Home Office": "amber", "Small Business": "green" }[s] ?? "blue") as any;

  return (
    <div>
      {/* Top row */}
      <div className="chart-grid">
        {/* New vs Returning */}
        <ChartCard title="New vs Returning Customers" sub="By order count in period">
          {nL ? <div style={{ height: 200, background: "var(--bg-card2)", borderRadius: 6 }} />
            : (
              <>
                <div style={{ display: "flex", gap: 24, marginBottom: 12 }}>
                  {(nvr ?? []).map((r: any, i: number) => (
                    <div key={r.customer_type} style={{ textAlign: "center" }}>
                      <div style={{ fontSize: 28, fontWeight: 700, color: nvrColors[i] }}>{r.pct}%</div>
                      <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2 }}>{r.customer_type}</div>
                      <div style={{ fontSize: 12, color: "var(--text-dim)" }}>{fmtNum(r.count)} customers</div>
                    </div>
                  ))}
                </div>
                <ResponsiveContainer width="100%" height={130}>
                  <PieChart>
                    <Pie data={nvr ?? []} cx="50%" cy="50%" innerRadius={38} outerRadius={58} dataKey="count" stroke="none">
                      {(nvr ?? []).map((_: any, i: number) => <Cell key={i} fill={nvrColors[i]} />)}
                    </Pie>
                    <Tooltip formatter={(v: number) => [fmtNum(v) + " customers"]} />
                  </PieChart>
                </ResponsiveContainer>
              </>
            )
          }
        </ChartCard>

        {/* Purchase frequency */}
        <ChartCard title="Purchase Frequency Distribution" sub="Orders per customer">
          {fL ? <div style={{ height: 200, background: "var(--bg-card2)", borderRadius: 6 }} />
            : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={freq ?? []} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e2d45" vertical={false} />
                  <XAxis dataKey="order_count" tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} label={{ value: "Orders", position: "insideBottom", fill: "#64748b", fontSize: 10, offset: -4 }} />
                  <YAxis tick={{ fill: "#64748b", fontSize: 10 }} axisLine={false} tickLine={false} width={32} />
                  <Tooltip content={<ChartTooltip />} cursor={{ fill: "transparent" }} />
                  <Bar dataKey="customers" name="Customers" fill="#a855f7" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </ChartCard>
      </div>

      {/* Top customers table */}
      <ChartCard title="Top Customers by Lifetime Spending" sub="Filtered by date range">
        <div className="dash-controls">
          <input
            placeholder="Search customers…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              background: "var(--bg)", border: "1px solid var(--border-2)", color: "var(--text)",
              borderRadius: 6, padding: "6px 10px", fontSize: 12, outline: "none", width: 200,
            }}
          />
        </div>
        <div className="table-wrapper">
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12 }}>
            <thead>
              <tr>
                {["#", "Customer", "Segment", "Region", "Orders", "Total Spent", "Avg Order", "Type"].map(h => (
                  <th key={h} style={{
                    textAlign: "left", padding: "8px 10px", color: "var(--text-muted)",
                    fontWeight: 600, fontSize: 11, letterSpacing: "0.4px", textTransform: "uppercase",
                    borderBottom: "1px solid var(--border)", whiteSpace: "nowrap",
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {cL
                ? Array.from({ length: 8 }).map((_, i) => (
                  <tr key={i}><td colSpan={8} style={{ padding: 10 }}>
                    <div style={{ height: 16, background: "var(--bg-card2)", borderRadius: 4 }} />
                  </td></tr>
                ))
                : filtered.map((c, i) => (
                  <tr key={c.customer_id}>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                      <span style={{ fontFamily: "monospace", fontSize: 11, color: RANK_COLORS[i] ?? "var(--text-muted)" }}>#{i + 1}</span>
                    </td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                      <div style={{ color: "var(--text)", fontWeight: 500 }}>{c.customer_name}</div>
                      <div style={{ fontSize: 10, color: "var(--text-muted)" }}>{c.state}</div>
                    </td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                      <Badge variant={segBadge(c.segment)}>{c.segment}</Badge>
                    </td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", color: "var(--text-dim)" }}>{c.region}</td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", fontFamily: "monospace", color: "var(--text-dim)" }}>{c.total_orders}</td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", fontFamily: "monospace", color: "var(--green)" }}>{fmt$(c.total_spent, true)}</td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)", fontFamily: "monospace", color: "var(--text-dim)" }}>{fmt$(c.avg_order_value)}</td>
                    <td style={{ padding: "9px 10px", borderBottom: "1px solid var(--border)" }}>
                      <Badge variant={c.customer_type === "Returning" ? "blue" : "green"}>{c.customer_type}</Badge>
                    </td>
                  </tr>
                ))
              }
            </tbody>
          </table>
        </div>
      </ChartCard>
    </div>
  );
};
