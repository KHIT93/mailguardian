const colors = require('tailwindcss/colors')

module.exports = {
  purge: [
    '../templates/**/*.html',
    '../../**/templates/**/*.html',
    './**/*.{vue,js,ts,jsx,tsx}'
  ],
  mode: 'jit',
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'blue-gray': colors.blueGray,
        'cool-gray': colors.coolGray,
        'true-gray': colors.trueGray,
        'warm-gray': colors.warmGray,
        'orange': colors.orange,
        'amber': colors.amber,
        'lime': colors.lime,
        'emerald': colors.emerald,
        'teal': colors.teal,
        'light-blue': colors.sky,
        'violet': colors.violet,
        'fuchsia': colors.fuchsia,
        'rose': colors.rose
      },
      fontFamily: {
        'sans': ["Roboto", "ui-sans-serif", "system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Helvetica Neue", "Arial", "Noto Sans", "sans-serif", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"]
      },
      keyframes: {
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' }
        }
      },
      animation: {
        wiggle: 'wiggle 1s ease-in-out infinite'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/typography'),
  ],
}
