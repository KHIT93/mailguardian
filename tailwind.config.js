let defaultConfig = require('tailwindcss/defaultConfig')

module.exports = {
    theme: {
        container: {
            center: true,
            padding: '2rem',
        },
        // colors: {
        //     ...defaultConfig.theme.colors,
        //     smoke-darkest: 'rgba(0, 0, 0, 0.9)',
        //     smoke-darker: 'rgba(0, 0, 0, 0.75)',
        //     smoke-dark: 'rgba(0, 0, 0, 0.6)',
        //     smoke: 'rgba(0, 0, 0, 0.5)',
        //     smoke-light: 'rgba(0, 0, 0, 0.4)',
        //     smoke-lighter: 'rgba(0, 0, 0, 0.25)',
        //     smoke-lightest: 'rgba(0, 0, 0, 0.1)',
        // }
    },
    variants: {
        appearance: [],
        backgroundColor: ['responsive', 'hover', 'active'],
        
        borderColor: ['responsive', 'hover', 'active'],
        borderRadius: ['responsive'],
        borderStyle: ['responsive'],
        borderWidth: ['responsive'],
        cursor: [],
        display: ['responsive'],

        flex: ['responsive'],
        flexDirection: ['responsive'],
        flexWrap: ['responsive'],
        alignItems: ['responsive'],
        alignSelf: ['responsive'],
        justifyContent: ['responsive'],
        alignContent: ['responsive'],
        flexGrow: ['responsive'],
        flexShrink: ['responsive'],

        fontFamily: ['responsive'],
        fontWeight: ['responsive', 'hover'],
        height: ['responsive'],
        lineHeight: ['responsive'],

        listStylePosition: [],
        listStyleType: [],

        margin: ['responsive'],
        maxHeight: ['responsive'],
        maxWidth: ['responsive'],
        minHeight: ['responsive'],
        minWidth: ['responsive'],
        negativeMargin: ['responsive'],
        opacity: ['hover', 'focus'],
        overflow: ['responsive'],
        padding: ['responsive'],
        pointerEvents: [],

        position: ['responsive'],
        inset: ['responsive'],

        boxShadow: ['responsive', 'active'],
        fill: [],
        stroke: [],
        textAlign: ['responsive'],
        textColor: ['responsive', 'hover'],
        fontSize: ['responsive'],

        fontStyle: ['responsive', 'hover'],
        fontSmoothing: [],
        textDecoration: ['responsive', 'hover'],
        textTransform: ['responsive', 'hover'],

        letterSpacing: ['responsive'],
        userSelect: ['responsive'],
        verticalAlign: ['responsive'],
        visibility: ['responsive'],

        whitespace: ['responsive'],
        wordBreak: ['responsive'],

        width: ['responsive'],
        zIndex: ['responsive'],
    },
    corePlugins: {
        resize: false,
        float: false,
        backgroundPosition: false,
        backgroundRepeat: false,
        backgroundSize: false,
        backgroundAttachment: false,
    }
}