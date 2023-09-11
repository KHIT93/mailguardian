import { EnvelopeIcon, LockClosedIcon, ChartBarIcon, UserGroupIcon, GlobeEuropeAfricaIcon, ServerIcon, DocumentMagnifyingGlassIcon, DocumentTextIcon, CogIcon, ServerStackIcon, RectangleGroupIcon } from '@heroicons/vue/24/outline'
export default [
    {
        name: 'Dashboard',
        path: '/',
        admin: false,
        icon: EnvelopeIcon
    },
    {
        name: 'Allow/Deny lists',
        path: '/lists',
        admin: false,
        icon: LockClosedIcon
    },
    {
        name: 'Statistics',
        path: '/statistics',
        admin: false,
        icon: ChartBarIcon
    },
    {
        name: 'Users',
        path: '/users',
        admin: true,
        icon: UserGroupIcon
    },
    {
        name: 'Domains',
        path: '/domains',
        admin: true,
        icon: GlobeEuropeAfricaIcon
    },
    {
        name: 'Cluster',
        path: '/cluster',
        admin: true,
        icon: ServerStackIcon,
        children: [
            {
                name: 'Dashboard',
                path: '/cluster',
                admin: true,
                icon: RectangleGroupIcon
            },
            {
                name: 'Hosts',
                path: '/cluster/nodes',
                admin: true,
                icon: ServerIcon
            }
        ]
    },
    {
        name: 'Audit',
        path: '/audit',
        admin: true,
        icon: DocumentMagnifyingGlassIcon,
        children: [
            {
                name: 'Log',
                path: '/audit/log',
                admin: true,
                icon: DocumentTextIcon
            },
            {
                name: 'Settings',
                path: '/audit/settings',
                admin: true,
                icon: CogIcon
            }
        ]
    },
]
