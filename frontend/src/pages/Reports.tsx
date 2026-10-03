// Reports page: generate and download the HTML orchard report.
import { useState } from "react";
import { getToken } from "../api/client";
import { PageHeader } from "../components/ui";

export default function Reports() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const download = async () => {
    setBusy(true);
    setError(null);
    try {
      const res = await fetch("/api/reports?orchard_id=1", {
        headers: { Authorization: `Bearer ${getToken()}` },
      });
      if (!res.ok) throw new Error(`Report failed (${res.status})`);
      const html = await res.text();
      const blob = new Blob([html], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "citrusguard-report.html";
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Download failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Reports"
        subtitle="Generate the orchard health report (metrics, zones, alerts, interventions, scans) and download it as HTML."
        actions={
          <button className="btn-primary" onClick={download} disabled={busy} data-testid="download-report">
            {busy ? "Generating…" : "Generate & download report"}
          </button>
        }
      />
      {error && <div className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</div>}
      <div className="card">
        <div className="section-title">What is included</div>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-gray-700">
          <li>Key metrics: total / monitored / healthy / at-risk area, critical zones, active alerts, coverage, sensor health</li>
          <li>Per-zone health status and risk scores</li>
          <li>Recent alerts and their verification state</li>
          <li>Intervention plans with target areas</li>
          <li>Recent scan history</li>
        </ul>
        <p className="mt-3 text-xs text-gray-500">The report is generated live from the database via GET /reports.</p>
      </div>
    </div>
  );
}
