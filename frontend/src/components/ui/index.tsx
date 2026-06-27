import React from "react";

// ── Skeleton ───────────────────────────────────────────────────────────────────
interface SkeletonProps { height?: number; className?: string; }
export const Skeleton: React.FC<SkeletonProps> = ({ height = 20, className = "" }) => (
  <div
    className={className}
    style={{
      height,
      borderRadius: 6,
      background: "linear-gradient(90deg,#1a2235 25%,#1e2d45 50%,#1a2235 75%)",
      backgroundSize: "400% 100%",
      animation: "shimmer 1.4s infinite",
    }}
  />
);

// ── KPI Card ───────────────────────────────────────────────────────────────────
interface KpiCardProps {
  label:   string;
  value:   string;
  sub?:    string;
  growth?: number | null;
  accent?: "blue" | "green" | "purple" | "amber" | "cyan";
  loading?: boolean;
}

const ACCENT_COLORS: Record<string, string> = {
  blue: "#3b82f6", green: "#22c55e", purple: "#a855f7",
  amber: "#f59e0b", cyan: "#06b6d4",
};

export const KpiCard: React.FC<KpiCardProps> = ({
  label, value, sub, growth, accent = "blue", loading = false,
}) => (
  <div
    style={{
      background: "var(--bg-card)", border: "1px solid var(--border)",
      borderRadius: "var(--radius)", padding: "18px 20px",
      borderTop: `2px solid ${ACCENT_COLORS[accent]}`,
      position: "relative",
    }}
  >
    <div style={{ fontSize: 11, fontWeight: 600, letterSpacing: "0.5px",
      textTransform: "uppercase", color: "var(--text-muted)", marginBottom: 8 }}>
      {label}
    </div>
    {loading
      ? <Skeleton height={32} />
      : <div style={{ fontSize: 26, fontWeight: 700, letterSpacing: "-0.5px",
          lineHeight: 1.1, marginBottom: 6 }}>{value}</div>
    }
    {growth != null && !loading && (
      <div style={{ fontSize: 12, fontWeight: 600, color: growth >= 0 ? "var(--green)" : "var(--red)" }}>
        {growth >= 0 ? "↑ " : "↓ "}{Math.abs(growth).toFixed(1)}% vs prior period
      </div>
    )}
    {sub && !loading && (
      <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2 }}>{sub}</div>
    )}
  </div>
);

// ── Chart Card ─────────────────────────────────────────────────────────────────
interface ChartCardProps {
  title:    string;
  sub?:     string;
  badge?:   string;
  children: React.ReactNode;
  style?:   React.CSSProperties;
}
export const ChartCard: React.FC<ChartCardProps> = ({ title, sub, badge, children, style }) => (
  <div style={{
    background: "var(--bg-card)", border: "1px solid var(--border)",
    borderRadius: "var(--radius)", padding: "18px 20px", ...style,
  }}>
    <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 16 }}>
      <div>
        <div style={{ fontSize: 13, fontWeight: 600 }}>{title}</div>
        {sub && <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 2 }}>{sub}</div>}
      </div>
      {badge && (
        <span style={{
          fontSize: 10, fontWeight: 600, padding: "3px 8px", borderRadius: 20,
          background: "var(--accent-glow)", color: "var(--accent)", letterSpacing: ".3px",
          flexShrink: 0,
        }}>{badge}</span>
      )}
    </div>
    {children}
  </div>
);

// ── Tab Bar ────────────────────────────────────────────────────────────────────
interface TabBarProps { tabs: string[]; active: string; onChange: (t: string) => void; }
export const TabBar: React.FC<TabBarProps> = ({ tabs, active, onChange }) => (
  <div style={{ display: "flex", gap: 4 }}>
    {tabs.map(t => (
      <button key={t} onClick={() => onChange(t)} style={{
        padding: "6px 14px", borderRadius: 6, fontSize: 12, fontWeight: 500,
        cursor: "pointer", border: "none", transition: "all .12s",
        background: active === t ? "var(--accent-glow)" : "none",
        color: active === t ? "var(--accent)" : "var(--text-muted)",
      }}>{t}</button>
    ))}
  </div>
);

// ── Badge ──────────────────────────────────────────────────────────────────────
type BadgeVariant = "blue" | "green" | "amber" | "purple" | "red";
const BADGE_STYLES: Record<BadgeVariant, React.CSSProperties> = {
  blue:   { background: "var(--accent-glow)", color: "var(--accent)" },
  green:  { background: "var(--green-bg)",    color: "var(--green)" },
  amber:  { background: "rgba(245,158,11,.1)", color: "var(--amber)" },
  purple: { background: "rgba(168,85,247,.1)", color: "var(--purple)" },
  red:    { background: "var(--red-bg)",       color: "var(--red)" },
};
interface BadgeProps { children: React.ReactNode; variant?: BadgeVariant; }
export const Badge: React.FC<BadgeProps> = ({ children, variant = "blue" }) => (
  <span style={{
    display: "inline-block", fontSize: 10, fontWeight: 600,
    padding: "2px 7px", borderRadius: 10, letterSpacing: ".3px",
    ...BADGE_STYLES[variant],
  }}>{children}</span>
);

