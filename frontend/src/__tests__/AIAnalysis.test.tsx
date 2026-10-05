import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import AIAnalysis from "../pages/AIAnalysis";

vi.mock("../api/client", () => ({
  api: { analyzeImage: vi.fn(), listAnalyses: vi.fn() },
  getToken: () => "test-token",
  setToken: () => {},
}));

const mocked = vi.mocked(api, true);

describe("AIAnalysis", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocked.listAnalyses.mockResolvedValue([]);
  });

  it("uploads, analyzes and shows condition/confidence/severity", async () => {
    mocked.analyzeImage.mockResolvedValue({
      condition: "Healthy",
      confidence: 94.2,
      severity: "Low",
      explanation: "Canopy looks healthy.",
      next_step: "Continue routine monitoring.",
      model_type: "synthetic_demo_rf",
    });
    render(<AIAnalysis />);
    const file = new File(["fake-image"], "leaf.jpg", { type: "image/jpeg" });
    fireEvent.change(screen.getByTestId("image-input"), { target: { files: [file] } });
    fireEvent.click(screen.getByTestId("analyze-btn"));
    await waitFor(() => expect(mocked.analyzeImage).toHaveBeenCalled());
    expect(await screen.findByText("Healthy")).toBeInTheDocument();
    expect(screen.getByText("94.2%")).toBeInTheDocument();
  });

  it("lists past recorded analyses", async () => {
    mocked.listAnalyses.mockResolvedValue([
      {
        id: 7, filename: "leaf.jpg", condition: "Healthy", confidence: 94.2,
        severity: "Low", explanation: "ok", next_step: "monitor",
        model_type: "synthetic_demo_rf", created_at: "2026-10-05T10:00:00Z",
      },
    ]);
    render(<AIAnalysis />);
    expect(await screen.findByTestId("past-analysis-7")).toBeInTheDocument();
    expect(screen.getByText(/leaf.jpg/)).toBeInTheDocument();
  });

  it("shows backend errors", async () => {
    mocked.analyzeImage.mockRejectedValue(new Error("Invalid image type"));
    render(<AIAnalysis />);
    const file = new File(["x"], "x.txt", { type: "text/plain" });
    fireEvent.change(screen.getByTestId("image-input"), { target: { files: [file] } });
    fireEvent.click(screen.getByTestId("analyze-btn"));
    expect(await screen.findByText("Invalid image type")).toBeInTheDocument();
  });
});
