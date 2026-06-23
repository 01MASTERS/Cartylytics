export function fmt$( n: number, compact = false): string {
  if (compact && n >= 1_000_000)
    return "$" + (n / 1_000_000).toFixed(1) + "M";
  if (compact && n >= 1_000)
    return "$" + (n / 1_000).toFixed(1) + "K";
  return new Intl.NumberFormat("en-US", {
    style: "currency", currency: "USD", minimumFractionDigits: 0, maximumFractionDigits: 0,
  }).format(n);
}

export function fmtNum(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}

export function fmtPct(n: number | null | undefined): string {
  if (n == null) return "N/A";
  return (n >= 0 ? "+" : "") + n.toFixed(1) + "%";
}

export function fmtMonth(m: string): string {
  const [y, mo] = m.split("-");
  const d = new Date(Number(y), Number(mo) - 1, 1);
  return d.toLocaleString("en-US", { month: "short", year: "2-digit" });
}

export function growthColor(v: number | null | undefined): string {
  if (v == null) return "#94a3b8";
  return v >= 0 ? "#22c55e" : "#ef4444";
}
