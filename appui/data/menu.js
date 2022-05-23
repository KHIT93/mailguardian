import { MailIcon, LockClosedIcon, ChartBarIcon, UserGroupIcon, GlobeIcon, ServerIcon, DocumentSearchIcon, DocumentTextIcon, CogIcon } from '@heroicons/vue/outline/esm/index.js'
export default [
    {
        name: 'Dashboard',
        path: '/',
        admin: false,
        icon: MailIcon
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
        icon: GlobeIcon
    },
    {
        name: 'Cluster',
        path: '/cluster',
        admin: true,
        icon: ServerIcon
    },
    {
        name: 'Audit',
        path: '/audit',
        admin: true,
        icon: DocumentSearchIcon,
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
