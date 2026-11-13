import { defineTheme } from 'pinceau'

// Tailwind `primary-*` follows the park palette in assets/css/park.css so any
// Content Wind default that reaches for `primary` comes out hemlock, not the
// old emerald. 50 = --fern, 100 = --rule, 200 = --on-dark-soft,
// 800 = --hemlock, 900 = --hemlock-deep; 300–700 are even steps between
// --fern and --hemlock. No site component uses primary-* directly today.
export default defineTheme({
  color: {
    primary: {
      50: '#eef3ec',
      100: '#d5ddd3',
      200: '#b9c9bd',
      300: '#91a096',
      400: '#72847a',
      500: '#596e63',
      600: '#40584c',
      700: '#2d473b',
      800: '#1f3a2e',
      900: '#162b22',
    }
  }
})
