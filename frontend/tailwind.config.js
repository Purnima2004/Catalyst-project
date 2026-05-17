/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#131313',
        primaryText: '#F0F0F0',
        accent1: '#14c2ed',
        accent2: '#ff6abc',
        cta: '#405843'
      }
    },
  },
  plugins: [],
}
