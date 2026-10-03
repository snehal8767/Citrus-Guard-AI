// Alert Center: human-in-the-loop VERIFY / REJECT / REQUEST RESCAN.
import { useState } from "react";
import { api } from "../api/client";
import { EmptyState, ErrorAlert, LoadingSpinner, PageHeader, StatusBadge } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime } from "../utils/helpers";

export default function Alerts() {
  const alerts = useApi(() => api.listAlerts());
  const [comment, setComment] = useState("");
  const [busyId, setBusyId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const act = async (id: number, decision: "verify" | "reject" | "rescan") => {
    setBusyId(id);
    setError(null);
    try {
      if (decision === "verify") await api.verifyAlert(id, decision, comment || undefined);
      else if (decision === "reject") await api.rejectAlert(id, comment || undefined);
      else await api.rescanAlert(id, comment || undefined);
      alerts.refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Action failed");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div>
      <PageHeader title="Alert Center" subtitle="Human-in-the-loop: the AI only raises alerts — a logged-in farmer verifies before any intervention." />
      {error && <div className="mb-4"><ErrorAlert message={error} /></div>}
      {alerts.loading ? (
        <LoadingSpinner />
      ) : alerts.error ? (
        <ErrorAlert message={alerts.error} onRetry={alerts.refresh} />
      ) : !alerts.data || alerts.data.length === 0 ? (
        <EmptyState message="No alerts. Run an orchard scan to detect issues." />
      ) : (
        <div className="space-y-4">
          {alerts.data.map((a) => (
            <div key={a.id} className="card" data-testid={`alert-${a.id}`}>
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="font-bold text-leaf-900">Alert #{a.id} · {a.alert_type}</div>
                <div className="flex gap-2">
                  <StatusBadge status={a.severity} />
                  <StatusBadge status={a.status} />
                </div>
              </div>
              <p className="mt-2 text-sm text-gray-700">{a.message}</p>
              <div className="mt-1 text-xs text-gray-500">
                Zone {a.zone_id} · risk {a.risk_score}/100 · {formatDateTime(a.created_at)}
              </div>
              <div className="mt-3 flex flex-wrap items-center gap-2">
                <input
                  className="input max-w-xs"
                  placeholder="Comment (optional)"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                />
                <button className="btn-primary" disabled={busyId === a.id} onClick={() => act(a.id, "verify")} data-testid={`verify-${a.id}`}>
                  VERIFY
                </button>
                <button className="btn-secondary" disabled={busyId === a.id} onClick={() => act(a.id, "reject")}>
                  REJECT
                </button>
                <button className="btn-secondary" disabled={busyId === a.id} onClick={() => act(a.id, "rescan")}>
                  REQUEST RESCAN
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
