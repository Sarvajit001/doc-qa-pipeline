/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#14161C",
        panel: "#1B1E27",
        panel2: "#20232E",
        border: "#2B2F3B",
        paper: "#ECEFF3",
        paperMuted: "#D8DDE4",
        textHi: "#F1EDE4",
        textLo: "#9AA1AE",
        teal: {
          DEFAULT: "#2FA8A0",
          soft: "#1F6B66",
        },
        amber: {
          DEFAULT: "#E8A33D",
          soft: "#8C6423",
        },
        rose: {
          DEFAULT: "#E2635B",
          soft: "#8C3D38",
        },
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
      },
      borderRadius: {
        sm: "6px",
        md: "10px",
        lg: "14px",
      },
      keyframes: {
        rise: {
          "0%": { opacity: 0, transform: "translateY(6px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        blink: {
          "0%, 80%, 100%": { opacity: 0.25 },
          "40%": { opacity: 1 },
        },
      },
      animation: {
        rise: "rise 0.25s ease-out",
        blink: "blink 1.4s infinite ease-in-out",
      },
    },
  },
  plugins: [],
};
