/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        leaf: {
          50: "#f2f8f0",
          100: "#e0efdb",
          200: "#c2dfba",
          300: "#97c78d",
          400: "#6aab5f",
          500: "#4a8d3e",
          600: "#37712e",
          700: "#2c5a26",
          800: "#264822",
          900: "#1f3b1d",
          950: "#0e200d",
        },
        citrus: {
          50: "#fff8eb",
          100: "#ffefc6",
          200: "#ffdd88",
          300: "#ffc44a",
          400: "#ffab1f",
          500: "#f98707",
          600: "#dd6502",
          700: "#b74506",
          800: "#94360c",
          900: "#7a2d0d",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "Segoe UI", "Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
};
