// Animated 12-step scan progress shown while POST /scans is running.
import { useEffect, useState } from "react";

export const SCAN_STEPS = [
  "Initializing drone mission",
  "Scanning orchard",
  "Collecting imagery",
  "Processing imagery",
  "Running AI analysis",
  "Checking sensor data",
  "Detecting crop-health anomaly",
  "Calculating risk",
  "Updating GIS map",
  "Generating alert",
  "Waiting for farmer verification",
  "Generating intervention plan",
];

export default function ScanProgress({ onDone }: { onDone?: () => void }) {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (step >= SCAN_STEPS.length) {
      onDone?.();
      return;
    }
    const t = setTimeout(() => setStep((s) => s + 1), 450);
    return () => clearTimeout(t);
  }, [step, onDone]);

  const pct = Math.min(100, Math.round((step / SCAN_STEPS.length) * 100));

  return (
    <div className="card" data-testid="scan-progress">
      <div className="flex items-center justify-between">
        <div className="section-title">Drone mission in progress…</div>
        <span className="text-sm font-bold text-citrus-600">{pct}%</span>
      </div>
      <div className="mt-2 h-2.5 overflow-hidden rounded-full bg-leaf-100">
        <div className="h-full rounded-full bg-gradient-to-r from-leaf-500 to-citrus-500 transition-all" style={{ width: `${pct}%` }} />
      </div>
      <ol className="mt-4 space-y-1.5 text-sm">
        {SCAN_STEPS.map((label, i) => (
          <li key={label} className="flex items-center gap-2">
            <span
              className={`flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${
                i < step ? "bg-leaf-600 text-white" : i === step ? "bg-citrus-500 text-leaf-950" : "bg-gray-200 text-gray-500"
              }`}
            >
              {i < step ? "✓" : i + 1}
            </span>
            <span className={i <= step ? "font-medium text-leaf-900" : "text-gray-400"}>{label}</span>
          </li>
        ))}
      </ol>
      <p className="mt-4 rounded-lg bg-yellow-50 p-2 text-xs text-yellow-800">
        SIMULATION — the drone mission is animated; the scan results come from the real backend API.
      </p>
    </div>
  );
}
