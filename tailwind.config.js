module.exports = {
    // mode: 'jit',
    purge: [
        './assets/src/js/**/*.js',
        './assets/src/js/**/*.vue',
        './src/**/*.html'
    ],
    theme: {
        extend: {
            container: {
                center: true,
                padding: '2rem',
            }
        }
        // customForms: theme => ({
        //     default: {
        //         select: {
        //             backgroundColor: theme('colors.cool-gray.200'),
        //             borderColor: theme('colors.cool-gray.200'),
        //             paddingLeft: theme('spacing.4'),
        //             paddingRight: theme('spacing.4'),
        //             fontSize: theme('fontSize.sm'),
        //             '&:hover': {
        //                 borderColor: theme('colors.blue.500')
        //             },
        //             '&:focus': {
        //                 borderColor: theme('colors.blue.500')
        //             }
        //         },
        //         'input, textarea': {
        //             backgroundColor: theme('colors.cool-gray.200'),
        //             borderColor: theme('colors.cool-gray.200'),
        //             paddingLeft: theme('spacing.4'),
        //             paddingRight: theme('spacing.4'),
        //             fontSize: theme('fontSize.sm'),
        //             '&:hover': {
        //                 borderColor: theme('colors.blue.500')
        //             },
        //             '&:focus': {
        //                 borderColor: theme('colors.blue.500')
        //             }
        //         }
        //     }
        // })
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ]
}