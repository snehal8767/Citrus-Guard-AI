// Dashboard: KPIs from /metrics, trend charts from /history, RUN ORCHARD SCAN.
import { useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { api } from "../api/client";
import ScanProgress from "../components/ScanProgress";
import CommandConsole from "../components/CommandConsole";
import { EmptyState, ErrorAlert, KpiCard, LoadingSpinner, PageHeader } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime, formatNumber } from "../utils/helpers";

const ORCHARD_ID = 1;

export default function Dashboard() {
  const metrics = useApi(() => api.getMetrics(ORCHARD_ID));
  const history = useApi(() => api.listHistory(ORCHARD_ID));
  const alerts = useApi(() => api.listAlerts());
  const [scanning, setScanning] = useState(false);
  const [scanError, setScanError] = useState<string | null>(null);

  const runScan = async () => {
    setScanning(true);
    setScanError(null);
    try {
      await api.runScan(ORCHARD_ID);
      metrics.refresh();
      history.refresh();
      alerts.refresh();
    } catch (e) {
      setScanError(e instanceof Error ? e.message : "Scan failed");
    } finally {
      setScanning(false);
    }
  };

  // Aggregate history per day for charts (average across zones).
  const trend = (() => {
    if (!history.data) return [];
    const byDay = new Map<string, { health: number[]; risk: number[]; affected: number }>();
    for (const h of history.data) {
      const day = new Date(h.recorded_at).toISOString().slice(0, 10);
      const entry = byDay.get(day) ?? { health: [], risk: [], affected: 0 };
      entry.health.push(h.health_score);
      entry.risk.push(h.risk_score);
      entry.affected += h.affected_area;
      byDay.set(day, entry);
    }
    return [...byDay.entries()]
      .sort()
      .slice(-14)
      .map(([day, v]) => ({
        day: day.slice(5),
        health: +(v.health.reduce((a, b) => a + b, 0) / v.health.length).toFixed(1),
        risk: +(v.risk.reduce((a, b) => a + b, 0) / v.risk.length).toFixed(1),
        affected: +v.affected.toFixed(2),
      }));
  })();

  const m = metrics.data;

  return (
    <div>
      <PageHeader
        title="Orchard Dashboard"
        subtitle="Vidarbha Orange Estate · 50 acres · Nagpur, Maharashtra — all numbers come from the live database."
        actions={
          <button className="btn-primary" onClick={runScan} disabled={scanning} data-testid="run-scan">
            {scanning ? "Scanning…" : "▶ RUN ORCHARD SCAN"}
          </button>
        }
      />

      {scanning && <div className="mb-6"><ScanProgress /></div>}
      {scanError && <div className="mb-6"><ErrorAlert message={scanError} /></div>}

      {metrics.loading ? (
        <LoadingSpinner text="Loading metrics…" />
      ) : metrics.error ? (
        <ErrorAlert message={metrics.error} onRetry={metrics.refresh} />
      ) : m ? (
        <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
          <KpiCard label="Total Orchard Area" value={`${formatNumber(m.total_orchard_area)} ac`} />
          <KpiCard label="Monitored Area" value={`${formatNumber(m.monitored_area)} ac`} sub={`${formatNumber(m.monitoring_coverage)}% coverage`} />
          <KpiCard label="Healthy Area" value={`${formatNumber(m.healthy_area)} ac`} />
          <KpiCard label="At-Risk Area" value={`${formatNumber(m.at_risk_area)} ac`} />
          <KpiCard label="Critical Zones" value={String(m.critical_zones)} />
          <KpiCard label="Active Alerts" value={String(m.active_alerts)} />
          <KpiCard label="Latest Scan" value={m.latest_scan ? new Date(m.latest_scan).toLocaleDateString() : "—"} sub={formatDateTime(m.latest_scan)} />
          <KpiCard label="Sensor Health" value={`${formatNumber(m.sensor_health, 0)}%`} />
        </div>
      ) : (
        <EmptyState message="No metrics yet. Run a scan to populate the dashboard." />
      )}

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="section-title">Health & Risk Trend (14 days)</div>
          {history.loading ? (
            <LoadingSpinner />
          ) : history.error ? (
            <ErrorAlert message={history.error} onRetry={history.refresh} />
          ) : trend.length === 0 ? (
            <EmptyState message="No history yet." />
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" fontSize={11} />
                <YAxis fontSize={11} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="health" stroke="#4a8d3e" name="Health score" dot={false} />
                <Line type="monotone" dataKey="risk" stroke="#f98707" name="Risk score" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
        <div className="card">
          <div className="section-title">Affected Area (acres / day)</div>
          {trend.length === 0 ? (
            <EmptyState message="No history yet." />
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" fontSize={11} />
                <YAxis fontSize={11} />
                <Tooltip />
                <Bar dataKey="affected" fill="#f98707" name="Affected acres" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="section-title">Monitoring History (risk by day)</div>
          {trend.length === 0 ? (
            <EmptyState message="No history yet." />
          ) : (
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={trend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" fontSize={11} />
                <YAxis fontSize={11} />
                <Tooltip />
                <Area type="monotone" dataKey="risk" stroke="#dc2626" fill="#fecaca" name="Risk" />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>
        <CommandConsole orchardId={ORCHARD_ID} />
      </div>

      <div className="card mt-6">
        <div className="section-title">Latest Alerts</div>
        {alerts.loading ? (
          <LoadingSpinner />
        ) : alerts.error ? (
          <ErrorAlert message={alerts.error} onRetry={alerts.refresh} />
        ) : !alerts.data || alerts.data.length === 0 ? (
          <EmptyState message="No alerts. Run a scan to detect crop-health issues." />
        ) : (
          <ul className="mt-3 space-y-2 text-sm">
            {alerts.data.slice(0, 5).map((a) => (
              <li key={a.id} className="flex items-center justify-between rounded-lg bg-leaf-50 px-3 py-2">
                <span>
                  <strong>Zone alert #{a.id}</strong> · {a.severity} · risk {a.risk_score}/100 · {a.status}
                </span>
                <a href="/alerts" className="font-semibold text-leaf-700 hover:underline">
                  Open →
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
