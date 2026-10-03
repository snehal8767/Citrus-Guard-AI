import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ZoneMap from "../components/ZoneMap";
import type { Zone } from "../types";

// Leaflet needs a real browser; stub react-leaflet for unit tests.
vi.mock("react-leaflet", () => ({
  MapContainer: ({ children }: { children: React.ReactNode }) => <div data-testid="leaflet-map">{children}</div>,
  TileLayer: () => null,
  Polygon: ({ children, eventHandlers }: { children: React.ReactNode; eventHandlers?: { click?: () => void } }) => (
    <div data-testid="zone-polygon" onClick={eventHandlers?.click}>{children}</div>
  ),
  Popup: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  useMap: () => ({ fitBounds: vi.fn() }),
}));

const ZONES: Zone[] = (["A", "B"] as const).map((n, i) => ({
  id: i + 1,
  orchard_id: 1,
  zone_name: n,
  area: 6.25,
  latitude: 21.14 + i * 0.004,
  longitude: 79.08 + i * 0.005,
  health_status: n === "B" ? "Critical" : "Healthy",
  risk_score: n === "B" ? 82 : 10,
}));

describe("ZoneMap", () => {
  it("renders a polygon per zone and reports clicks", () => {
    const onSelect = vi.fn();
    render(<ZoneMap zones={ZONES} selected={null} onSelect={onSelect} />);
    expect(screen.getByTestId("zone-map")).toBeInTheDocument();
    expect(screen.getAllByTestId("zone-polygon")).toHaveLength(2);
    fireEvent.click(screen.getAllByTestId("zone-polygon")[1]);
    expect(onSelect).toHaveBeenCalledWith("B");
  });

  it("shows zone health in popups", () => {
    render(<ZoneMap zones={ZONES} />);
    expect(screen.getByText(/Critical/)).toBeInTheDocument();
    expect(screen.getByText(/82\/100/)).toBeInTheDocument();
  });
});
