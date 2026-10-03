import "@testing-library/jest-dom";

// jsdom does not implement URL.createObjectURL — stub it for upload-preview tests.
if (typeof URL.createObjectURL !== "function") {
  URL.createObjectURL = () => "blob:mock-preview-url";
}
