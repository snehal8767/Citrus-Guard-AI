// GIS Map page: Leaflet orchard map + zone detail panel.
import { useState } from "react";
import { api } from "../api/client";
import ZoneMap from "../components/ZoneMap";
import { EmptyState, ErrorAlert, LoadingSpinner, PageHeader, StatusBadge } from "../components/ui";
import { useApi } from "../hooks/useApi";
import { formatNumber } from "../utils/helpers";

export default function MapPage() {
  const zones = useApi(() => api.listZones(1));
  const sensors = useApi(() => api.sensorStatus());
  const [selected, setSelected] = useState<string | null>("B");

  const zone = zones.data?.find((z) => z.zone_name === selected);
  const sensor = sensors.data?.find((s) => s.zone_name === selected);

  return (
    <div>
      <PageHeader title="GIS Orchard Map" subtitle="8 zones (A–H) coloured by health status. Click a zone for details. Base map: OpenStreetMap." />
      {zones.loading ? (
        <LoadingSpinner text="Loading zones…" />
      ) : zones.error ? (
        <ErrorAlert message={zones.error} onRetry={zones.refresh} />
      ) : !zones.data || zones.data.length === 0 ? (
        <EmptyState message="No zones found." />
      ) : (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <ZoneMap zones={zones.data} selected={selected} onSelect={setSelected} />
            <div className="mt-3 flex flex-wrap gap-2 text-xs">
              {["Healthy", "Watch", "At Risk", "Critical"].map((s) => (
                <span key={s} className="flex items-center gap-1.5 rounded-full bg-white px-2.5 py-1 shadow-sm">
                  <span className="inline-block h-3 w-3 rounded-full" style={{ background: s === "Healthy" ? "#4a8d3e" : s === "Watch" ? "#eab308" : s === "At Risk" ? "#f98707" : "#dc2626" }} />
                  {s}
                </span>
              ))}
            </div>
          </div>
          <div className="card">
            <div className="section-title">Zone detail</div>
            {!zone ? (
              <p className="mt-2 text-sm text-gray-500">Click a zone on the map.</p>
            ) : (
              <dl className="mt-3 space-y-2 text-sm">
                <div className="flex justify-between"><dt className="text-gray-500">Zone</dt><dd className="font-bold">{zone.zone_name}</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Crop health</dt><dd><StatusBadge status={zone.health_status} /></dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Risk score</dt><dd className="font-bold">{formatNumber(zone.risk_score)}/100</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Area</dt><dd>{formatNumber(zone.area, 2)} ac</dd></div>
                <div className="flex justify-between"><dt className="text-gray-500">Center</dt><dd className="text-xs">{zone.latitude.toFixed(4)}, {zone.longitude.toFixed(4)}</dd></div>
                {sensor && (
                  <>
                    <div className="flex justify-between"><dt className="text-gray-500">Sensor status</dt><dd><StatusBadge status={sensor.status} /></dd></div>
                    <div className="flex justify-between"><dt className="text-gray-500">Leaf wetness</dt><dd>{formatNumber(sensor.leaf_wetness)}%</dd></div>
                    <div className="flex justify-between"><dt className="text-gray-500">Humidity</dt><dd>{formatNumber(sensor.humidity)}%</dd></div>
                    <div className="flex justify-between"><dt className="text-gray-500">Soil moisture</dt><dd>{formatNumber(sensor.soil_moisture)}%</dd></div>
                  </>
                )}
                <div className="rounded-lg bg-leaf-50 p-2 text-xs text-leaf-800">
                  {zone.zone_name === "B"
                    ? "Recommended action: verify affected trees before intervention. (Deterministic demo: Zone B flags disease stress at risk 82/100.)"
                    : "Recommended action: continue routine monitoring."}
                </div>
              </dl>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
