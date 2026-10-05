import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import Interventions from "../pages/Interventions";

vi.mock("../api/client", () => ({
  api: {
    listZones: vi.fn(),
    listAlerts: vi.fn(),
    listInterventions: vi.fn(),
    getRecommendation: vi.fn(),
    createIntervention: vi.fn(),
  },
  getToken: () => "test-token",
  setToken: () => {},
}));

const mocked = vi.mocked(api, true);

describe("Interventions recommendation card", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocked.listZones.mockResolvedValue([
      { id: 2, orchard_id: 1, zone_name: "B", area: 6.25, latitude: 21.14, longitude: 79.08, health_status: "Critical", risk_score: 82 },
    ]);
    mocked.listAlerts.mockResolvedValue([]);
    mocked.listInterventions.mockResolvedValue([]);
    mocked.getRecommendation.mockResolvedValue({
      zone_id: 2, zone_name: "B", health_status: "Critical", risk_score: 82, area: 6.25,
      condition: "Possible Citrus Disease Stress", severity: "High", risk: 82,
      affected_area: 2.94, alert_id: 1, alert_status: "New", verified_alert: false,
      steps: [
        "Step 1: Inspect affected trees and confirm the suspected condition.",
        "Step 2: If confirmed, consult your local agricultural advisory for approved treatment options.",
        "Step 3: Generate a targeted intervention map for the affected area only.",
        "Step 4: Apply the approved treatment only to the verified affected zone.",
        "Step 5: Re-scan the zone after intervention to confirm recovery.",
      ],
      safety_note: "Important: this system does not prescribe pesticides, doses, or chemicals.",
    });
  });

  it("shows the structured recommendation in the requested format", async () => {
    render(<Interventions />);
    expect(await screen.findByTestId("recommendation-card")).toBeInTheDocument();
    expect(await screen.findByText("Zone B — Critical")).toBeInTheDocument();
    expect(screen.getByText("Possible Citrus Disease Stress")).toBeInTheDocument();
    expect(screen.getByText("82.0/100")).toBeInTheDocument();
    expect(screen.getByText("2.94 acres")).toBeInTheDocument();
    expect(screen.getByText("Recommended action")).toBeInTheDocument();
    expect(screen.getByText(/Step 1: Inspect affected trees/)).toBeInTheDocument();
    expect(screen.getByText(/does not prescribe pesticides/)).toBeInTheDocument();
  });
});
