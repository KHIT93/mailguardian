<script setup>
    import TopNavigation from '~/components/account/TopNavigation'
    import MainLayout from '~/components/MainLayout.vue'

    const $auth = useAuth()
    const currentUser = useAuth().$state.user

</script>

<template>
    <MainLayout page-title="My Account">
        <TopNavigation />
        <UCard>
            
        </UCard>
    </MainLayout>
</template>