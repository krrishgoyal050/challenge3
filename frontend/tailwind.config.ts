import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#f7f8f5",
        foreground: "#18201c",
        primary: "#236b4b",
        accent: "#386fa4",
        warning: "#b7791f",
        panel: "#ffffff",
        line: "#d9e2da"
      },
      boxShadow: {
        soft: "0 8px 24px rgba(24,32,28,0.08)"
      }
    }
  },
  plugins: []
};

export default config;
