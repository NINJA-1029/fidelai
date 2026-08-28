import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      maxWidth: {
        container: "1078px",
      },
      borderRadius: {
        none: "0px",
        sm: "0px",
        md: "0px",
        lg: "0px",
        xl: "0px",
        "2xl": "0px",
        full: "75.024px",
        pill: "75px",
      },
      colors: {
        obsidian: "#000000",
        paper: "#ffffff",
        inkstone: "#181818",
        "felt-gray": "#6d6d6d",
        "slate-pill": "#636363",
        "ash-mist": "#9a9a9a",
        pewter: "#808080",
        border: "var(--border)",
        input: "var(--input)",
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
        },
        muted: {
          DEFAULT: "var(--muted)",
          foreground: "var(--muted-foreground)",
        },
        card: {
          DEFAULT: "var(--card)",
          foreground: "var(--card-foreground)",
        },
      },
      fontFamily: {
        roobert: ["var(--font-roobert)", "Inter", "system-ui", "sans-serif"],
        raleway: ["var(--font-raleway)", "Raleway", "sans-serif"],
      },
      transitionTimingFunction: {
        patient: "cubic-bezier(0.19, 1, 0.22, 1)",
      },
      transitionDuration: {
        patient: "1250ms",
        smooth: "800ms",
      },
    },
  },
  plugins: [],
};

export default config;
