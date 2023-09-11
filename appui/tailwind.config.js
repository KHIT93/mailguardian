const colors = require('tailwindcss/colors')

module.exports = {
    content: [
        '../src/**/templates/**/*.html',
        'components/**/*.{vue,js,ts}',
        'layouts/**/*.{vue,js,ts}',
        'pages/**/*.{vue,js,ts}',
        'composables/**/*.{vue,js,ts}',
        'plugins/**/*.{vue,js,ts}',
        `App.{js,ts,vue}`,
        `app.{js,ts,vue}`
    ],
    theme: {
        extend: {
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
    plugins: [
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ],
}
