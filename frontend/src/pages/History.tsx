// History page: scans, detections, risk changes, alerts, interventions with search/filter/sort.
import { useMemo, useState } from "react";
import { api } from "../api/client";
import { EmptyState, ErrorAlert, LoadingSpinner, PageHeader, StatusBadge } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime, formatNumber } from "../utils/helpers";

export default function History() {
  const history = useApi(() => api.listHistory(1));
  const scans = useApi(() => api.listScans(1));
  const alerts = useApi(() => api.listAlerts());
  const interventions = useApi(() => api.listInterventions());
  const zones = useApi(() => api.listZones(1));
  const [query, setQuery] = useState("");
  const [sortDir, setSortDir] = useState<"desc" | "asc">("desc");

  const zoneName = (id: number) => zones.data?.find((z) => z.id === id)?.zone_name ?? String(id);

  const rows = useMemo(() => {
    const data = history.data ?? [];
    const q = query.trim().toLowerCase();
    const filtered = q
      ? data.filter((h) => zoneName(h.zone_id).toLowerCase().includes(q) || String(h.risk_score).includes(q))
      : data;
    return [...filtered].sort((a, b) =>
      sortDir === "desc"
        ? b.recorded_at.localeCompare(a.recorded_at)
        : a.recorded_at.localeCompare(b.recorded_at)
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [history.data, query, sortDir, zones.data]);

  return (
    <div>
      <PageHeader title="Monitoring History" subtitle="Every scan, detection, risk change, alert and intervention — searchable and sortable." />
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="section-title">Previous scans</div>
          {scans.loading ? <LoadingSpinner /> : scans.error ? <ErrorAlert message={scans.error} onRetry={scans.refresh} /> : (
            <ul className="mt-3 max-h-56 space-y-1.5 overflow-y-auto text-sm">
              {(scans.data ?? []).map((s) => (
                <li key={s.id} className="flex justify-between rounded-lg bg-leaf-50 px-3 py-1.5">
                  <span>Scan #{s.id} · {s.detections.length} detections</span>
                  <span>{formatNumber(s.coverage)}% · {formatDateTime(s.timestamp)}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="card">
          <div className="section-title">Alerts & interventions</div>
          <div className="mt-3 max-h-56 space-y-1.5 overflow-y-auto text-sm">
            {(alerts.data ?? []).map((a) => (
              <div key={`a${a.id}`} className="flex items-center justify-between rounded-lg bg-leaf-50 px-3 py-1.5">
                <span>Alert #{a.id} · Zone {zoneName(a.zone_id)} · {a.alert_type}</span>
                <StatusBadge status={a.status} />
              </div>
            ))}
            {(interventions.data ?? []).map((i) => (
              <div key={`i${i.id}`} className="flex items-center justify-between rounded-lg bg-citrus-50 px-3 py-1.5">
                <span>Intervention #{i.id} · Zone {zoneName(i.zone_id)}</span>
                <StatusBadge status={i.status} />
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card mt-6">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="section-title">Risk history ({rows.length} records)</div>
          <div className="flex gap-2">
            <input className="input max-w-[200px]" placeholder="Search zone or risk…" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button className="btn-secondary" onClick={() => setSortDir((d) => (d === "desc" ? "asc" : "desc"))}>
              {sortDir === "desc" ? "Newest first" : "Oldest first"}
            </button>
          </div>
        </div>
        {history.loading ? <LoadingSpinner /> : history.error ? <ErrorAlert message={history.error} onRetry={history.refresh} /> : rows.length === 0 ? (
          <div className="mt-3"><EmptyState message="No history records." /></div>
        ) : (
          <div className="mt-3 max-h-96 overflow-y-auto">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-white">
                <tr className="text-left text-gray-500">
                  <th className="py-1">Recorded</th><th>Zone</th><th>Health</th><th>Risk</th><th>Affected (ac)</th>
                </tr>
              </thead>
              <tbody>
                {rows.slice(0, 100).map((h) => (
                  <tr key={h.id} className="border-t border-gray-100">
                    <td className="py-1">{formatDateTime(h.recorded_at)}</td>
                    <td>{zoneName(h.zone_id)}</td>
                    <td>{formatNumber(h.health_score)}</td>
                    <td className="font-semibold">{formatNumber(h.risk_score)}</td>
                    <td>{formatNumber(h.affected_area, 2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
