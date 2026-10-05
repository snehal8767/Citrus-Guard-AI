// Intervention page: precision plan for the verified zone only. NO pesticide dosage.
import { useState } from "react";
import { api } from "../api/client";
import { EmptyState, ErrorAlert, LoadingSpinner, PageHeader, StatusBadge } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime, formatNumber } from "../utils/helpers";

const TYPES = [
  "Targeted canopy inspection and treatment",
  "Localized irrigation adjustment",
  "Affected-branch pruning and sanitation",
  "Follow-up monitoring schedule",
];

export default function Interventions() {
  const zones = useApi(() => api.listZones(1));
  const alerts = useApi(() => api.listAlerts());
  const interventions = useApi(() => api.listInterventions());
  const [zoneId, setZoneId] = useState(2);
  const recommendation = useApi(() => api.getRecommendation(zoneId), [zoneId]);  const [itype, setItype] = useState(TYPES[0]);
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const verifiedAlert = alerts.data?.find((a) => a.zone_id === zoneId && a.status === "Verified");
  const zone = zones.data?.find((z) => z.id === zoneId);
  const fullOrchard = 50.0;

  const create = async () => {
    setBusy(true);
    setError(null);
    try {
      await api.createIntervention({
        zone_id: zoneId,
        intervention_type: itype,
        target_area: zone?.area ?? 6.25,
        reason: reason || undefined,
      });
      interventions.refresh();
      alerts.refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not create intervention");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <PageHeader title="Precision Intervention" subtitle="Plans target only the affected zone — never the whole orchard. Requires a Verified alert (human-in-the-loop). No pesticide dosage is ever shown." />
      {error && <div className="mb-4"><ErrorAlert message={error} /></div>}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="section-title">New intervention plan</div>
          <label className="mt-3 block text-sm font-medium">Target zone</label>
          <select className="input mt-1" value={zoneId} onChange={(e) => setZoneId(Number(e.target.value))}>
            {zones.data?.map((z) => (
              <option key={z.id} value={z.id}>Zone {z.zone_name} — {z.health_status} (risk {z.risk_score})</option>
            ))}
          </select>
          <label className="mt-3 block text-sm font-medium">Intervention type</label>
          <select className="input mt-1" value={itype} onChange={(e) => setItype(e.target.value)}>
            {TYPES.map((t) => <option key={t}>{t}</option>)}
          </select>
          <label className="mt-3 block text-sm font-medium">Reason</label>
          <input className="input mt-1" value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Why is this intervention needed?" />
          {zone && (
            <div className="mt-3 rounded-lg bg-leaf-50 p-3 text-sm">
              <div>Target area: <strong>{formatNumber(zone.area, 2)} ac</strong> (Zone {zone.zone_name} only)</div>
              <div>vs full-orchard treatment: <strong>{formatNumber(fullOrchard, 1)} ac</strong></div>
              <div className="text-leaf-700">Precision approach treats {formatNumber((zone.area / fullOrchard) * 100, 1)}% of the orchard area.</div>
              <div className="mt-1">Detection risk: <strong>{zone.risk_score}/100</strong> · Recommended action: verify affected trees before intervention.</div>
            </div>
          )}
          {!verifiedAlert ? (
            <div className="mt-3 rounded-lg bg-yellow-50 p-3 text-sm text-yellow-800">
              No Verified alert for this zone yet. Verify the alert in the Alert Center first.
            </div>
          ) : (
            <div className="mt-3 rounded-lg bg-leaf-100 p-3 text-sm text-leaf-800">
              Verified alert #{verifiedAlert.id} found — intervention can be created.
            </div>
          )}
          <button className="btn-primary mt-4" onClick={create} disabled={busy || !verifiedAlert} data-testid="create-intervention">
            {busy ? "Creating…" : "Create intervention plan"}
          </button>
        </div>
        <div className="card">
          <div className="section-title">Existing plans</div>
          {interventions.loading ? (
            <LoadingSpinner />
          ) : interventions.error ? (
            <ErrorAlert message={interventions.error} onRetry={interventions.refresh} />
          ) : !interventions.data || interventions.data.length === 0 ? (
            <EmptyState message="No interventions yet." />
          ) : (
            <ul className="mt-3 space-y-2 text-sm">
              {interventions.data.map((i) => (
                <li key={i.id} className="rounded-lg bg-leaf-50 px-3 py-2">
                  <div className="flex items-center justify-between">
                    <strong>#{i.id} · {i.intervention_type}</strong>
                    <StatusBadge status={i.status} />
                  </div>
                  <div className="text-gray-600">Zone {i.zone_id} · {formatNumber(i.target_area, 2)} ac · {formatDateTime(i.created_at)}</div>
                  {i.reason && <div className="text-gray-600">{i.reason}</div>}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      <div className="card mt-6" data-testid="recommendation-card">
        <div className="section-title">Zone recommendation</div>
        {recommendation.loading ? (
          <LoadingSpinner />
        ) : recommendation.error ? (
          <ErrorAlert message={recommendation.error} onRetry={recommendation.refresh} />
        ) : recommendation.data ? (
          <div className="mt-2 text-sm">
            <div className="text-lg font-bold text-leaf-900">
              Zone {recommendation.data.zone_name} — {recommendation.data.health_status}
            </div>
            <dl className="mt-2 space-y-1">
              <div className="flex gap-2"><dt className="text-gray-500">Detected condition:</dt><dd className="font-medium">{recommendation.data.condition}</dd></div>
              <div className="flex gap-2"><dt className="text-gray-500">Risk:</dt><dd className="font-medium">{formatNumber(recommendation.data.risk)}/100</dd></div>
              <div className="flex gap-2"><dt className="text-gray-500">Affected area:</dt><dd className="font-medium">{formatNumber(recommendation.data.affected_area, 2)} acres</dd></div>
            </dl>
            <div className="mt-3 font-bold text-leaf-900">Recommended action</div>
            <ol className="mt-1 space-y-1">
              {recommendation.data.steps.map((s) => (
                <li key={s} className="rounded-lg bg-leaf-50 px-3 py-1.5">{s}</li>
              ))}
            </ol>
            <div className="mt-3 rounded-lg bg-yellow-50 p-3 text-xs text-yellow-800">
              ⚠️ {recommendation.data.safety_note}
            </div>
          </div>
        ) : (
          <EmptyState message="Select a zone to see its recommendation." />
        )}
      </div>
    </div>
  );
}