// ── Progress Bar ───────────────────────────────────────────────────────────────
interface ProgressBarProps { value: number; max: number; color?: string; }
export const ProgressBar: React.FC<ProgressBarProps> = ({ value, max, color = "#3b82f6" }) => (
  <div style={{ height: 5, background: "var(--bg-card2)", borderRadius: 3, overflow: "hidden", minWidth: 60 }}>
    <div style={{
      height: "100%", borderRadius: 3,
      width: `${Math.min(100, (value / max) * 100)}%`,
      background: color,
    }} />
  </div>
);

// ── Error Box ──────────────────────────────────────────────────────────────────
export const ErrorBox: React.FC<{ message: string }> = ({ message }) => (
  <div style={{
    background: "var(--red-bg)", border: "1px solid var(--red)", color: "var(--red)",
    borderRadius: "var(--radius)", padding: "12px 16px", fontSize: 13, marginBottom: 16,
  }}>⚠ {message}</div>
);

// ── Empty State ────────────────────────────────────────────────────────────────
export const EmptyState: React.FC<{ message?: string }> = ({ message = "No data for selected range" }) => (
  <div style={{
    display: "flex", flexDirection: "column", alignItems: "center",
    justifyContent: "center", padding: "48px 0", color: "var(--text-muted)", fontSize: 13, gap: 8,
  }}>
    <span style={{ fontSize: 32 }}>📭</span>
    <span>{message}</span>
  </div>
);

// ── Recharts custom tooltip ────────────────────────────────────────────────────
interface TooltipProps {
  active?: boolean;
  payload?: { name: string; value: number; color: string }[];
  label?:   string;
  prefix?:  string;
}
export const ChartTooltip: React.FC<TooltipProps> = ({ active, payload, label, prefix = "" }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: "#111827", border: "1px solid #1e2d45",
      borderRadius: 8, padding: "10px 14px", fontSize: 12,
    }}>
      <p style={{ color: "#94a3b8", marginBottom: 6, fontSize: 11 }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color, fontFamily: "monospace" }}>
          {p.name}: {prefix}{new Intl.NumberFormat("en-US").format(Math.round(p.value))}
        </p>
      ))}
    </div>
  );
};

// ── Filter Bar ─────────────────────────────────────────────────────────────────
interface FilterBarProps {
  range:    { startDate?: string; endDate?: string };
  onChange: (r: { startDate?: string; endDate?: string }) => void;
}
export const FilterBar: React.FC<FilterBarProps> = ({ range, onChange }) => {
  const [local, setLocal] = React.useState(range);

  const quick = (days: number) => {
    const end   = new Date();
    const start = new Date();
    start.setDate(end.getDate() - days);
    const r = {
      startDate: start.toISOString().slice(0, 10),
      endDate:   end.toISOString().slice(0, 10),
    };
    setLocal(r);
    onChange(r);
  };

  const inputStyle: React.CSSProperties = {
    background: "var(--bg)", border: "1px solid var(--border-2)", color: "var(--text)",
    borderRadius: 6, padding: "5px 10px", fontSize: 12, outline: "none",
    colorScheme: "dark",
  };

  const QUICK: [string, number][] = [["30d", 30], ["90d", 90], ["1Y", 365], ["All", 1100]];

  return (
    <div className="filter-bar">
      <div className="filter-inputs">
        <label style={{ fontSize: 12, color: "var(--text-muted)", fontWeight: 500 }}>From</label>
        <input type="date" style={inputStyle} value={local.startDate || ""}
          onChange={e => setLocal({ ...local, startDate: e.target.value })} />
        <label style={{ fontSize: 12, color: "var(--text-muted)", fontWeight: 500 }}>To</label>
        <input type="date" style={inputStyle} value={local.endDate || ""}
          onChange={e => setLocal({ ...local, endDate: e.target.value })} />
        <button onClick={() => onChange(local)} style={{
          background: "var(--accent)", color: "white", border: "none",
          borderRadius: 6, padding: "6px 14px", fontSize: 12, fontWeight: 600, cursor: "pointer",
        }}>Apply</button>
      </div>
      <div className="filter-quick">
        {QUICK.map(([l, d]) => (
          <button key={l} onClick={() => quick(d)} style={{
            background: "var(--bg)", border: "1px solid var(--border-2)", color: "var(--text-muted)",
            borderRadius: 5, padding: "4px 8px", fontSize: 11, fontWeight: 500, cursor: "pointer",
          }}>{l}</button>
        ))}
      </div>
    </div>
  );
};
