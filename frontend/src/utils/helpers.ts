// Shared helpers: status colors, formatting.

export function badgeClass(status: string): string {
  const s = (status || "").toLowerCase().replace(/[\s_]/g, "-");
  if (s === "healthy" || s === "verified" || s === "resolved" || s === "completed" || s === "normal") {
    return "badge badge-healthy";
  }
  if (s === "watch" || s === "under-review" || s === "new") {
    return "badge badge-watch";
  }
  if (s.includes("at-risk") || s === "action-planned" || s === "warning") {
    return "badge badge-at-risk";
  }
  if (s === "critical" || s === "rejected") {
    return "badge badge-critical";
  }
  return "badge badge-default";
}

export function zoneColor(status: string): string {
  switch ((status || "").toLowerCase()) {
    case "healthy":
      return "#4a8d3e";
    case "watch":
      return "#eab308";
    case "at risk":
      return "#f98707";
    case "critical":
      return "#dc2626";
    default:
      return "#6b7280";
  }
}

export function formatDateTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString();
}

export function formatNumber(n: number | null | undefined, digits = 1): string {
  if (n === null || n === undefined || Number.isNaN(n)) return "—";
  return Number(n).toFixed(digits);
}
