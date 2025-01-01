<script setup>
    const $auth = useAuth()
    const currentUser = useAuth().$state.user

    const links = [
        {
            label: 'General',
            icon: 'i-heroicons-user-circle',
            to: '/account',
            exact: true
        },
        {
            label: 'Security',
            icon: 'i-heroicons-lock-closed',
            to: '/account/security',
            exact: true
        },
        {
            label: 'Domains',
            to: '/account/domains',
            icon: 'i-heroicons-globe-europe-africa',
            exact: true
        },
        {
            label: 'Filters',
            to: '/account/filters',
            icon: 'i-heroicons-adjustments-horizontal',
            exact: true
        },
    ]

</script>

<template>
    <UHorizontalNavigation :links="links" class="border-b border-gray-200 dark:border-gray-800 mb-4" />
</template>