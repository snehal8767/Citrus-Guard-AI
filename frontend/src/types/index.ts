// Shared TypeScript types mirroring the backend schemas.

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  username: string;
  role: string;
}

export interface Zone {
  id: number;
  orchard_id: number;
  zone_name: string;
  area: number;
  latitude: number;
  longitude: number;
  health_status: string;
  risk_score: number;
}

export interface Orchard {
  id: number;
  name: string;
  location: string | null;
  area: number;
  crop: string;
  created_at: string;
}

export interface OrchardDetail extends Orchard {
  zones: Zone[];
}

export interface AIDetection {
  id: number;
  scan_id: number;
  zone_id: number;
  condition: string;
  confidence: number;
  severity: string;
  explanation: string | null;
  timestamp: string;
}

export interface Scan {
  id: number;
  orchard_id: number;
  scan_type: string;
  timestamp: string;
  coverage: number;
  status: string;
  detections: AIDetection[];
}

export interface SensorReading {
  id: number;
  zone_id: number;
  soil_moisture: number;
  temperature: number;
  humidity: number;
  leaf_wetness: number;
  irrigation_status: string;
  timestamp: string;
}

export interface SensorStatus {
  zone_id: number;
  zone_name: string;
  soil_moisture: number;
  temperature: number;
  humidity: number;
  leaf_wetness: number;
  irrigation_status: string;
  status: string;
  last_updated: string;
}

export interface Alert {
  id: number;
  zone_id: number;
  alert_type: string;
  severity: string;
  risk_score: number;
  message: string;
  status: string;
  created_at: string;
}

export interface Intervention {
  id: number;
  zone_id: number;
  intervention_type: string;
  target_area: number;
  status: string;
  reason: string | null;
  created_at: string;
}

export interface HistoryRecord {
  id: number;
  orchard_id: number;
  zone_id: number;
  scan_id: number | null;
  health_score: number;
  risk_score: number;
  affected_area: number;
  recorded_at: string;
}

export interface Metrics {
  total_orchard_area: number;
  monitored_area: number;
  healthy_area: number;
  at_risk_area: number;
  critical_zones: number;
  active_alerts: number;
  latest_scan: string | null;
  monitoring_coverage: number;
  sensor_health: number;
}

export interface CommandResponse {
  intent: string;
  message: string;
  data: Record<string, unknown> | unknown[] | null;
}

export interface AIAnalysisResult {
  id?: number;
  condition: string;
  confidence: number;
  severity: string;
  explanation: string;
  next_step: string;
  model_type: string;
  filename?: string;
}

export interface AIAnalysisRecord {
  id: number;
  filename: string;
  condition: string;
  confidence: number;
  severity: string;
  explanation: string | null;
  next_step: string | null;
  model_type: string;
  created_at: string;
}

export interface ZoneRecommendation {
  zone_id: number;
  zone_name: string;
  health_status: string;
  risk_score: number;
  area: number;
  condition: string;
  severity: string;
  risk: number;
  affected_area: number;
  alert_id: number | null;
  alert_status: string | null;
  verified_alert: boolean;
  steps: string[];
  safety_note: string;
}
