<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user

    const endpoint = computed(() => `/me/domains`)

    const { status, data } = (await useApi(endpoint))

    const columns = [
        {
            accessorKey: 'name',
            header: 'Domain'
        },
        {
            accessorKey: 'relay_type',
            header: 'Transport'
        },
        {
            accessorKey: 'destination',
            header: 'Deliver To'
        }
    ]

</script>

<template>
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UCard v-if="currentUser.role == 'superuser'">
            You are a superuser and therefore this page is not relevant for you
        </UCard>
        <UCard v-else="">
            The below list of domains are the ones that you have access to
            <UTable :loading="status != 'success'" :columns="columns" :data="data" />
        </UCard>
    </MainLayout>
</template>