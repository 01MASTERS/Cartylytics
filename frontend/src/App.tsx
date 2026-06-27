import React, { useState } from "react";
import { FilterBar } from "./components/ui";
import { ExecutiveDashboard } from "./pages/ExecutiveDashboard";
import { ProductDashboard }   from "./pages/ProductDashboard";
import { CustomerDashboard }  from "./pages/CustomerDashboard";
import { GeographyDashboard } from "./pages/GeographyDashboard";
import type { DateRange } from "./types";

type PageId = "executive" | "products" | "customers" | "geography";

const NAV: { id: PageId; label: string; icon: string }[] = [
  { id: "executive",  label: "Executive",  icon: "📊" },
  { id: "products",   label: "Products",   icon: "📦" },
  { id: "customers",  label: "Customers",  icon: "👥" },
  { id: "geography",  label: "Geography",  icon: "🗺️"  },
];

const PAGE_META: Record<PageId, { title: string; sub: string }> = {
  executive:  { title: "Executive Dashboard",  sub: "Revenue, profit & growth at a glance" },
  products:   { title: "Product Dashboard",    sub: "Top performers, category mix & profitability" },
  customers:  { title: "Customer Dashboard",   sub: "Spend analysis, segments & purchase patterns" },
  geography:  { title: "Geography Dashboard",  sub: "Regional revenue, profit & market reach" },
};

export default function App() {
  const [page,  setPage]  = useState<PageId>("executive");
  const [range, setRange] = useState<DateRange>({ startDate: "2022-01-01", endDate: "2024-09-30" });

  const meta     = PAGE_META[page];
  const PageComp = {
    executive:  ExecutiveDashboard,
    products:   ProductDashboard,
    customers:  CustomerDashboard,
    geography:  GeographyDashboard,
  }[page];

  return (
    <div className="app-layout">
      {/* ── Sidebar ────────────────────────────────────────────── */}
      <aside className="sidebar">
        {/* Logo */}
        <div style={{ padding: "24px 20px 20px", borderBottom: "1px solid var(--border)" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 17, fontWeight: 700, letterSpacing: "-0.4px" }}>
            <div style={{
              width: 32, height: 32, borderRadius: 8,
              background: "linear-gradient(135deg,#3b82f6,#6366f1)",
              display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
            }}>📈</div>
            <div>
              <div>Cartlytics</div>
              <div style={{ fontSize: 10, color: "var(--text-muted)", fontWeight: 400, letterSpacing: "0.5px", textTransform: "uppercase" }}>
                Analytics Platform
              </div>
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav className="sidebar-nav">
          <div style={{ fontSize: 10, fontWeight: 600, letterSpacing: 1, textTransform: "uppercase",
            color: "var(--text-muted)", padding: "8px 8px 10px" }}>Dashboards</div>
          {NAV.map(n => (
            <button key={n.id} onClick={() => setPage(n.id)} className={`sidebar-nav-btn ${page === n.id ? 'active' : ''}`} style={{
              background:  page === n.id ? "var(--accent-glow)" : "none",
              color:       page === n.id ? "var(--accent)"      : "var(--text-dim)",
              borderLeft:  page === n.id ? "2px solid var(--accent)" : "2px solid transparent",
            }}>
              <span style={{ fontSize: 15, width: 18, textAlign: "center" }}>{n.icon}</span>
              {n.label}
            </button>
          ))}
        </nav>

        {/* Footer */}
        <div style={{ padding: "16px 20px", borderTop: "1px solid var(--border)", fontSize: 11, color: "var(--text-muted)" }} className="sidebar-footer">
          <span style={{ display: "inline-block", width: 6, height: 6, background: "var(--green)", borderRadius: "50%", marginRight: 6 }} />
          Live · MySQL + FastAPI
        </div>
      </aside>

      {/* ── Main ──────────────────────────────────────────────── */}
      <main className="main-area">
        {/* Topbar */}
        <div className="topbar">
          <div>
            <div style={{ fontSize: 16, fontWeight: 600 }}>{meta.title}</div>
            <div style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 1 }}>{meta.sub}</div>
          </div>
          <div style={{ fontSize: 11, color: "var(--text-muted)" }}>
            3,000 orders · 500 customers
          </div>
        </div>

        {/* Content */}
        <div className="dashboard-content">
          <FilterBar range={range} onChange={setRange} />
          <PageComp range={range} />
        </div>
      </main>
    </div>
  );
}
