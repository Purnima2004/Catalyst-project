/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
        serif: ['Fraunces', 'serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      colors: {
        background: '#07080e',
        primaryText: '#F8FAFC',
        accent1: '#3b82f6',     // Premium Ice Blue
        accent2: '#f59e0b',     // Refined Amber/Gold
        cta: '#10b981',         // Pristine Emerald / Mint
        panel: '#0f121d',       // Sleek Graphite Panel
        'panel-hover': '#151928',
        'border-subtle': 'rgba(255,255,255,0.06)',
        'text-muted': '#94a3b8',
      },
      animation: {
        blob: "blob 10s infinite",
      },
      keyframes: {
        blob: {
          "0%": { transform: "translate(0px, 0px) scale(1)" },
          "33%": { transform: "translate(30px, -50px) scale(1.05)" },
          "66%": { transform: "translate(-20px, 20px) scale(0.95)" },
          "100%": { transform: "translate(0px, 0px) scale(1)" },
        },
      }
    },
  },
  plugins: [],
}
