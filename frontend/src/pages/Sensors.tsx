// Sensors page: current values, normal ranges, status, trend, last updated.
import { useState } from "react";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../api/client";
import { EmptyState, ErrorAlert, LoadingSpinner, PageHeader, StatusBadge } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatDateTime, formatNumber } from "../utils/helpers";

const NORMAL = {
  soil_moisture: "25–45%",
  temperature: "20–35°C",
  humidity: "40–75%",
  leaf_wetness: "≤40%",
};

export default function Sensors() {
  const status = useApi(() => api.sensorStatus());
  const [zoneId, setZoneId] = useState<number | undefined>(undefined);
  const readings = useApi(() => api.listSensors(zoneId), [zoneId]);

  const trend = (readings.data ?? []).slice(0, 30).reverse().map((r) => ({
    t: new Date(r.timestamp).toLocaleDateString(),
    soil: r.soil_moisture,
    temp: r.temperature,
    humidity: r.humidity,
    wetness: r.leaf_wetness,
  }));

  return (
    <div>
      <PageHeader title="Sensor Network" subtitle="IoT soil + microclimate readings per zone (simulated sensor feed stored in the database)." />
      {status.loading ? (
        <LoadingSpinner />
      ) : status.error ? (
        <ErrorAlert message={status.error} onRetry={status.refresh} />
      ) : !status.data || status.data.length === 0 ? (
        <EmptyState message="No sensor data." />
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {status.data.map((s) => (
            <div key={s.zone_id} className="card" data-testid={`sensor-zone-${s.zone_name}`}>
              <div className="flex items-center justify-between">
                <span className="font-bold text-leaf-900">Zone {s.zone_name}</span>
                <StatusBadge status={s.status} />
              </div>
              <dl className="mt-2 space-y-1 text-sm">
                <div className="flex justify-between"><dt className="text-gray-500">Soil moisture</dt><dd>{formatNumber(s.soil_moisture)}% <span className="text-xs text-gray-400">({NORMAL.soil_moisture})</span></dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Temperature</dt><dd>{formatNumber(s.temperature)}°C <span className="text-xs text-gray-400">({NORMAL.temperature})</span></dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Humidity</dt><dd>{formatNumber(s.humidity)}% <span className="text-xs text-gray-400">({NORMAL.humidity})</span></dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Leaf wetness</dt><dd>{formatNumber(s.leaf_wetness)}% <span className="text-xs text-gray-400">({NORMAL.leaf_wetness})</span></dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Irrigation</dt><dd>{s.irrigation_status}</dd></div>
              </dl>
              <div className="mt-2 text-xs text-gray-400">Updated: {formatDateTime(s.last_updated)}</div>
              <button className="btn-secondary mt-2 w-full" onClick={() => setZoneId(s.zone_id)}>View trend</button>
            </div>
          ))}
        </div>
      )}

      <div className="card mt-6">
        <div className="section-title">Sensor trend {zoneId ? `(zone ${zoneId})` : "(latest 30 readings)"}</div>
        {readings.loading ? (
          <LoadingSpinner />
        ) : readings.error ? (
          <ErrorAlert message={readings.error} onRetry={readings.refresh} />
        ) : trend.length === 0 ? (
          <EmptyState message="No readings." />
        ) : (
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="t" fontSize={11} />
              <YAxis fontSize={11} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="soil" stroke="#4a8d3e" name="Soil %" dot={false} />
              <Line type="monotone" dataKey="temp" stroke="#dc2626" name="Temp °C" dot={false} />
              <Line type="monotone" dataKey="humidity" stroke="#2563eb" name="Humidity %" dot={false} />
              <Line type="monotone" dataKey="wetness" stroke="#f98707" name="Leaf wet %" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
