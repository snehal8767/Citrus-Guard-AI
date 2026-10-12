// Alert Center: human-in-the-loop VERIFY / REJECT / REQUEST RESCAN.
import { useState } from "react";
import { api } from "../api/client";
import { EmptyState, ErrorAlert, LoadingSpinner, PageHeader, StatusBadge } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime } from "../utils/helpers";

// Farmer actions are only valid from these alert states (server-enforced).
const ACTIONABLE_STATUSES = new Set(["New", "Under Review"]);

// Friendly explanation for alerts that are past the farmer decision point.
const STATUS_NOTES: Record<string, string> = {
  Verified:
    "Verified by the farmer. Create the intervention plan from the Intervention page.",
  "Action Planned": "An intervention plan has been created. See the Intervention page.",
  Resolved: "Resolved. No further action is needed.",
  Rejected: "Rejected by the farmer. No intervention will be planned.",
  "Rescan Requested": "A rescan was requested. The alert reopens once the new scan lands.",
};

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
          {alerts.data.map((a) => {
            const canAct = ACTIONABLE_STATUSES.has(a.status);
            return (
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
              {canAct ? (
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
              ) : (
                <p className="mt-3 text-sm text-gray-600">
                  {STATUS_NOTES[a.status] ?? `Status: ${a.status}. No farmer action is available on this alert.`}
                </p>
              )}
            </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
