// Leaflet GIS map: orchard zones coloured by health status.
// Zone geometry comes from the backend (lat/lon centers); polygons are drawn
// as rectangles matching the seeded 4x2 grid layout.
import { useEffect } from "react";
import { MapContainer, Polygon, Popup, TileLayer, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { Zone } from "../types";
import { zoneColor } from "../utils/helpers";

const LAT_STEP = 0.0045;
const LON_STEP = 0.0052;

function FitBounds({ zones }: { zones: Zone[] }) {
  const map = useMap();
  useEffect(() => {
    if (zones.length === 0) return;
    const lats = zones.map((z) => z.latitude);
    const lons = zones.map((z) => z.longitude);
    map.fitBounds(
      [
        [Math.min(...lats) - LAT_STEP, Math.min(...lons) - LON_STEP],
        [Math.max(...lats) + LAT_STEP, Math.max(...lons) + LON_STEP],
      ],
      { padding: [20, 20] }
    );
  }, [zones, map]);
  return null;
}

function zonePolygon(z: Zone): [number, number][] {
  const dlat = (LAT_STEP / 2) * 0.9;
  const dlon = (LON_STEP / 2) * 0.9;
  return [
    [z.latitude - dlat, z.longitude - dlon],
    [z.latitude - dlat, z.longitude + dlon],
    [z.latitude + dlat, z.longitude + dlon],
    [z.latitude + dlat, z.longitude - dlon],
  ];
}

export default function ZoneMap({
  zones,
  selected,
  onSelect,
}: {
  zones: Zone[];
  selected?: string | null;
  onSelect?: (zoneName: string) => void;
}) {
  if (zones.length === 0) return null;
  const center: [number, number] = [
    zones.reduce((s, z) => s + z.latitude, 0) / zones.length,
    zones.reduce((s, z) => s + z.longitude, 0) / zones.length,
  ];

  return (
    <div data-testid="zone-map" className="overflow-hidden rounded-xl border border-leaf-100">
      <MapContainer center={center} zoom={14} style={{ height: 420, width: "100%" }} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <FitBounds zones={zones} />
        {zones.map((z) => (
          <Polygon
            key={z.id}
            positions={zonePolygon(z)}
            pathOptions={{
              color: selected === z.zone_name ? "#1f3b1d" : zoneColor(z.health_status),
              weight: selected === z.zone_name ? 3 : 2,
              fillColor: zoneColor(z.health_status),
              fillOpacity: 0.45,
            }}
            eventHandlers={{ click: () => onSelect?.(z.zone_name) }}
          >
            <Popup>
              <div className="text-sm">
                <div className="font-bold">Zone {z.zone_name}</div>
                <div>Health: {z.health_status}</div>
                <div>Risk: {z.risk_score}/100</div>
                <div>Area: {z.area.toFixed(2)} ac</div>
              </div>
            </Popup>
          </Polygon>
        ))}
      </MapContainer>
    </div>
  );
}
