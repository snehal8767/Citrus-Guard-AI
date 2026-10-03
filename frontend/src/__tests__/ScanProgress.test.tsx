import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import ScanProgress, { SCAN_STEPS } from "../components/ScanProgress";

describe("ScanProgress", () => {
  it("renders all 12 scan steps", () => {
    expect(SCAN_STEPS).toHaveLength(12);
    render(<ScanProgress />);
    for (const step of SCAN_STEPS) {
      expect(screen.getByText(step)).toBeInTheDocument();
    }
    expect(screen.getByTestId("scan-progress")).toBeInTheDocument();
  });

  it("labels the mission as a simulation", () => {
    render(<ScanProgress />);
    expect(screen.getByText(/SIMULATION/i)).toBeInTheDocument();
  });
});
