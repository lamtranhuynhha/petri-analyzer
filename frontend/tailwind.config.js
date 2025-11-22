/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        canvas: {
          bg: '#f8fafc',
          grid: '#e2e8f0',
        },
        place: {
          default: '#ffffff',
          selected: '#dbeafe',
          hover: '#f1f5f9',
          border: '#64748b',
        },
        transition: {
          default: '#1e293b',
          enabled: '#10b981',
          disabled: '#94a3b8',
          selected: '#3b82f6',
          dead: '#9ca3af',
          l1: '#93c5fd',
          l3: '#fb923c',
          live: '#22c55e',
        }
      },
      spacing: {
        'toolbar': '80px',
        'topbar': '60px',
        'sidebar': '320px',
      },
      zIndex: {
        'toolbar': '10',
        'topbar': '20',
        'sidebar': '10',
        'modal': '50',
        'toast': '100',
      }
    },
  },
  plugins: [],
}


