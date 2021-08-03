export default [
    {
        name: 'Dashboard',
        to : '/',
        admin: false
    },
    {
        name: 'Allow/Deny lists',
        to : '/lists',
        admin: false
    },
    {
        name: 'Statistics',
        to : '/statistics',
        admin: false
    },
    {
        name: 'Users',
        to : '/users',
        admin: true
    },
    {
        name: 'Domains',
        to : '/domains',
        admin: true
    },
    {
        name: 'Cluster',
        to : '/cluster',
        admin: true
    },
    {
        name: 'Audit',
        to : '/audit',
        admin: true
    },
]
