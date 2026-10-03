// Drone Mission page: clearly labelled SIMULATION with animated telemetry.
import { useEffect, useState } from "react";
import { api } from "../api/client";
import ScanProgress from "../components/ScanProgress";
import { ErrorAlert, PageHeader } from "../components/ui";
import { useApi } from "../hooks/useApi";

export default function DroneMission() {
  const scans = useApi(() => api.listScans(1));
  const [flying, setFlying] = useState(false);
  const [battery, setBattery] = useState(100);
  const [coverage, setCoverage] = useState(0);
  const [images, setImages] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!flying) return;
    const t = setInterval(() => {
      setBattery((b) => Math.max(12, b - 2));
      setCoverage((c) => Math.min(100, c + 4));
      setImages((i) => i + 7);
    }, 400);
    return () => clearInterval(t);
  }, [flying]);

  const launch = async () => {
    setError(null);
    setFlying(true);
    setBattery(100);
    setCoverage(0);
    setImages(0);
    try {
      await api.runScan(1);
      scans.refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Mission failed");
      setFlying(false);
    }
  };

  return (
    <div>
      <PageHeader
        title="Drone Mission"
        subtitle="SIMULATION — animated telemetry for the demo. Results come from the real POST /scans API."
        actions={
          <button className="btn-primary" onClick={launch} disabled={flying} data-testid="launch-mission">
            {flying ? "Mission in progress…" : "Launch simulated mission"}
          </button>
        }
      />
      {error && <div className="mb-4"><ErrorAlert message={error} /></div>}

      <div className="grid gap-3 sm:grid-cols-3">
        <div className="card"><div className="text-xs font-semibold uppercase text-gray-500">Battery (simulated)</div>
          <div className="mt-1 text-2xl font-bold text-leaf-900">{battery}%</div>
          <div className="mt-2 h-2 rounded-full bg-gray-200"><div className="h-full rounded-full bg-leaf-500" style={{ width: `${battery}%` }} /></div></div>
        <div className="card"><div className="text-xs font-semibold uppercase text-gray-500">Coverage (simulated)</div>
          <div className="mt-1 text-2xl font-bold text-leaf-900">{coverage}%</div>
          <div className="mt-2 h-2 rounded-full bg-gray-200"><div className="h-full rounded-full bg-citrus-500" style={{ width: `${coverage}%` }} /></div></div>
        <div className="card"><div className="text-xs font-semibold uppercase text-gray-500">Images captured (simulated)</div>
          <div className="mt-1 text-2xl font-bold text-leaf-900">{images}</div></div>
      </div>

      {flying && (
        <div className="mt-6"><ScanProgress onDone={() => setFlying(false)} /></div>
      )}

      <div className="card mt-6">
        <div className="section-title">Mission history (real scans from database)</div>
        <ul className="mt-3 space-y-1.5 text-sm">
          {scans.data?.slice(0, 8).map((s) => (
            <li key={s.id} className="flex justify-between rounded-lg bg-leaf-50 px-3 py-2">
              <span>Scan #{s.id} · {s.scan_type}</span>
              <span>{s.coverage}% coverage · {s.status}</span>
            </li>
          )) ?? <li className="text-gray-500">No missions yet.</li>}
        </ul>
      </div>
    </div>
  );
}
