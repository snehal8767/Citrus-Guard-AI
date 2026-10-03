import { describe, expect, it } from "vitest";
import { badgeClass, formatDateTime, formatNumber, zoneColor } from "../utils/helpers";

describe("helpers", () => {
  it("maps health statuses to badge classes", () => {
    expect(badgeClass("Healthy")).toContain("badge-healthy");
    expect(badgeClass("Critical")).toContain("badge-critical");
    expect(badgeClass("At Risk")).toContain("badge-at-risk");
    expect(badgeClass("Watch")).toContain("badge-watch");
    expect(badgeClass("SomethingElse")).toContain("badge-default");
  });

  it("maps alert workflow states to badge classes", () => {
    expect(badgeClass("Verified")).toContain("badge-healthy");
    expect(badgeClass("New")).toContain("badge-watch");
    expect(badgeClass("Rejected")).toContain("badge-critical");
  });

  it("colors zones by health status", () => {
    expect(zoneColor("Healthy")).toBe("#4a8d3e");
    expect(zoneColor("Critical")).toBe("#dc2626");
    expect(zoneColor("Unknown")).toBe("#6b7280");
  });

  it("formats datetimes and numbers safely", () => {
    expect(formatDateTime(null)).toBe("—");
    expect(formatDateTime("not-a-date")).toBe("—");
    expect(formatDateTime("2026-10-01T10:00:00Z")).not.toBe("—");
    expect(formatNumber(82.0)).toBe("82.0");
    expect(formatNumber(null)).toBe("—");
  });
});
