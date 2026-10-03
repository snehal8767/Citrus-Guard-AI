// Typed API client. All requests go through here so auth + error handling
// live in one place. The Vite dev server proxies /api -> http://localhost:8000.

import type {
  AIAnalysisResult,
  Alert,
  CommandResponse,
  HistoryRecord,
  Intervention,
  LoginResponse,
  Metrics,
  Orchard,
  OrchardDetail,
  Scan,
  SensorReading,
  SensorStatus,
  Zone,
} from "../types";

const BASE = "/api";

let authToken: string | null = localStorage.getItem("cg_token");

export function setToken(token: string | null) {
  authToken = token;
  if (token) localStorage.setItem("cg_token", token);
  else localStorage.removeItem("cg_token");
}

export function getToken(): string | null {
  return authToken;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (authToken) headers["Authorization"] = `Bearer ${authToken}`;
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(`${BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    setToken(null);
    window.location.href = "/login";
    throw new Error("Session expired. Please log in again.");
  }
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (body?.detail) detail = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export const api = {
  // --- auth ---
  login: (username: string, password: string) =>
    request<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  // --- orchards ---
  listOrchards: () => request<Orchard[]>("/orchards"),
  getOrchard: (id: number) => request<OrchardDetail>(`/orchards/${id}`),

  // --- zones ---
  listZones: (orchardId?: number) =>
    request<Zone[]>(`/zones${orchardId ? `?orchard_id=${orchardId}` : ""}`),

  // --- scans ---
  listScans: (orchardId?: number) =>
    request<Scan[]>(`/scans${orchardId ? `?orchard_id=${orchardId}` : ""}`),
  runScan: (orchardId: number, scanType = "drone_simulation") =>
    request<Scan>("/scans", {
      method: "POST",
      body: JSON.stringify({ orchard_id: orchardId, scan_type: scanType }),
    }),

  // --- ai ---
  analyzeImage: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return request<AIAnalysisResult>("/ai/analyze", { method: "POST", body: fd });
  },

  // --- sensors ---
  listSensors: (zoneId?: number) =>
    request<SensorReading[]>(`/sensors${zoneId ? `?zone_id=${zoneId}` : ""}`),
  sensorStatus: () => request<SensorStatus[]>("/sensors/status"),

  // --- alerts ---
  listAlerts: (status?: string) =>
    request<Alert[]>(`/alerts${status ? `?status=${status}` : ""}`),
  verifyAlert: (id: number, decision: string, comment?: string) =>
    request<Alert>(`/alerts/${id}/verify`, {
      method: "POST",
      body: JSON.stringify({ decision, comment }),
    }),
  rejectAlert: (id: number, comment?: string) =>
    request<Alert>(`/alerts/${id}/reject`, {
      method: "POST",
      body: JSON.stringify({ decision: "reject", comment }),
    }),
  rescanAlert: (id: number, comment?: string) =>
    request<Alert>(`/alerts/${id}/rescan`, {
      method: "POST",
      body: JSON.stringify({ decision: "rescan", comment }),
    }),

  // --- interventions ---
  listInterventions: (zoneId?: number) =>
    request<Intervention[]>(`/interventions${zoneId ? `?zone_id=${zoneId}` : ""}`),
  createIntervention: (payload: {
    zone_id: number;
    intervention_type: string;
    target_area: number;
    reason?: string;
  }) =>
    request<Intervention>("/interventions", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // --- history ---
  listHistory: (orchardId?: number, zoneId?: number) => {
    const params = new URLSearchParams();
    if (orchardId) params.set("orchard_id", String(orchardId));
    if (zoneId) params.set("zone_id", String(zoneId));
    const q = params.toString();
    return request<HistoryRecord[]>(`/history${q ? `?${q}` : ""}`);
  },

  // --- metrics ---
  getMetrics: (orchardId = 1) => request<Metrics>(`/metrics?orchard_id=${orchardId}`),

  // --- commands ---
  runCommand: (command: string, orchardId = 1) =>
    request<CommandResponse>("/commands", {
      method: "POST",
      body: JSON.stringify({ command }),
      headers: { "X-Orchard-Id": String(orchardId) },
    }),
};
