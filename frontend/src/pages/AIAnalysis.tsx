// AI Image Analysis page: upload -> preview -> analyze -> results.
// Every analysis is saved to the database; past analyses are listed below.
import { useState } from "react";
import { api } from "../api/client";
import type { AIAnalysisResult } from "../types";
import { PageHeader, StatusBadge } from "../components/ui";
import { EmptyState, ErrorAlert, LoadingSpinner } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime, formatNumber } from "../utils/helpers";

export default function AIAnalysis() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AIAnalysisResult | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const past = useApi(() => api.listAnalyses());

  const onFile = (f: File | undefined) => {
    setResult(null);
    setError(null);
    if (!f) {
      setFile(null);
      setPreview(null);
      return;
    }
    setFile(f);
    setPreview(URL.createObjectURL(f));
  };

  const analyze = async () => {
    if (!file) return;
    setBusy(true);
    setError(null);
    try {
      const res = await api.analyzeImage(file);
      setResult(res);
      past.refresh(); // new analysis is now recorded — reload the history list
    } catch (e) {
      setError(e instanceof Error ? e.message : "Analysis failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <PageHeader title="AI Image Analysis" subtitle="Upload a leaf/canopy photo. It runs the real OpenCV + scikit-learn pipeline. Demo model trained on synthetic data — not field-validated." />
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <div className="section-title">Upload</div>
          <input
            type="file"
            accept="image/*"
            data-testid="image-input"
            className="mt-3 block w-full text-sm"
            onChange={(e) => onFile(e.target.files?.[0])}
          />
          {preview && <img src={preview} alt="Upload preview" className="mt-4 max-h-72 rounded-lg border" />}
          <button className="btn-primary mt-4" onClick={analyze} disabled={!file || busy} data-testid="analyze-btn">
            {busy ? "Analyzing…" : "Analyze image"}
          </button>
          {error && <div className="mt-3 rounded-lg bg-red-50 p-2 text-sm text-red-700">{error}</div>}
        </div>
        <div className="card" data-testid="analysis-result">
          <div className="section-title">Result</div>
          {!result ? (
            <p className="mt-2 text-sm text-gray-500">No analysis yet. Upload an image and click Analyze.</p>
          ) : (
            <dl className="mt-3 space-y-2 text-sm">
              <div className="flex justify-between"><dt className="text-gray-500">Condition</dt><dd className="font-bold">{result.condition}</dd></div>
              <div className="flex justify-between"><dt className="text-gray-500">Confidence</dt><dd className="font-bold">{formatNumber(result.confidence)}%</dd></div>
              <div className="flex justify-between"><dt className="text-gray-500">Severity</dt><dd><StatusBadge status={result.severity} /></dd></div>
              <div><dt className="text-gray-500">Explanation</dt><dd className="mt-1 rounded-lg bg-leaf-50 p-2">{result.explanation}</dd></div>
              <div><dt className="text-gray-500">Next step</dt><dd className="mt-1 rounded-lg bg-citrus-50 p-2 font-medium">{result.next_step}</dd></div>
              <div className="text-xs text-gray-400">model: {result.model_type} (synthetic demo)</div>
            </dl>
          )}
        </div>
      </div>

      <div className="card mt-6">
        <div className="section-title">Past analyses (recorded in database)</div>
        <p className="mt-1 text-xs text-gray-500">Every uploaded image is saved with its result. Newest first.</p>
        {past.loading ? (
          <LoadingSpinner />
        ) : past.error ? (
          <ErrorAlert message={past.error} onRetry={past.refresh} />
        ) : !past.data || past.data.length === 0 ? (
          <div className="mt-3"><EmptyState message="No analyses yet. Upload an image above." /></div>
        ) : (
          <ul className="mt-3 max-h-72 space-y-2 overflow-y-auto text-sm">
            {past.data.slice(0, 20).map((a) => (
              <li key={a.id} className="flex flex-wrap items-center justify-between gap-2 rounded-lg bg-leaf-50 px-3 py-2" data-testid={`past-analysis-${a.id}`}>
                <span className="font-medium">#{a.id} · {a.filename}</span>
                <span>{a.condition} · {formatNumber(a.confidence)}%</span>
                <span className="flex items-center gap-2">
                  <StatusBadge status={a.severity} />
                  <span className="text-xs text-gray-400">{formatDateTime(a.created_at)}</span>
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
