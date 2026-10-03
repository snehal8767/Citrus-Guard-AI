import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { api } from "../api/client";
import CommandConsole from "../components/CommandConsole";

vi.mock("../api/client", () => ({
  api: { runCommand: vi.fn() },
  getToken: () => "test-token",
  setToken: () => {},
}));

const mocked = vi.mocked(api, true);

describe("CommandConsole", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("sends a command and shows the real backend response", async () => {
    mocked.runCommand.mockResolvedValue({
      intent: "zone_risk",
      message: "Zone B: health=Critical, risk=82.0/100.",
      data: { zone_name: "B" },
    });
    render(<CommandConsole />);
    const input = screen.getByPlaceholderText(/Type a command/i);
    fireEvent.change(input, { target: { value: "show zone B risk" } });
    fireEvent.click(screen.getByText("Send"));
    await waitFor(() => expect(mocked.runCommand).toHaveBeenCalledWith("show zone B risk", 1));
    expect(await screen.findByText(/Zone B: health=Critical/)).toBeInTheDocument();
  });

  it("states it is not an LLM", () => {
    render(<CommandConsole />);
    expect(screen.getByText(/not.*an LLM/i)).toBeInTheDocument();
  });
});
