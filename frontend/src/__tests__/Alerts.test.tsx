import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import Alerts from "../pages/Alerts";

vi.mock("../api/client", () => ({
  api: {
    listAlerts: vi.fn(),
    verifyAlert: vi.fn(),
    rejectAlert: vi.fn(),
    rescanAlert: vi.fn(),
  },
  getToken: () => "test-token",
  setToken: () => {},
}));

const mocked = vi.mocked(api, true);

const ALERT = {
  id: 1, zone_id: 2, alert_type: "Disease Risk", severity: "High",
  risk_score: 82.0, message: "Zone B disease stress", status: "New",
  created_at: "2026-10-04T10:00:00Z",
};

describe("Alert Center", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocked.listAlerts.mockResolvedValue([ALERT]);
  });

  it("lists alerts with human-in-the-loop buttons", async () => {
    render(<Alerts />);
    expect(await screen.findByTestId("alert-1")).toBeInTheDocument();
    expect(screen.getByTestId("verify-1")).toHaveTextContent("VERIFY");
    expect(screen.getByText("REJECT")).toBeInTheDocument();
    expect(screen.getByText("REQUEST RESCAN")).toBeInTheDocument();
  });

  it("VERIFY calls the verify endpoint", async () => {
    mocked.verifyAlert.mockResolvedValue({ ...ALERT, status: "Verified" });
    render(<Alerts />);
    fireEvent.click(await screen.findByTestId("verify-1"));
    await waitFor(() => expect(mocked.verifyAlert).toHaveBeenCalledWith(1, "verify", undefined));
  });

  it("shows an empty state when there are no alerts", async () => {
    mocked.listAlerts.mockResolvedValue([]);
    render(<Alerts />);
    expect(await screen.findByText(/No alerts/)).toBeInTheDocument();
  });
});
