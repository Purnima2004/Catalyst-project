/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
      colors: {
        background: '#f7f6f3',
        surface: '#ffffff',
        ink: '#1c1917',
        'ink-muted': '#57534e',
        'ink-faint': '#a8a29e',
        border: '#e7e5e4',
        'border-strong': '#d6d3d1',
        accent: '#1d4ed8',
        'accent-soft': '#eff6ff',
        success: '#15803d',
        'success-soft': '#f0fdf4',
        warn: '#b45309',
        'warn-soft': '#fffbeb',
      },
      boxShadow: {
        card: '0 1px 2px rgba(28, 25, 23, 0.04), 0 4px 16px rgba(28, 25, 23, 0.06)',
        lift: '0 2px 8px rgba(28, 25, 23, 0.08), 0 12px 32px rgba(28, 25, 23, 0.06)',
      },
    },
  },
  plugins: [],
}
