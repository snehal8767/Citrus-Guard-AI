import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import Dashboard from "../pages/Dashboard";

vi.mock("../api/client", () => ({
  api: {
    getMetrics: vi.fn(),
    listHistory: vi.fn(),
    listAlerts: vi.fn(),
    runScan: vi.fn(),
  },
  getToken: () => "test-token",
  setToken: () => {},
}));

const mocked = vi.mocked(api, true);

describe("Dashboard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocked.getMetrics.mockResolvedValue({
      total_orchard_area: 50.0,
      monitored_area: 50.0,
      healthy_area: 43.75,
      at_risk_area: 6.25,
      critical_zones: 1,
      active_alerts: 1,
      latest_scan: "2026-10-04T10:00:00Z",
      monitoring_coverage: 100.0,
      sensor_health: 87.5,
    });
    mocked.listHistory.mockResolvedValue([]);
    mocked.listAlerts.mockResolvedValue([]);
  });

  it("renders KPIs from the metrics API", async () => {
    render(<Dashboard />);
    await waitFor(() => expect(mocked.getMetrics).toHaveBeenCalled());
    // Total + monitored areas are both "50.0 ac"
    expect(await screen.findAllByText("50.0 ac")).toHaveLength(2);
    expect(screen.getByText("Total Orchard Area")).toBeInTheDocument();
    expect(screen.getByText("Active Alerts")).toBeInTheDocument();
  });

  it("RUN ORCHARD SCAN calls the real scan endpoint and refreshes", async () => {
    mocked.runScan.mockResolvedValue({
      id: 1, orchard_id: 1, scan_type: "drone_simulation",
      timestamp: "2026-10-04T10:00:00Z", coverage: 99.0,
      status: "Completed", detections: [],
    });
    render(<Dashboard />);
    const btn = await screen.findByTestId("run-scan");
    fireEvent.click(btn);
    await waitFor(() => expect(mocked.runScan).toHaveBeenCalledWith(1));
    // metrics refreshed after scan
    await waitFor(() => expect(mocked.getMetrics.mock.calls.length).toBeGreaterThan(1));
  });

  it("shows an error when the API fails", async () => {
    mocked.getMetrics.mockRejectedValue(new Error("backend down"));
    render(<Dashboard />);
    expect(await screen.findByText("backend down")).toBeInTheDocument();
  });
});
